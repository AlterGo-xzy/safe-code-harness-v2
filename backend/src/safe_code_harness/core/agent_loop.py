from dataclasses import dataclass
from typing import Any, Literal

from safe_code_harness.core.action import parse_action
from safe_code_harness.core.context import build_context
from safe_code_harness.core.models import Action
from safe_code_harness.memory.store import MemoryEvent
from safe_code_harness.tools.dispatcher import ToolResult


EventKind = Literal[
    "context", "llm_action", "rule_decision", "approval", "tool_result", "feedback", "stopped"
]


@dataclass(frozen=True)
class RunConfig:
    max_steps: int
    approval_actions: frozenset[str] = frozenset()
    run_id: str = "run-1"
    memory_limit: int = 10

    def __post_init__(self) -> None:
        if self.max_steps < 1:
            raise ValueError("max_steps must be positive")
        if self.memory_limit < 1:
            raise ValueError("memory_limit must be positive")


@dataclass(frozen=True)
class RunEvent:
    kind: EventKind
    step: int
    summary: str = ""
    action_type: str | None = None
    ok: bool | None = None
    failure: str | None = None


@dataclass(frozen=True)
class RunState:
    task: str
    events: tuple[RunEvent, ...]
    status: str
    stop_reason: str
    steps: int
    approval_id: str | None = None
    pending_action: Action | None = None
    resume_cursor: int | None = None

    @property
    def tool_events(self) -> list[RunEvent]:
        return [event for event in self.events if event.kind == "tool_result"]


class AgentLoop:
    """A deterministic harness loop: the LLM proposes, local code decides and executes."""

    def __init__(self, llm: Any, rules: Any, approvals: Any, tools: Any, feedback: Any, memory: Any) -> None:
        self._llm = llm
        self._rules = rules
        self._approvals = approvals
        self._tools = tools
        self._feedback = feedback
        self._memory = memory

    def run(self, task: str, config: RunConfig) -> RunState:
        return self._continue(task, config, [], [], 0)

    def resume(self, state: RunState, config: RunConfig, approval: Any) -> RunState:
        """Continue a paused run after the caller supplies its approval decision."""

        if state.status != "waiting_approval" or state.pending_action is None or state.approval_id is None:
            raise ValueError("run is not waiting for approval")
        if getattr(approval, "id", None) != state.approval_id:
            raise ValueError("approval does not match the pending action")

        events = list(state.events)
        feedback_items = [event.summary for event in events if event.kind == "feedback"]
        steps = state.resume_cursor or state.steps
        return self._process_action(
            state.task, config, events, feedback_items, steps, state.pending_action, approval
        ) or self._continue(state.task, config, events, feedback_items, steps)

    def _continue(
        self,
        task: str,
        config: RunConfig,
        events: list[RunEvent],
        feedback_items: list[object],
        steps: int,
    ) -> RunState:
        while steps < config.max_steps:
            context = build_context(
                task, feedback_items[-config.memory_limit :], self._memory.relevant(config.memory_limit)
            )
            events.append(RunEvent("context", steps, summary=context))
            try:
                raw_action = self._llm.next_action(context)
            except Exception as exc:
                return self._stop(events, task, steps, "llm_error", type(exc).__name__)

            events.append(RunEvent("llm_action", steps, summary=raw_action))
            try:
                action = parse_action(raw_action)
            except (TypeError, ValueError, KeyError):
                self._record_feedback(events, feedback_items, config, steps, None, "invalid action")
                return self._stop(events, task, steps, "invalid_action")

            steps += 1
            if action.type == "finish":
                return self._stop(events, task, steps, "finished")

            terminal = self._process_action(task, config, events, feedback_items, steps, action)
            if terminal is not None:
                return terminal

        return self._stop(events, task, steps, "max_steps")

    def _process_action(
        self,
        task: str,
        config: RunConfig,
        events: list[RunEvent],
        feedback_items: list[object],
        steps: int,
        action: Action,
        resolved_approval: Any | None = None,
    ) -> RunState | None:
        decision = self._rules.evaluate(action)
        events.append(RunEvent("rule_decision", steps, summary=", ".join(decision.reasons), action_type=action.type))
        if decision.level == "block":
            self._record_feedback(
                events, feedback_items, config, steps, action, f"blocked by rule: {', '.join(decision.reasons)}"
            )
            return self._stop(events, task, steps, "rule_blocked")

        if action.type in config.approval_actions:
            approval = resolved_approval or self._create_approval(action)
            status = getattr(approval, "status", "rejected")
            events.append(RunEvent("approval", steps, summary=status, action_type=action.type))
            if status != "approved":
                if status == "pending":
                    return self._stop(
                        events,
                        task,
                        steps,
                        "waiting_approval",
                        approval_id=getattr(approval, "id", None),
                        pending_action=action,
                        resume_cursor=steps,
                    )
                self._record_feedback(events, feedback_items, config, steps, action, "approval rejected")
                return self._stop(events, task, steps, "approval_rejected")

        result, failure = self._dispatch(action)
        events.append(
            RunEvent("tool_result", steps, summary=result.summary, action_type=action.type, ok=result.ok, failure=failure)
        )
        self._record_feedback(events, feedback_items, config, steps, action, result)
        if steps >= config.max_steps:
            return self._stop(events, task, steps, "max_steps")
        return None

    def _create_approval(self, action: Action) -> Any:
        create = getattr(self._approvals, "create", None)
        if not callable(create):
            return _Approval("rejected")
        return create(f"{action.type} requires approval")

    def _dispatch(self, action: Action) -> tuple[ToolResult, str | None]:
        try:
            result = self._tools.dispatch(action)
            return result, "tool_failure" if not result.ok else None
        except Exception as exc:
            return ToolResult(ok=False, summary=f"tool error: {type(exc).__name__}"), "tool_exception"

    def _record_feedback(
        self,
        events: list[RunEvent],
        feedback_items: list[object],
        config: RunConfig,
        step: int,
        action: Action | None,
        result: ToolResult | str,
    ) -> None:
        feedback = self._feedback.from_result(
            action or Action("invalid", {}, None),
            result if isinstance(result, ToolResult) else ToolResult(ok=False, summary=result),
        )
        feedback_items.append(feedback)
        summary = getattr(feedback, "summary", None)
        if summary is None and isinstance(feedback, dict):
            summary = feedback.get("summary", "")
        summary = str(summary or "")
        events.append(RunEvent("feedback", step, summary=summary, action_type=action.type if action else None))
        self._memory.remember(MemoryEvent(run_id=config.run_id, summary=summary))

    @staticmethod
    def _stop(
        events: list[RunEvent],
        task: str,
        steps: int,
        reason: str,
        summary: str = "",
        approval_id: str | None = None,
        pending_action: Action | None = None,
        resume_cursor: int | None = None,
    ) -> RunState:
        events.append(RunEvent("stopped", steps, summary=summary or reason))
        status = {
            "finished": "completed",
            "rule_blocked": "blocked",
            "approval_rejected": "blocked",
            "waiting_approval": "waiting_approval",
            "invalid_action": "failed",
            "llm_error": "failed",
        }.get(reason, "stopped")
        return RunState(
            task=task,
            events=tuple(events),
            status=status,
            stop_reason=reason,
            steps=steps,
            approval_id=approval_id,
            pending_action=pending_action,
            resume_cursor=resume_cursor,
        )


@dataclass(frozen=True)
class _Approval:
    status: str

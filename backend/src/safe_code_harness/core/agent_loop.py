from dataclasses import dataclass, field
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
    require_approval: bool = False
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


@dataclass(frozen=True)
class RunState:
    task: str
    events: tuple[RunEvent, ...]
    status: str
    stop_reason: str
    steps: int

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
        events: list[RunEvent] = []
        feedback_items: list[object] = []
        steps = 0

        while steps < config.max_steps:
            context = build_context(task, feedback_items[-config.memory_limit :], self._memory.relevant(config.memory_limit))
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

            decision = self._rules.evaluate(action)
            events.append(
                RunEvent("rule_decision", steps, summary=", ".join(decision.reasons), action_type=action.type)
            )
            if decision.level == "block":
                self._record_feedback(
                    events,
                    feedback_items,
                    config,
                    steps,
                    action,
                    f"blocked by rule: {', '.join(decision.reasons)}",
                )
                return self._stop(events, task, steps, "rule_blocked")

            if decision.level == "warn" and config.require_approval:
                approval = self._create_approval(action)
                events.append(RunEvent("approval", steps, summary=approval.status, action_type=action.type))
                if approval.status != "approved":
                    reason = "approval_rejected" if approval.status == "rejected" else "waiting_approval"
                    self._record_feedback(events, feedback_items, config, steps, action, reason.replace("_", " "))
                    return self._stop(events, task, steps, reason)

            result = self._dispatch(action)
            events.append(RunEvent("tool_result", steps, summary=result.summary, action_type=action.type))
            self._record_feedback(events, feedback_items, config, steps, action, result)
            if steps >= config.max_steps:
                return self._stop(events, task, steps, "max_steps")

        return self._stop(events, task, steps, "max_steps")

    def _create_approval(self, action: Action) -> Any:
        create = getattr(self._approvals, "create", None)
        if not callable(create):
            return _Approval("rejected")
        return create(f"{action.type} requires approval")

    def _dispatch(self, action: Action) -> ToolResult:
        try:
            return self._tools.dispatch(action)
        except Exception as exc:
            return ToolResult(ok=False, summary=f"tool error: {type(exc).__name__}")

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
        events: list[RunEvent], task: str, steps: int, reason: str, summary: str = ""
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
        return RunState(task=task, events=tuple(events), status=status, stop_reason=reason, steps=steps)


@dataclass(frozen=True)
class _Approval:
    status: str

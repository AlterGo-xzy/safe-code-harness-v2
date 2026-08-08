import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Callable, Literal

from safe_code_harness.core.agent_loop import AgentLoop, RunConfig, RunState
from safe_code_harness.core.models import Action
from safe_code_harness.feedback.evaluator import FeedbackEvaluator
from safe_code_harness.governance.approval import ApprovalStateError, ApprovalStore
from safe_code_harness.governance.rules import RuleEvaluator
from safe_code_harness.llm.mock import MockLLM
from safe_code_harness.memory.store import MemoryStore
from safe_code_harness.tools.dispatcher import ToolResult


_SECRET_ASSIGNMENT = re.compile(
    r"\b(?:[A-Za-z_][A-Za-z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)|api[-_]?key|token|secret|password)"
    r"\s*[:=]\s*\S+",
    re.IGNORECASE,
)
_SECRET_VALUE = re.compile(r"\b(?:sk-proj-|sk-|ghp_|github_pat_)[A-Za-z0-9_-]+\b")


class RunNotFoundError(ValueError):
    pass


class ApprovalNotFoundError(ValueError):
    pass


class ApprovalNotPendingError(ValueError):
    pass


class _ScenarioTools:
    """Deterministic injected tool boundary used only by the offline API scenario."""

    def dispatch(self, action: Action) -> ToolResult:
        if action.type != "write_file":
            return ToolResult(ok=False, summary="unknown scenario tool")
        return ToolResult(ok=True, summary="write completed")


@dataclass
class _ManagedRun:
    loop: AgentLoop
    config: RunConfig
    approvals: ApprovalStore
    state: RunState
    approval_id: str | None
    scenario: str
    created_at: datetime
    updated_at: datetime
    creation_order: int


class RunService:
    """Keep API run state in-process while delegating all transitions to AgentLoop."""

    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self._runs: dict[str, _ManagedRun] = {}
        self._next_run_id = 1
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def start(self, scenario: Literal["pending_write", "secret_write"]) -> dict[str, object]:
        if scenario not in {"pending_write", "secret_write"}:
            raise ValueError("unsupported scenario")

        run_id = f"run-{self._next_run_id}"
        self._next_run_id += 1
        approvals = ApprovalStore()
        config = RunConfig(
            max_steps=2,
            approval_actions=frozenset({"write_file"}),
            run_id=run_id,
        )
        actions = [
            '{"type":"write_file","args":{"path":"notes.txt","content":"safe edit"}}',
            '{"type":"finish","args":{}}',
        ]
        if scenario == "secret_write":
            actions = ['{"type":"write_file","args":{"path":"notes.txt","content":"API_KEY=secret-value"}}']
        loop = AgentLoop(
            llm=MockLLM(actions),
            rules=RuleEvaluator(),
            approvals=approvals,
            tools=_ScenarioTools(),
            feedback=FeedbackEvaluator(),
            memory=MemoryStore(run_id=run_id, max_entries=10, max_bytes=4096),
        )
        state = loop.run("perform the deterministic pending write", config)
        created_at = self._timestamp()
        self._runs[run_id] = _ManagedRun(
            loop=loop,
            config=config,
            approvals=approvals,
            state=state,
            approval_id=state.approval_id,
            scenario=scenario,
            created_at=created_at,
            updated_at=created_at,
            creation_order=self._next_run_id - 1,
        )
        return self.snapshot(run_id)

    def list_summaries(self) -> list[dict[str, object]]:
        return [
            self._summary(run_id, managed)
            for run_id, managed in sorted(
                self._runs.items(), key=lambda item: (item[1].created_at, item[1].creation_order)
            )
        ]

    def snapshot(self, run_id: str) -> dict[str, object]:
        managed = self._get_run(run_id)
        state = managed.state
        return {
            "id": run_id,
            "scenario": managed.scenario,
            "status": state.status,
            "created_at": self._timestamp_value(managed.created_at),
            "updated_at": self._timestamp_value(managed.updated_at),
            "stop_reason": state.stop_reason,
            "approval_id": state.approval_id,
            "events": [self._event_payload(event) for event in state.events],
        }

    def decide(
        self, run_id: str, approval_id: str, decision: Literal["approve", "reject"]
    ) -> dict[str, object]:
        managed = self._get_run(run_id)
        if managed.approval_id is None or managed.approval_id != approval_id:
            raise ApprovalNotFoundError("approval not found")

        try:
            if decision == "approve":
                managed.approvals.approve(approval_id)
            else:
                managed.approvals.reject(approval_id)
        except ApprovalStateError as exc:
            if str(exc) == "approval request not found":
                raise ApprovalNotFoundError("approval not found") from exc
            raise ApprovalNotPendingError("approval request is not pending") from exc

        managed.state = managed.loop.resume(managed.state, managed.config)
        managed.updated_at = self._timestamp()
        return self.snapshot(run_id)

    def _summary(self, run_id: str, managed: _ManagedRun) -> dict[str, object]:
        return {
            "id": run_id,
            "scenario": managed.scenario,
            "status": managed.state.status,
            "updated_at": self._timestamp_value(managed.updated_at),
        }

    def _get_run(self, run_id: str) -> _ManagedRun:
        managed = self._runs.get(run_id)
        if managed is None:
            raise RunNotFoundError("run not found")
        return managed

    def _timestamp(self) -> datetime:
        timestamp = self._clock()
        if timestamp.tzinfo is None:
            return timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone.utc)

    @staticmethod
    def _timestamp_value(timestamp: datetime) -> str:
        return timestamp.isoformat()

    @staticmethod
    def _event_payload(event: object) -> dict[str, object]:
        payload = asdict(event)
        return {
            key: _SECRET_VALUE.sub("[REDACTED]", _SECRET_ASSIGNMENT.sub("[REDACTED]", value))
            if isinstance(value, str)
            else value
            for key, value in payload.items()
        }

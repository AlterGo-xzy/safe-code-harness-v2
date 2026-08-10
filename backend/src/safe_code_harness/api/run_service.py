from dataclasses import dataclass
from datetime import datetime, timezone
import subprocess
from typing import Callable, Literal

from safe_code_harness.core.agent_loop import AgentLoop, RunConfig, RunState
from safe_code_harness.core.models import Action
from safe_code_harness.feedback.evaluator import FeedbackEvaluator
from safe_code_harness.governance.approval import ApprovalStateError, ApprovalStore
from safe_code_harness.governance.command_guard import CommandGuard
from safe_code_harness.governance.path_sandbox import PathSandbox
from safe_code_harness.governance.policy import RuntimePolicy
from safe_code_harness.governance.rules import RuleEvaluator
from safe_code_harness.llm.mock import MockLLM
from safe_code_harness.memory.store import MemoryStore
from safe_code_harness.tools.dispatcher import ToolDispatcher, ToolResult
from safe_code_harness.tools.file_tools import FileTools
from safe_code_harness.tools.memory_tools import MemoryTools
from safe_code_harness.tools.shell_tools import ShellTools
from safe_code_harness.tools.test_tools import TestTools
from safe_code_harness.workspaces.registry import Workspace


_TIMELINE_DISPLAY_STATUS = {
    "rule_blocked": "规则已阻止操作",
    "rule_checked": "规则审查已完成",
    "approval_pending": "等待人工审批",
    "approval_approved": "审批已通过",
    "approval_rejected": "审批已拒绝",
    "tool_succeeded": "工具执行成功",
    "tool_failed": "工具执行失败",
    "run_finished": "任务已结束",
    "unknown_governed_event": "未知受治理事件",
}

_TIMELINE_SUMMARY_CODES = {
    key: key
    for key in _TIMELINE_DISPLAY_STATUS
}

_TIMELINE_LEVELS = {
    "rule_blocked": "blocked",
    "rule_checked": "info",
    "approval_pending": "warning",
    "approval_approved": "info",
    "approval_rejected": "blocked",
    "tool_succeeded": "info",
    "tool_failed": "error",
    "run_finished": "info",
    "unknown_governed_event": "warning",
}


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

    def start_real(self, task: str, workspace: Workspace, llm: object) -> dict[str, object]:
        """Run a locally opted-in real Planner inside one uploaded workspace.

        The LLM is only the proposal source.  It cannot bypass the existing
        deterministic policy, path sandbox, or approval state machine.
        """

        if not task.strip():
            raise ValueError("task is required")

        run_id = f"run-{self._next_run_id}"
        self._next_run_id += 1
        approvals = ApprovalStore()
        policy = RuntimePolicy()
        config = RunConfig(
            max_steps=6,
            approval_actions=frozenset({"write_file", "run_tests", "run_command"}),
            run_id=run_id,
        )
        loop = AgentLoop(
            llm=llm,
            rules=RuleEvaluator(policy),
            approvals=approvals,
            tools=self._workspace_tools(workspace, policy),
            feedback=FeedbackEvaluator(),
            memory=MemoryStore(run_id=run_id, max_entries=10, max_bytes=4096),
        )
        state = loop.run(task.strip(), config)
        created_at = self._timestamp()
        self._runs[run_id] = _ManagedRun(
            loop=loop,
            config=config,
            approvals=approvals,
            state=state,
            approval_id=state.approval_id,
            scenario="local_real_planner",
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
            "events": [
                self._timeline_payload(event, state.stop_reason, managed.created_at)
                for event in state.events
            ],
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
    def _workspace_tools(workspace: Workspace, policy: RuntimePolicy) -> ToolDispatcher:
        def runner(arguments: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                arguments,
                cwd=workspace.root,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

        guard = CommandGuard(policy)
        return ToolDispatcher(
            file_tools=FileTools(PathSandbox(workspace.root, policy)),
            test_tools=TestTools(guard, runner),
            shell_tools=ShellTools(guard, runner),
            memory_tools=MemoryTools(),
        )

    @staticmethod
    def _timestamp_value(timestamp: datetime) -> str:
        return timestamp.isoformat()

    @classmethod
    def _timeline_payload(
        cls, event: object, stop_reason: str, created_at: datetime
    ) -> dict[str, str]:
        mapping_key, event_type = cls._timeline_mapping(event, stop_reason)
        return {
            "type": event_type,
            "created_at": cls._timestamp_value(created_at),
            "level": _TIMELINE_LEVELS[mapping_key],
            "display_status": _TIMELINE_DISPLAY_STATUS[mapping_key],
            "summary_code": _TIMELINE_SUMMARY_CODES[mapping_key],
        }

    @staticmethod
    def _timeline_mapping(event: object, stop_reason: str) -> tuple[str, str]:
        kind = getattr(event, "kind", None)
        if kind == "rule_decision":
            return (
                ("rule_blocked", "rule_decision")
                if stop_reason == "rule_blocked"
                else ("rule_checked", "rule_decision")
            )
        if kind == "approval":
            approval_key = {
                "waiting_approval": "approval_pending",
                "approval_rejected": "approval_rejected",
            }.get(stop_reason, "approval_approved")
            return approval_key, "approval"
        if kind == "tool_result":
            return (
                ("tool_succeeded", "tool_result")
                if getattr(event, "ok", None) is True
                else ("tool_failed", "tool_result")
            )
        if kind == "stopped" and stop_reason == "finished":
            return "run_finished", "finish"
        return "unknown_governed_event", "unknown"

"""Emit an offline feedback-loop example backed by the real AgentLoop."""

import json
from pathlib import Path
import shutil
import sys
import tempfile


BACKEND_SRC = Path(__file__).parents[1] / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from safe_code_harness.core.agent_loop import AgentLoop, RunConfig
from safe_code_harness.core.models import Action
from safe_code_harness.feedback.evaluator import FeedbackEvaluator
from safe_code_harness.governance.approval import ApprovalStore
from safe_code_harness.governance.rules import RuleEvaluator
from safe_code_harness.llm.mock import MockLLM
from safe_code_harness.memory.store import MemoryStore
from safe_code_harness.tools.dispatcher import ToolResult


class _FeedbackCheckingMockLLM(MockLLM):
    """Use fixed mock actions, but refuse the repair unless feedback reached its context."""

    def __init__(self) -> None:
        super().__init__(
            [
                '{"type":"run_tests","args":{}}',
                '{"type":"write_file","args":{"path":"repair.txt","content":"fixed"}}',
                '{"type":"finish","args":{}}',
            ]
        )
        self._calls = 0

    def next_action(self, context: str) -> str:
        if self._calls == 1 and "tests failed: 2 failures" not in context:
            raise RuntimeError("feedback was not supplied before the repair action")
        self._calls += 1
        return super().next_action(context)


class _FeedbackDemoTools:
    """A bounded local tool double; only the repair may write inside the temporary directory."""

    def __init__(self, workspace: Path) -> None:
        self._workspace = workspace

    def dispatch(self, action: Action) -> ToolResult:
        if action.type == "run_tests":
            return ToolResult(ok=False, summary="tests failed: 2 failures")
        if action.type == "write_file":
            (self._workspace / "repair.txt").write_text("fixed", encoding="utf-8")
            return ToolResult(ok=True, summary="repair written")
        return ToolResult(ok=False, summary="unknown demo tool")


def run_feedback_demo() -> list[dict[str, object]]:
    """Show that failed-test feedback is present before the fixed mock chooses a repair."""
    workspace = Path(tempfile.mkdtemp(prefix="safe-code-harness-demo-"))
    try:
        loop = AgentLoop(
            llm=_FeedbackCheckingMockLLM(),
            rules=RuleEvaluator(),
            approvals=ApprovalStore(),
            tools=_FeedbackDemoTools(workspace),
            feedback=FeedbackEvaluator(),
            memory=MemoryStore(run_id="feedback-demo", max_entries=4, max_bytes=1024),
        )
        state = loop.run("repair a deterministic failing test", RunConfig(max_steps=3, run_id="feedback-demo"))
        if state.status != "completed":
            raise RuntimeError("the feedback demo did not finish")
        return [
            {"action": event.action_type, "ok": event.ok}
            for event in state.tool_events
            if event.action_type is not None and event.ok is not None
        ]
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def main() -> None:
    print(json.dumps(run_feedback_demo(), sort_keys=True))


if __name__ == "__main__":
    main()

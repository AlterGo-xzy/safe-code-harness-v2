from dataclasses import dataclass

from safe_code_harness.core.agent_loop import AgentLoop, RunConfig
from safe_code_harness.core.models import Action
from safe_code_harness.governance.rules import RuleEvaluator
from safe_code_harness.tools.dispatcher import ToolResult


class FeedbackAwareLLM:
    """Returns a repair only after the loop provides deterministic test feedback."""

    def __init__(self) -> None:
        self.contexts: list[str] = []

    def next_action(self, context: str) -> str:
        self.contexts.append(context)
        if len(self.contexts) == 2 and "tests failed: 2 failures" in context:
            return '{"type":"write_file","args":{"path":"fix.py","content":"fixed"}}'
        if len(self.contexts) == 1:
            return '{"type":"run_tests","args":{}}'
        return '{"type":"finish","args":{}}'


@dataclass
class FailingThenSuccessfulTools:
    def __post_init__(self) -> None:
        self.actions: list[Action] = []

    def dispatch(self, action: Action) -> ToolResult:
        self.actions.append(action)
        if action.type == "run_tests":
            return ToolResult(ok=False, summary="tests failed: 2 failures")
        return ToolResult(ok=True, summary="file written")


class Feedback:
    def from_result(self, action: Action, result: ToolResult) -> dict[str, str]:
        del action
        return {"kind": "tool_failure" if not result.ok else "success", "summary": result.summary}


class Memory:
    def __init__(self) -> None:
        self.remembered: list[object] = []

    def relevant(self, limit: int) -> list[object]:
        del limit
        return []

    def remember(self, event: object) -> None:
        self.remembered.append(event)


def test_failed_tests_change_the_next_mock_action_through_feedback_context() -> None:
    llm = FeedbackAwareLLM()
    tools = FailingThenSuccessfulTools()
    memory = Memory()
    loop = AgentLoop(
        llm=llm,
        rules=RuleEvaluator(),
        approvals=object(),
        tools=tools,
        feedback=Feedback(),
        memory=memory,
    )

    run = loop.run("repair", RunConfig(max_steps=3))

    assert run.stop_reason == "finished"
    assert [action.type for action in tools.actions] == ["run_tests", "write_file"]
    assert "tests failed: 2 failures" in llm.contexts[1]
    assert [event.kind for event in run.events] == [
        "context",
        "llm_action",
        "rule_decision",
        "tool_result",
        "feedback",
        "context",
        "llm_action",
        "rule_decision",
        "tool_result",
        "feedback",
        "context",
        "llm_action",
        "stopped",
    ]
    assert len(memory.remembered) == 2

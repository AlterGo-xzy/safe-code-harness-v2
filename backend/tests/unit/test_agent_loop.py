from dataclasses import dataclass

from safe_code_harness.core.agent_loop import AgentLoop, RunConfig
from safe_code_harness.core.models import Action
from safe_code_harness.governance.approval import Approval
from safe_code_harness.governance.rules import RuleEvaluator
from safe_code_harness.llm.mock import MockLLM
from safe_code_harness.tools.dispatcher import ToolResult


@dataclass
class ScriptedTools:
    results: list[ToolResult]

    def __post_init__(self) -> None:
        self.actions: list[Action] = []

    def dispatch(self, action: Action) -> ToolResult:
        self.actions.append(action)
        return self.results.pop(0)


class RejectingApprovals:
    def create(self, summary: str) -> Approval:
        return Approval(id="approval-rejected", summary=summary, status="rejected")


class RecordingMemory:
    def __init__(self) -> None:
        self.events: list[object] = []

    def relevant(self, limit: int) -> list[object]:
        del limit
        return []

    def remember(self, event: object) -> None:
        self.events.append(event)


class RecordingFeedback:
    def from_result(self, action: Action, result: ToolResult) -> object:
        del action
        return {"kind": "tool_failure" if not result.ok else "success", "summary": result.summary}


def _loop(llm: object, tools: ScriptedTools, approvals: object = object()) -> AgentLoop:
    return AgentLoop(
        llm=llm,
        rules=RuleEvaluator(),
        approvals=approvals,
        tools=tools,
        feedback=RecordingFeedback(),
        memory=RecordingMemory(),
    )


def test_finish_stops_without_dispatching_a_tool() -> None:
    tools = ScriptedTools([])

    run = _loop(MockLLM(['{"type":"finish","args":{}}']), tools).run(
        "inspect", RunConfig(max_steps=2)
    )

    assert run.stop_reason == "finished"
    assert run.status == "completed"
    assert tools.actions == []
    assert [event.kind for event in run.events] == ["context", "llm_action", "stopped"]


def test_max_steps_stops_after_the_last_permitted_action() -> None:
    tools = ScriptedTools([ToolResult(ok=True, summary="first"), ToolResult(ok=True, summary="second")])

    run = _loop(
        MockLLM(['{"type":"run_tests","args":{}}', '{"type":"run_tests","args":{}}']), tools
    ).run("test", RunConfig(max_steps=1))

    assert run.stop_reason == "max_steps"
    assert [action.type for action in tools.actions] == ["run_tests"]
    assert run.events[-1].kind == "stopped"


def test_invalid_json_stops_as_a_parse_failure_without_tool_execution() -> None:
    tools = ScriptedTools([])

    run = _loop(MockLLM(["not json"]), tools).run("repair", RunConfig(max_steps=2))

    assert run.stop_reason == "invalid_action"
    assert tools.actions == []
    assert [event.kind for event in run.events] == ["context", "llm_action", "feedback", "stopped"]


def test_rule_block_stops_before_dispatching_the_proposed_action() -> None:
    tools = ScriptedTools([])

    run = _loop(
        MockLLM(['{"type":"write_file","args":{"path":".env","content":"x"}}']), tools
    ).run("repair", RunConfig(max_steps=2))

    assert run.stop_reason == "rule_blocked"
    assert tools.actions == []
    assert [event.kind for event in run.events] == ["context", "llm_action", "rule_decision", "feedback", "stopped"]


def test_rejected_approval_stops_before_a_warned_write_is_dispatched() -> None:
    tools = ScriptedTools([])

    run = _loop(
        MockLLM(['{"type":"write_file","args":{"path":"notes.txt","content":"x"}}']),
        tools,
        RejectingApprovals(),
    ).run("repair", RunConfig(max_steps=2, require_approval=True))

    assert run.stop_reason == "approval_rejected"
    assert tools.actions == []
    assert [event.kind for event in run.events] == [
        "context",
        "llm_action",
        "rule_decision",
        "approval",
        "feedback",
        "stopped",
    ]

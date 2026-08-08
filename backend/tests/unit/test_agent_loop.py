from dataclasses import dataclass

import pytest

from safe_code_harness.core.agent_loop import AgentLoop, RunConfig
from safe_code_harness.core.models import Action
from safe_code_harness.governance.approval import Approval, ApprovalStore
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


@pytest.mark.parametrize(
    ("action_type", "args"),
    [
        ("run_command", {"command": "python -V"}),
        ("write_file", {"path": "notes.txt", "content": "x"}),
    ],
)
def test_explicit_approval_policy_pauses_command_and_write_before_dispatch(
    action_type: str, args: dict[str, str]
) -> None:
    tools = ScriptedTools([])
    approvals = ApprovalStore()

    run = _loop(
        MockLLM([f'{{"type":"{action_type}","args":{args!r}}}'.replace("'", '"')]),
        tools,
        approvals,
    ).run("repair", RunConfig(max_steps=2, approval_actions=frozenset({action_type})))

    assert run.stop_reason == "waiting_approval"
    assert run.status == "waiting_approval"
    assert run.approval_id is not None
    assert run.pending_action == Action(action_type, args, None)
    assert run.resume_cursor == 1
    assert tools.actions == []
    assert [event.kind for event in run.events] == [
        "context",
        "llm_action",
        "rule_decision",
        "approval",
        "stopped",
    ]


def test_resume_executes_pending_action_only_after_the_matching_approval() -> None:
    tools = ScriptedTools([ToolResult(ok=True, summary="command completed")])
    approvals = ApprovalStore()
    loop = _loop(
        MockLLM(['{"type":"run_command","args":{"command":"python -V"}}', '{"type":"finish","args":{}}']),
        tools,
        approvals,
    )
    config = RunConfig(max_steps=2, approval_actions=frozenset({"run_command"}))
    waiting = loop.run("repair", config)
    approved = approvals.approve(waiting.approval_id or "")

    resumed = loop.resume(waiting, config, approved)

    assert resumed.stop_reason == "finished"
    assert resumed.status == "completed"
    assert resumed.approval_id is None
    assert resumed.pending_action is None
    assert [action.type for action in tools.actions] == ["run_command"]
    approved_index = next(
        index
        for index, event in enumerate(resumed.events)
        if event.kind == "approval" and event.summary == "approved"
    )
    assert [event.kind for event in resumed.events[approved_index - 1 : approved_index + 3]] == [
        "rule_decision",
        "approval",
        "tool_result",
        "feedback",
    ]


def test_rejected_pending_approval_never_dispatches_the_action() -> None:
    tools = ScriptedTools([])
    approvals = ApprovalStore()
    loop = _loop(
        MockLLM(['{"type":"write_file","args":{"path":"notes.txt","content":"x"}}']), tools, approvals
    )
    config = RunConfig(max_steps=2, approval_actions=frozenset({"write_file"}))
    waiting = loop.run("repair", config)
    rejected = approvals.reject(waiting.approval_id or "")

    resumed = loop.resume(waiting, config, rejected)

    assert resumed.stop_reason == "approval_rejected"
    assert resumed.status == "blocked"
    assert tools.actions == []


def test_failed_tool_result_is_structured_and_retried_by_the_next_model_action() -> None:
    tools = ScriptedTools([ToolResult(ok=False, summary="test failed")])

    run = _loop(
        MockLLM(['{"type":"run_tests","args":{}}', '{"type":"finish","args":{}}']), tools
    ).run("repair", RunConfig(max_steps=2))

    tool_event = run.tool_events[0]
    assert run.stop_reason == "finished"
    assert tool_event.ok is False
    assert tool_event.failure == "tool_failure"
    assert tool_event.summary == "test failed"


class ExplodingTools:
    def __init__(self) -> None:
        self.actions: list[Action] = []

    def dispatch(self, action: Action) -> ToolResult:
        self.actions.append(action)
        raise RuntimeError("runner unavailable")


def test_tool_exception_is_structured_and_retried_by_the_next_model_action() -> None:
    tools = ExplodingTools()

    run = _loop(
        MockLLM(['{"type":"run_tests","args":{}}', '{"type":"finish","args":{}}']), tools
    ).run("repair", RunConfig(max_steps=2))

    tool_event = run.tool_events[0]
    assert run.stop_reason == "finished"
    assert tool_event.ok is False
    assert tool_event.failure == "tool_exception"
    assert "RuntimeError" in tool_event.summary

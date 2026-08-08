import pytest

from safe_code_harness.core.models import Action
from safe_code_harness.feedback.evaluator import FeedbackEvaluator
from safe_code_harness.tools.dispatcher import ToolResult


@pytest.mark.parametrize(
    ("result", "expected_kind"),
    [
        (ToolResult(ok=True, summary="file written"), "success"),
        (ToolResult(ok=False, summary="2 failed"), "tool_failure"),
        (ToolResult(ok=False, summary="blocked command"), "rule_denial"),
        (ToolResult(ok=False, summary="blocked by rule: secret_path"), "rule_denial"),
        (ToolResult(ok=False, summary="approval rejected"), "approval_denial"),
    ],
)
def test_feedback_classifies_deterministic_result_outcomes(
    result: ToolResult, expected_kind: str
) -> None:
    feedback = FeedbackEvaluator().from_result(Action("run_tests", {}, None), result)

    assert feedback.kind == expected_kind
    assert feedback.summary == result.summary


def test_failed_test_result_produces_actionable_feedback() -> None:
    feedback = FeedbackEvaluator().from_result(
        Action("run_tests", {}, None), ToolResult(ok=False, summary="2 failed")
    )

    assert feedback.kind == "tool_failure"
    assert "2 failed" in feedback.summary


def test_empty_failed_result_becomes_a_generic_tool_failure() -> None:
    feedback = FeedbackEvaluator().from_result(
        Action("run_tests", {}, None), ToolResult(ok=False, summary="")
    )

    assert feedback.kind == "tool_failure"
    assert feedback.summary == "tool failed without a summary"

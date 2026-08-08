from dataclasses import dataclass
from typing import Literal

from safe_code_harness.core.models import Action
from safe_code_harness.tools.dispatcher import ToolResult


FeedbackKind = Literal["success", "tool_failure", "rule_denial", "approval_denial"]


@dataclass(frozen=True)
class Feedback:
    kind: FeedbackKind
    summary: str


class FeedbackEvaluator:
    """Turn governed tool results into deterministic, non-policy feedback."""

    def from_result(self, action: Action, result: ToolResult) -> Feedback:
        del action
        summary = result.summary or "tool failed without a summary"
        if result.ok:
            return Feedback(kind="success", summary=summary)

        normalized_summary = result.summary.casefold()
        if normalized_summary.startswith("blocked ") or normalized_summary.startswith("rule denied"):
            return Feedback(kind="rule_denial", summary=summary)
        if normalized_summary.startswith("approval rejected") or normalized_summary.startswith("approval denied"):
            return Feedback(kind="approval_denial", summary=summary)
        return Feedback(kind="tool_failure", summary=summary)

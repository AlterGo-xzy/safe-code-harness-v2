import re
from dataclasses import dataclass
from typing import Literal

from safe_code_harness.core.models import Action
from safe_code_harness.governance.policy import RuntimePolicy


DecisionLevel = Literal["allow", "warn", "block"]
SECRET_VALUE_PATTERNS = (
    re.compile(r"\b[A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)\s*=", re.IGNORECASE),
    re.compile(r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
)


@dataclass(frozen=True)
class RuleDecision:
    level: DecisionLevel
    reasons: tuple[str, ...] = ()


class RuleEvaluator:
    """Evaluate local governance rules without model calls or external state."""

    def __init__(self, policy: RuntimePolicy | None = None) -> None:
        self.policy = policy or RuntimePolicy()

    def evaluate(self, action: Action) -> RuleDecision:
        if self._targets_sensitive_path(action):
            return RuleDecision("block", ("secret_path",))
        if self._contains_secret_value(action):
            return RuleDecision("block", ("secret_value",))
        if action.type == "write_file":
            return RuleDecision("warn", ("post_edit_tests",))
        return RuleDecision("allow")

    def _targets_sensitive_path(self, action: Action) -> bool:
        if action.type not in {"read_file", "write_file"}:
            return False
        path_parts = str(action.args.get("path", "")).replace("\\", "/").casefold().split("/")
        blocked_parts = {part.casefold() for part in self.policy.blocked_path_parts}
        return any(part in blocked_parts for part in path_parts)

    def _contains_secret_value(self, action: Action) -> bool:
        if action.type != "write_file":
            return False
        content = str(action.args.get("content", ""))
        return any(pattern.search(content) for pattern in SECRET_VALUE_PATTERNS)

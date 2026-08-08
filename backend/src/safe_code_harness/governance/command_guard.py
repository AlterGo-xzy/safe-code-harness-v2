from dataclasses import dataclass

from safe_code_harness.governance.policy import RuntimePolicy


@dataclass(frozen=True)
class GuardDecision:
    blocked: bool
    reason: str | None = None


class CommandGuard:
    """Deterministically block destructive shell commands without executing them."""

    def __init__(self, policy: RuntimePolicy) -> None:
        self.policy = policy

    def check(self, command: str) -> GuardDecision:
        normalized = " ".join(command.lower().split())
        if "rm -rf /" in normalized:
            return GuardDecision(blocked=True, reason="blocked command")
        return GuardDecision(blocked=False)

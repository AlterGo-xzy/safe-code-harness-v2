from safe_code_harness.governance.command_guard import CommandGuard
from safe_code_harness.governance.policy import RuntimePolicy


def test_guard_blocks_destructive_command_after_normalizing_case_and_whitespace() -> None:
    result = CommandGuard(RuntimePolicy()).check("  RM\t-RF\n/  ")

    assert result.blocked is True
    assert result.reason == "blocked command"


def test_guard_allows_a_safe_command() -> None:
    result = CommandGuard(RuntimePolicy()).check("python -m pytest backend/tests")

    assert result.blocked is False
    assert result.reason is None

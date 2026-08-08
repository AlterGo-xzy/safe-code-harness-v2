import pytest

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


@pytest.mark.parametrize(
    "command",
    [
        "rm -rf /",
        "rm -fr /",
        "rm -r -f /",
        "rm -rf -- /",
        "rm --recursive --force /",
        "/bin/rm -rf /",
    ],
)
def test_guard_blocks_recursive_forced_deletion_of_root(command: str) -> None:
    result = CommandGuard(RuntimePolicy()).check(command)

    assert result.blocked is True
    assert result.reason == "blocked command"


def test_guard_uses_policy_configured_blocked_executables() -> None:
    policy = RuntimePolicy(blocked_command_executables=("rm", "wipe"))

    result = CommandGuard(policy).check("wipe --force --recursive /")

    assert result.blocked is True


def test_guard_allows_a_quoted_destructive_phrase_passed_to_a_safe_command() -> None:
    result = CommandGuard(RuntimePolicy()).check('echo "rm -rf /"')

    assert result.blocked is False


@pytest.mark.parametrize("command", [None, 42, "rm -rf '"])
def test_guard_fails_closed_for_non_string_or_malformed_commands(command: object) -> None:
    result = CommandGuard(RuntimePolicy()).check(command)  # type: ignore[arg-type]

    assert result.blocked is True
    assert result.reason == "blocked command"

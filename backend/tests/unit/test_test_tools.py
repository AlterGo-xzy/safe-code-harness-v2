import subprocess

from safe_code_harness.governance.command_guard import CommandGuard, GuardDecision
from safe_code_harness.governance.policy import RuntimePolicy
from safe_code_harness.tools.test_tools import TestTools


class RecordingRunner:
    def __init__(self) -> None:
        self.calls: list[tuple[list[str], float]] = []

    def __call__(self, arguments: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
        self.calls.append((arguments, timeout))
        return subprocess.CompletedProcess(arguments, 0, stdout="3 passed\n", stderr="")


class BlockingGuard:
    def check(self, command: str) -> GuardDecision:
        return GuardDecision(blocked=True, reason="blocked command")


def test_test_tool_uses_argument_list_and_timeout_with_a_fake_runner() -> None:
    runner = RecordingRunner()
    tools = TestTools(CommandGuard(RuntimePolicy()), runner, timeout_seconds=12.5)

    result = tools.run("backend/tests/unit")

    assert result.ok is True
    assert result.summary == "tests passed"
    assert result.details == "3 passed\n"
    assert runner.calls == [(["python", "-m", "pytest", "backend/tests/unit"], 12.5)]


def test_test_tool_returns_a_blocked_result_without_calling_the_runner() -> None:
    runner = RecordingRunner()
    tools = TestTools(BlockingGuard(), runner)

    result = tools.run("backend/tests")

    assert result.ok is False
    assert result.summary == "blocked command"
    assert runner.calls == []

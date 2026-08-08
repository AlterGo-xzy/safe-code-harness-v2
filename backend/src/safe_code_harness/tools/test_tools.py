import shlex
import subprocess
from collections.abc import Callable

from safe_code_harness.governance.command_guard import CommandGuard
from safe_code_harness.tools.dispatcher import ToolResult


Runner = Callable[[list[str], float], subprocess.CompletedProcess[str]]


class TestTools:
    __test__ = False

    def __init__(self, command_guard: CommandGuard, runner: Runner, timeout_seconds: float = 30.0) -> None:
        self._command_guard = command_guard
        self._runner = runner
        self._timeout_seconds = timeout_seconds

    def run(self, path: str) -> ToolResult:
        arguments = ["python", "-m", "pytest", path]
        decision = self._command_guard.check(shlex.join(arguments))
        if decision.blocked or getattr(decision, "requires_approval", False):
            return ToolResult(ok=False, summary=decision.reason or "approval required")
        try:
            completed = self._runner(arguments, self._timeout_seconds)
        except subprocess.TimeoutExpired:
            return ToolResult(ok=False, summary="tests timed out")
        except OSError as error:
            return ToolResult(ok=False, summary="tests failed", details=str(error))
        if completed.returncode != 0:
            return ToolResult(ok=False, summary="tests failed", details=completed.stderr or completed.stdout)
        return ToolResult(ok=True, summary="tests passed", details=completed.stdout)

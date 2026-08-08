import shlex
import subprocess
from collections.abc import Callable

from safe_code_harness.governance.command_guard import CommandGuard
from safe_code_harness.tools.dispatcher import ToolResult


Runner = Callable[[list[str], float], subprocess.CompletedProcess[str]]


class ShellTools:
    def __init__(self, command_guard: CommandGuard, runner: Runner, timeout_seconds: float = 20.0) -> None:
        self._command_guard = command_guard
        self._runner = runner
        self._timeout_seconds = timeout_seconds

    def run(self, command: object) -> ToolResult:
        decision = self._command_guard.check(command)  # type: ignore[arg-type]
        if decision.blocked or getattr(decision, "requires_approval", False):
            return ToolResult(ok=False, summary=decision.reason or "approval required")
        try:
            arguments = shlex.split(command, posix=True)
            completed = self._runner(arguments, self._timeout_seconds)
        except (TypeError, ValueError):
            return ToolResult(ok=False, summary="invalid command")
        except subprocess.TimeoutExpired:
            return ToolResult(ok=False, summary="command timed out")
        except OSError as error:
            return ToolResult(ok=False, summary="command failed", details=str(error))
        if completed.returncode != 0:
            return ToolResult(ok=False, summary="command failed", details=completed.stderr or completed.stdout)
        return ToolResult(ok=True, summary="command passed", details=completed.stdout)

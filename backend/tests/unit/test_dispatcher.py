from pathlib import Path
import subprocess

from safe_code_harness.core.models import Action
from safe_code_harness.governance.command_guard import CommandGuard
from safe_code_harness.governance.path_sandbox import PathSandbox
from safe_code_harness.governance.policy import RuntimePolicy
from safe_code_harness.tools.dispatcher import ToolDispatcher
from safe_code_harness.tools.file_tools import FileTools
from safe_code_harness.tools.memory_tools import MemoryTools
from safe_code_harness.tools.shell_tools import ShellTools
from safe_code_harness.tools.test_tools import TestTools


class RecordingRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def __call__(self, arguments: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
        self.calls.append(arguments)
        return subprocess.CompletedProcess(arguments, 0, stdout="ok\n", stderr="")


def _dispatcher(tmp_path: Path, runner: RecordingRunner) -> ToolDispatcher:
    guard = CommandGuard(RuntimePolicy())
    return ToolDispatcher(
        file_tools=FileTools(PathSandbox(tmp_path)),
        test_tools=TestTools(guard, runner),
        shell_tools=ShellTools(guard, runner),
        memory_tools=MemoryTools(),
    )


def test_dispatcher_routes_only_declared_handlers(tmp_path: Path) -> None:
    runner = RecordingRunner()
    dispatcher = _dispatcher(tmp_path, runner)

    result = dispatcher.dispatch(Action("write_file", {"path": "notes.txt", "content": "kept"}, None))

    assert result.ok is True
    assert (tmp_path / "notes.txt").read_text() == "kept"
    assert runner.calls == []


def test_dispatcher_rejects_an_unknown_action_without_executing_a_handler(tmp_path: Path) -> None:
    runner = RecordingRunner()
    dispatcher = _dispatcher(tmp_path, runner)

    result = dispatcher.dispatch(Action("delete_everything", {}, None))

    assert result.ok is False
    assert result.summary == "unknown tool"
    assert runner.calls == []


def test_dispatcher_blocks_a_guarded_shell_command_before_the_runner(tmp_path: Path) -> None:
    runner = RecordingRunner()
    dispatcher = _dispatcher(tmp_path, runner)

    result = dispatcher.dispatch(Action("run_command", {"command": "rm -rf /"}, None))

    assert result.ok is False
    assert result.summary == "blocked command"
    assert runner.calls == []

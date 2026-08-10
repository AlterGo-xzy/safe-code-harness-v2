from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from safe_code_harness.core.models import Action

if TYPE_CHECKING:
    from safe_code_harness.tools.file_tools import FileTools
    from safe_code_harness.tools.memory_tools import MemoryTools
    from safe_code_harness.tools.shell_tools import ShellTools
    from safe_code_harness.tools.test_tools import TestTools


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    summary: str
    details: str = ""
    artifacts: tuple[str, ...] = field(default_factory=tuple)


class ToolDispatcher:
    """Dispatch only the fixed, governed tool action set."""

    def __init__(
        self,
        file_tools: "FileTools",
        test_tools: "TestTools",
        shell_tools: "ShellTools",
        memory_tools: "MemoryTools",
    ) -> None:
        self._handlers = {
            "read_file": lambda action: file_tools.read(str(action.args.get("path", ""))),
            "write_file": lambda action: file_tools.write(
                str(action.args.get("path", "")), str(action.args.get("content", ""))
            ),
            "run_tests": lambda action: test_tools.run(str(action.args.get("path", "backend/tests"))),
            "run_command": lambda action: shell_tools.run(action.args.get("command")),
            "remember": lambda action: memory_tools.remember(
                str(action.args.get("key", "")), str(action.args.get("value", ""))
            ),
            "recall": lambda action: memory_tools.recall(str(action.args.get("key", ""))),
        }

    def dispatch(self, action: Action) -> ToolResult:
        handler = self._handlers.get(action.type)
        if handler is None:
            return ToolResult(ok=False, summary="unknown tool")
        return handler(action)

from safe_code_harness.governance.path_sandbox import PathSandbox
from safe_code_harness.tools.dispatcher import ToolResult


class FileTools:
    def __init__(self, sandbox: PathSandbox) -> None:
        self._sandbox = sandbox

    def read(self, path: str) -> ToolResult:
        try:
            target = self._sandbox.resolve(path)
            if not target.is_file():
                return ToolResult(ok=False, summary="file read failed", details="file not found")
            return ToolResult(
                ok=True,
                summary="file read",
                details=target.read_text(encoding="utf-8"),
                artifacts=(str(target),),
            )
        except (OSError, PermissionError, UnicodeError) as error:
            return ToolResult(ok=False, summary="file read failed", details=str(error))

    def write(self, path: str, content: str) -> ToolResult:
        try:
            target = self._sandbox.resolve(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return ToolResult(ok=True, summary="file written", artifacts=(str(target),))
        except (OSError, PermissionError, UnicodeError) as error:
            return ToolResult(ok=False, summary="file write failed", details=str(error))

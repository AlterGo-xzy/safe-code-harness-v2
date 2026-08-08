from safe_code_harness.tools.dispatcher import ToolResult


class MemoryTools:
    """Small deterministic in-memory notes store for the dispatcher boundary."""

    def __init__(self) -> None:
        self._entries: dict[str, str] = {}

    def remember(self, key: str, value: str) -> ToolResult:
        if not key:
            return ToolResult(ok=False, summary="memory key is required")
        self._entries[key] = value
        return ToolResult(ok=True, summary="memory stored", artifacts=(key,))

    def recall(self, key: str) -> ToolResult:
        if key not in self._entries:
            return ToolResult(ok=False, summary="memory not found")
        return ToolResult(ok=True, summary="memory recalled", details=self._entries[key], artifacts=(key,))

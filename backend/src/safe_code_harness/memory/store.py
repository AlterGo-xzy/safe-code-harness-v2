import re
from dataclasses import dataclass, field


_SECRET_ASSIGNMENT = re.compile(
    r"\b(?:api[_-]?key|token|secret|password|authorization)\b\s*[:=]\s*\S+", re.IGNORECASE
)
_SECRET_VALUE = re.compile(r"\b(?:sk-proj-|sk-|ghp_|github_pat_)[A-Za-z0-9_-]+\b")


@dataclass(frozen=True)
class MemoryEvent:
    run_id: str
    summary: str
    details: dict[str, object] = field(default_factory=dict)


class MemoryStore:
    """Keep only redacted event summaries for one bounded harness run."""

    def __init__(self, run_id: str, max_entries: int, max_bytes: int) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be positive")
        if max_bytes < 1:
            raise ValueError("max_bytes must be positive")
        self._run_id = run_id
        self._max_entries = max_entries
        self._max_bytes = max_bytes
        self._entries: list[MemoryEvent] = []
        self._stored_bytes = 0

    def remember(self, event: MemoryEvent) -> None:
        if event.run_id != self._run_id:
            return

        stored = MemoryEvent(run_id=self._run_id, summary=self._redact(event.summary))
        stored_size = len(stored.summary.encode("utf-8"))
        if stored_size > self._max_bytes:
            return

        while self._entries and (
            len(self._entries) >= self._max_entries
            or self._stored_bytes + stored_size > self._max_bytes
        ):
            removed = self._entries.pop(0)
            self._stored_bytes -= len(removed.summary.encode("utf-8"))

        self._entries.append(stored)
        self._stored_bytes += stored_size

    def relevant(self, limit: int) -> list[MemoryEvent]:
        if limit <= 0:
            return []
        return list(self._entries[-limit:])

    @staticmethod
    def _redact(summary: str) -> str:
        redacted = _SECRET_ASSIGNMENT.sub("[REDACTED]", summary)
        return _SECRET_VALUE.sub("[REDACTED]", redacted)

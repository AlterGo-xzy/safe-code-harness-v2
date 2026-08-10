from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Action:
    type: str
    args: dict[str, Any]
    thought: str | None

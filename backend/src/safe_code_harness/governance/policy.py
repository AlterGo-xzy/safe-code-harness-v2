from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimePolicy:
    """Local, deterministic defaults for sensitive workspace paths."""

    blocked_path_parts: tuple[str, ...] = (".env", ".git", "secrets")

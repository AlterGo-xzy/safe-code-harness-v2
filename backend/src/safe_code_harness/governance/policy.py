from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimePolicy:
    """Local, deterministic defaults for sensitive workspace paths."""

    blocked_path_parts: tuple[str, ...] = (".env", ".git", "secrets")

    def blocks_path_part(self, path_part: str) -> bool:
        normalized_part = path_part.casefold()
        for blocked_part in self.blocked_path_parts:
            normalized_blocked_part = blocked_part.casefold()
            if normalized_part == normalized_blocked_part:
                return True
            if normalized_blocked_part == ".env" and normalized_part.startswith(".env."):
                return True
        return False

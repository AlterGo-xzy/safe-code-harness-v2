from pathlib import Path

from safe_code_harness.governance.policy import RuntimePolicy


class PathSandbox:
    def __init__(self, root: str | Path, policy: RuntimePolicy | None = None) -> None:
        self.root = Path(root).resolve()
        self.policy = policy or RuntimePolicy()

    def resolve(self, relative_path: str | Path) -> Path:
        raw_path = Path(relative_path)
        candidate = raw_path.resolve() if raw_path.is_absolute() else (self.root / raw_path).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PermissionError("workspace escape")

        relative_candidate = candidate.relative_to(self.root)
        if any(self.policy.blocks_path_part(part) for part in relative_candidate.parts):
            raise PermissionError("blocked sensitive path")
        return candidate

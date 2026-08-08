from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from safe_code_harness.workspaces.upload import UploadLimits, extract_verified_zip


@dataclass(frozen=True)
class Workspace:
    id: str
    root: Path
    file_count: int


class WorkspaceRegistry:
    """In-process registry for uploads isolated beneath one configured root."""

    def __init__(self, root: str | Path, limits: UploadLimits | None = None) -> None:
        self.root = Path(root).resolve()
        self.limits = limits or UploadLimits()
        self._workspaces: dict[str, Workspace] = {}

    def create_from_zip(self, upload: bytes) -> Workspace:
        workspace_id = uuid4().hex
        workspace_root = self.root / workspace_id
        file_count = extract_verified_zip(upload, workspace_root, self.limits)
        workspace = Workspace(id=workspace_id, root=workspace_root, file_count=file_count)
        self._workspaces[workspace_id] = workspace
        return workspace

    def get(self, workspace_id: str) -> Workspace:
        return self._workspaces[workspace_id]

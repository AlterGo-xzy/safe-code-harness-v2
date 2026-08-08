from __future__ import annotations

from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.responses import JSONResponse

from safe_code_harness.workspaces.registry import WorkspaceRegistry
from safe_code_harness.workspaces.upload import ArchiveRejectedError


router = APIRouter(prefix="/api/workspaces", tags=["workspaces"])

_ERROR_MESSAGES = {
    "invalid_archive": "upload must be a valid ZIP archive",
    "unsafe_archive_path": "archive contains an unsafe path",
    "protected_archive_path": "archive contains a protected path",
    "unsafe_archive_member": "archive contains an unsafe member",
    "too_many_files": "archive contains too many files",
    "archive_too_large": "archive exceeds size limits",
    "empty_archive": "archive contains no files",
}


def _registry(request: Request) -> WorkspaceRegistry:
    return request.app.state.workspace_registry


@router.post("/upload-zip", status_code=status.HTTP_201_CREATED, response_model=None)
async def upload_zip(request: Request, file: UploadFile = File(...)) -> dict[str, object] | JSONResponse:
    registry = _registry(request)
    data = await file.read(registry.limits.max_archive_bytes + 1)
    try:
        workspace = registry.create_from_zip(data)
    except ArchiveRejectedError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": exc.code, "message": _ERROR_MESSAGES[exc.code]},
        )
    return {"id": workspace.id, "file_count": workspace.file_count}

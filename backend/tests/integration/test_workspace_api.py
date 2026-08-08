from __future__ import annotations

import io
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient

from safe_code_harness.api.main import create_app
from safe_code_harness.workspaces.registry import WorkspaceRegistry


def make_zip(name: str, content: bytes) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(name, content)
    return buffer.getvalue()


def test_upload_zip_registers_an_isolated_workspace(tmp_path: Path) -> None:
    app = create_app()
    app.state.workspace_registry = WorkspaceRegistry(tmp_path)
    client = TestClient(app)

    response = client.post(
        "/api/workspaces/upload-zip",
        files={"file": ("project.zip", make_zip("src/app.py", b"pass"), "application/zip")},
    )

    assert response.status_code == 201
    payload = response.json()
    assert set(payload) == {"id", "file_count"}
    assert payload["file_count"] == 1
    workspace = app.state.workspace_registry.get(payload["id"])
    assert (workspace.root / "src" / "app.py").read_bytes() == b"pass"


def test_upload_zip_returns_safe_deterministic_error_for_zip_slip(tmp_path: Path) -> None:
    app = create_app()
    app.state.workspace_registry = WorkspaceRegistry(tmp_path)
    client = TestClient(app)

    response = client.post(
        "/api/workspaces/upload-zip",
        files={"file": ("bad.zip", make_zip("../escape.txt", b"x"), "application/zip")},
    )

    assert response.status_code == 400
    assert response.json() == {"code": "unsafe_archive_path", "message": "archive contains an unsafe path"}
    assert str(tmp_path) not in response.text


def test_upload_zip_rejects_non_zip_input(tmp_path: Path) -> None:
    app = create_app()
    app.state.workspace_registry = WorkspaceRegistry(tmp_path)
    client = TestClient(app)

    response = client.post(
        "/api/workspaces/upload-zip",
        files={"file": ("notes.txt", b"not an archive", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"code": "invalid_archive", "message": "upload must be a valid ZIP archive"}

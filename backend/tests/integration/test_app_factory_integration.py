from fastapi.testclient import TestClient

from safe_code_harness.api.main import create_app
from safe_code_harness.config.secret_store import SecretStore


class FakeCredentialManager:
    def read(self, target: str) -> str | None:
        return None

    def write(self, target: str, secret: str) -> None:
        return None

    def delete(self, target: str) -> None:
        return None


def test_factory_serves_planner_and_rejects_invalid_workspace_upload() -> None:
    """Dropping either router/state during a stacked merge must fail this real API contract."""
    app = create_app(secret_store=SecretStore(adapter=FakeCredentialManager(), platform_name="Windows"))

    with TestClient(app) as client:
        planner = client.get("/api/config/planner")
        workspace = client.post(
            "/api/workspaces/upload-zip",
            files={"file": ("not-a-zip.zip", b"not a zip", "application/zip")},
        )

    assert planner.status_code == 200
    assert planner.json()["configured"] is False
    assert workspace.status_code == 400
    assert workspace.json() == {"code": "invalid_archive", "message": "upload must be a valid ZIP archive"}

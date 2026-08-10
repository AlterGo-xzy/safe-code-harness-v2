import pytest
from fastapi.testclient import TestClient

from safe_code_harness.api.main import create_app


class FakeSecretStore:
    def __init__(self) -> None:
        self.secret: str | None = None

    def set(self, secret: str) -> None:
        self.secret = secret

    def get(self) -> str | None:
        return self.secret

    def clear(self) -> None:
        self.secret = None


@pytest.fixture
def client():
    with TestClient(create_app(secret_store=FakeSecretStore())) as test_client:
        yield test_client


def test_integrated_app_registers_run_planner_and_workspace_routes(client) -> None:
    assert client.get("/api/runs").status_code == 200
    planner = client.get("/api/config/planner")
    assert planner.status_code == 200
    assert set(planner.json()) == {"configured", "masked_suffix", "base_url", "model"}
    assert client.post(
        "/api/workspaces/upload-zip",
        files={"file": ("bad.txt", b"x", "text/plain")},
    ).status_code == 400

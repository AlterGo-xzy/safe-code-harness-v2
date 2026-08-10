from pathlib import Path

import pytest


class FakeCredentialManager:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def write(self, target: str, secret: str) -> None:
        self.values[target] = secret

    def read(self, target: str) -> str | None:
        return self.values.get(target)

    def delete(self, target: str) -> None:
        self.values.pop(target, None)


@pytest.fixture
def app(tmp_path: Path):
    from safe_code_harness.api.main import create_app
    from safe_code_harness.config.secret_store import SecretStore
    from safe_code_harness.workspaces.registry import Workspace

    app = create_app(secret_store=SecretStore(adapter=FakeCredentialManager(), platform_name="Windows"))
    workspace = Workspace(id="workspace-1", root=tmp_path / "workspace", file_count=0)
    workspace.root.mkdir()
    app.state.workspace_registry._workspaces[workspace.id] = workspace
    return app


def test_real_planner_mode_is_disabled_without_exact_local_opt_in(monkeypatch, app) -> None:
    from fastapi.testclient import TestClient

    monkeypatch.delenv("SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER", raising=False)
    with TestClient(app) as client:
        response = client.post(
            "/api/runs",
            json={"mode": "real", "task": "write one safe note", "workspace_id": "workspace-1"},
        )

    assert response.status_code == 403
    assert response.json() == {"detail": "local real Planner mode is disabled"}


def test_real_planner_mode_stays_disabled_in_the_mock_container(monkeypatch, app) -> None:
    from fastapi.testclient import TestClient

    monkeypatch.setenv("SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER", "1")
    monkeypatch.setenv("SAFE_CODE_HARNESS_DEPLOYMENT", "mock")
    with TestClient(app) as client:
        response = client.post(
            "/api/runs",
            json={"mode": "real", "task": "write one safe note", "workspace_id": "workspace-1"},
        )

    assert response.status_code == 403


def test_real_planner_requires_a_configured_key_without_sending_a_request(monkeypatch, app) -> None:
    from fastapi.testclient import TestClient

    monkeypatch.setenv("SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER", "1")
    with TestClient(app) as client:
        response = client.post(
            "/api/runs",
            json={"mode": "real", "task": "write one safe note", "workspace_id": "workspace-1"},
        )

    assert response.status_code == 409
    assert response.json() == {"detail": "Planner API key is not configured"}


def test_real_planner_actions_still_wait_for_approval_and_stay_in_workspace(monkeypatch, app) -> None:
    from fastapi.testclient import TestClient
    from safe_code_harness.llm.mock import MockLLM

    monkeypatch.setenv("SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER", "1")
    app.state.planner_configuration.create_llm = lambda: MockLLM(
        [
            '{"type":"write_file","args":{"path":"notes.txt","content":"safe local planner note"}}',
            '{"type":"finish","args":{}}',
        ]
    )
    with TestClient(app) as client:
        started = client.post(
            "/api/runs",
            json={"mode": "real", "task": "write one safe note", "workspace_id": "workspace-1"},
        )
        assert started.status_code == 201
        body = started.json()
        assert body["scenario"] == "local_real_planner"
        assert body["status"] == "waiting_approval"
        assert all(event["summary_code"] != "tool_succeeded" for event in body["events"])

        approved = client.post(f"/api/runs/{body['id']}/approvals/{body['approval_id']}/approve")

    assert approved.status_code == 200
    assert (app.state.workspace_registry.get("workspace-1").root / "notes.txt").read_text() == "safe local planner note"

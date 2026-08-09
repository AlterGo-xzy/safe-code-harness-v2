from fastapi.testclient import TestClient


def test_e2e_app_starts_with_empty_memory_store_without_windows_credential_manager(monkeypatch) -> None:
    """Starting or reading E2E Planner settings must never cross the OS credential boundary."""
    from safe_code_harness.config import secret_store

    credential_manager_attempts: list[str] = []

    class ForbiddenWindowsCredentialManager:
        def __init__(self) -> None:
            credential_manager_attempts.append("constructed")
            raise AssertionError("E2E must not access Windows Credential Manager")

    monkeypatch.setattr(secret_store, "WindowsCredentialManager", ForbiddenWindowsCredentialManager)

    from safe_code_harness.api.e2e_app import app

    with TestClient(app) as client:
        response = client.get("/api/config/planner")

    assert response.status_code == 200
    assert response.json() == {
        "configured": False,
        "masked_suffix": None,
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    }
    assert credential_manager_attempts == []

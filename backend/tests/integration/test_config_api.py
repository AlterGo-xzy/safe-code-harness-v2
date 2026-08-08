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
def client():
    from fastapi.testclient import TestClient
    from safe_code_harness.api.main import create_app
    from safe_code_harness.config.secret_store import SecretStore

    app = create_app(secret_store=SecretStore(adapter=FakeCredentialManager(), platform_name="Windows"))
    with TestClient(app) as test_client:
        yield test_client


def test_config_response_is_masked_and_never_contains_the_submitted_secret(client) -> None:
    """Returning api_key from GET or PUT would make this test fail."""
    secret = "fixture-secret-2026"

    saved = client.put(
        "/api/config/planner",
        json={"base_url": "https://planner.invalid/v1", "model": "offline-model", "api_key": secret},
    )
    current = client.get("/api/config/planner")

    assert saved.status_code == 200
    assert current.status_code == 200
    assert set(current.json()) == {"configured", "masked_suffix", "base_url", "model"}
    assert current.json() == {
        "configured": True,
        "masked_suffix": "2026",
        "base_url": "https://planner.invalid/v1",
        "model": "offline-model",
    }
    assert secret not in repr(saved.json())
    assert secret not in repr(current.json())


def test_clear_removes_the_key_but_preserves_non_secret_planner_settings(client) -> None:
    client.put(
        "/api/config/planner",
        json={"base_url": "https://planner.invalid/v1", "model": "offline-model", "api_key": "fixture-secret-2026"},
    )

    cleared = client.delete("/api/config/planner")

    assert cleared.status_code == 200
    assert cleared.json() == {
        "configured": False,
        "masked_suffix": None,
        "base_url": "https://planner.invalid/v1",
        "model": "offline-model",
    }


@pytest.mark.parametrize("field, value", [("base_url", " "), ("model", "")])
def test_empty_non_secret_settings_are_rejected(field: str, value: str, client) -> None:
    payload = {"base_url": "https://planner.invalid/v1", "model": "offline-model", "api_key": "fixture-secret-2026"}
    payload[field] = value

    response = client.put("/api/config/planner", json=payload)

    assert response.status_code == 422

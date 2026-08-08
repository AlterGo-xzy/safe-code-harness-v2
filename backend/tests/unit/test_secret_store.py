import traceback

import pytest


class FakeCredentialManager:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.calls: list[tuple[str, str]] = []

    def write(self, target: str, secret: str) -> None:
        self.calls.append(("write", target))
        self.values[target] = secret

    def read(self, target: str) -> str | None:
        self.calls.append(("read", target))
        return self.values.get(target)

    def delete(self, target: str) -> None:
        self.calls.append(("delete", target))
        self.values.pop(target, None)


def test_windows_store_round_trips_and_clears_through_credential_manager() -> None:
    """Replacing the adapter calls with disk I/O would make this test fail."""
    from safe_code_harness.config.secret_store import SecretStore

    adapter = FakeCredentialManager()
    store = SecretStore(adapter=adapter, platform_name="Windows")

    store.set("fixture-secret-2026")
    assert store.get() == "fixture-secret-2026"
    store.clear()

    assert store.get() is None
    assert [operation for operation, _ in adapter.calls] == ["write", "read", "delete", "read"]


def test_non_windows_store_fails_closed_without_creating_a_fallback_file(tmp_path) -> None:
    """Adding a plaintext fallback makes this test fail."""
    from safe_code_harness.config.secret_store import SecretStore, SecretStoreUnavailableError

    store = SecretStore(platform_name="Linux")

    with pytest.raises(SecretStoreUnavailableError, match="Credential Manager"):
        store.set("fixture-secret-2026")

    assert list(tmp_path.iterdir()) == []


def test_adapter_failure_fails_closed_and_does_not_reveal_the_secret() -> None:
    from safe_code_harness.config.secret_store import SecretStore, SecretStoreUnavailableError

    class FailingCredentialManager:
        def write(self, target: str, secret: str) -> None:
            raise OSError("credential service unavailable")

        def read(self, target: str) -> str | None:
            raise OSError("credential service unavailable")

        def delete(self, target: str) -> None:
            raise OSError("credential service unavailable")

    store = SecretStore(adapter=FailingCredentialManager(), platform_name="Windows")

    with pytest.raises(SecretStoreUnavailableError) as raised:
        store.set("fixture-secret-2026")

    assert "fixture-secret-2026" not in str(raised.value)


@pytest.mark.parametrize("operation", ["set", "get", "clear"])
def test_adapter_failure_cannot_leak_a_secret_through_the_exception_traceback(operation: str) -> None:
    """Chaining the adapter exception would make the fixture secret visible here."""
    from safe_code_harness.config.secret_store import SecretStore, SecretStoreUnavailableError

    secret = "fixture-secret-2026"

    class SecretLeakingCredentialManager:
        def write(self, target: str, value: str) -> None:
            raise OSError(f"credential failure: {secret}")

        def read(self, target: str) -> str | None:
            raise OSError(f"credential failure: {secret}")

        def delete(self, target: str) -> None:
            raise OSError(f"credential failure: {secret}")

    store = SecretStore(adapter=SecretLeakingCredentialManager(), platform_name="Windows")

    with pytest.raises(SecretStoreUnavailableError) as raised:
        if operation == "set":
            store.set(secret)
        elif operation == "get":
            store.get()
        else:
            store.clear()

    assert secret not in "".join(traceback.format_exception(raised.value))

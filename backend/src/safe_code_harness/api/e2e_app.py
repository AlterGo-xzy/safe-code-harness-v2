"""Offline-only FastAPI entrypoint for browser end-to-end tests."""

from fastapi import FastAPI

from safe_code_harness.api.main import create_app


class _InMemorySecretStore:
    """Keep fixture credentials process-local and initially empty."""

    def __init__(self) -> None:
        self._secret: str | None = None

    def set(self, secret: str) -> None:
        self._secret = secret

    def get(self) -> str | None:
        return self._secret

    def clear(self) -> None:
        self._secret = None


def create_e2e_app() -> FastAPI:
    return create_app(secret_store=_InMemorySecretStore())


app = create_e2e_app()

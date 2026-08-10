from collections.abc import Callable
from typing import Protocol

import httpx


class _SecretReader(Protocol):
    def get(self) -> str | None: ...


class PlannerNotConfiguredError(RuntimeError):
    pass


Transport = Callable[[str, dict[str, str], dict[str, object]], dict[str, object]]


class OpenAICompatibleLLM:
    """One OpenAI-compatible completion call behind an injectable transport."""

    def __init__(self, base_url: str, model: str, secret_store: _SecretReader, transport: Transport | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._secret_store = secret_store
        self._transport = transport or self._post_json

    def next_action(self, context: str) -> str:
        secret = self._secret_store.get()
        if not secret:
            raise PlannerNotConfiguredError("Planner API key is not configured")
        response = self._transport(
            f"{self._base_url}/chat/completions",
            {"Authorization": f"Bearer {secret}", "Content-Type": "application/json"},
            {"model": self._model, "messages": [{"role": "user", "content": context}]},
        )
        try:
            return str(response["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Planner response did not contain a message action") from exc

    @staticmethod
    def _post_json(url: str, headers: dict[str, str], payload: dict[str, object]) -> dict[str, object]:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json()

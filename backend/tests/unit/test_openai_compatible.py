import pytest


def test_next_action_uses_an_injected_offline_transport_and_returns_the_provider_content() -> None:
    """Removing the transport call or changing the action extraction makes this fail."""
    from safe_code_harness.llm.openai_compatible import OpenAICompatibleLLM

    observed: dict[str, object] = {}

    def fake_transport(url: str, headers: dict[str, str], payload: dict[str, object]) -> dict[str, object]:
        observed.update(url=url, headers=headers, payload=payload)
        return {"choices": [{"message": {"content": '{"type":"finish","args":{}}'}}]}

    llm = OpenAICompatibleLLM(
        base_url="https://planner.invalid/v1",
        model="offline-model",
        secret_store=type("Store", (), {"get": lambda self: "fixture-secret-2026"})(),
        transport=fake_transport,
    )

    assert llm.next_action("finish safely") == '{"type":"finish","args":{}}'
    assert observed["url"] == "https://planner.invalid/v1/chat/completions"
    assert observed["headers"] == {"Authorization": "Bearer fixture-secret-2026", "Content-Type": "application/json"}
    assert observed["payload"] == {"model": "offline-model", "messages": [{"role": "user", "content": "finish safely"}]}


def test_missing_secret_raises_without_calling_the_transport() -> None:
    from safe_code_harness.llm.openai_compatible import OpenAICompatibleLLM, PlannerNotConfiguredError

    calls = 0

    def fake_transport(url: str, headers: dict[str, str], payload: dict[str, object]) -> dict[str, object]:
        nonlocal calls
        calls += 1
        return {}

    llm = OpenAICompatibleLLM(
        base_url="https://planner.invalid/v1",
        model="offline-model",
        secret_store=type("Store", (), {"get": lambda self: None})(),
        transport=fake_transport,
    )

    with pytest.raises(PlannerNotConfiguredError):
        llm.next_action("finish safely")

    assert calls == 0

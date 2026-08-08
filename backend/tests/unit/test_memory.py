import pytest

from safe_code_harness.memory.store import MemoryEvent, MemoryStore


def test_memory_keeps_current_run_entries_within_fifo_entry_limit() -> None:
    store = MemoryStore(run_id="run-a", max_entries=2, max_bytes=64)

    store.remember(MemoryEvent(run_id="run-a", summary="first"))
    store.remember(MemoryEvent(run_id="run-a", summary="second"))
    store.remember(MemoryEvent(run_id="run-a", summary="third"))

    assert [event.summary for event in store.relevant(limit=10)] == ["second", "third"]


def test_memory_evicts_oldest_entries_when_summary_bytes_exceed_budget() -> None:
    store = MemoryStore(run_id="run-a", max_entries=3, max_bytes=8)

    store.remember(MemoryEvent(run_id="run-a", summary="aaaa"))
    store.remember(MemoryEvent(run_id="run-a", summary="bbbb"))
    store.remember(MemoryEvent(run_id="run-a", summary="c"))

    assert [event.summary for event in store.relevant(limit=10)] == ["bbbb", "c"]


def test_memory_discards_events_from_other_runs() -> None:
    store = MemoryStore(run_id="run-a", max_entries=3, max_bytes=64)

    store.remember(MemoryEvent(run_id="run-b", summary="other run"))
    store.remember(MemoryEvent(run_id="run-a", summary="current run"))

    assert store.relevant(limit=10) == [MemoryEvent(run_id="run-a", summary="current run")]


def test_memory_stores_redacted_summaries_without_event_details() -> None:
    store = MemoryStore(run_id="run-a", max_entries=3, max_bytes=128)
    secret = "sk-proj-abcdefghijklmnopqrstuvwxyz"

    store.remember(
        MemoryEvent(
            run_id="run-a",
            summary=f"wrote API_KEY={secret}",
            details={"api_key": secret, "file_original": "print('source')"},
        )
    )

    stored = store.relevant(limit=1)[0]

    assert secret not in stored.summary
    assert "API_KEY" not in stored.summary
    assert "print('source')" not in str(stored)
    assert stored.details == {}


@pytest.mark.parametrize(
    "summary",
    [
        "wrote OPENAI_API_KEY=plainvalue",
        "wrote GITHUB_TOKEN=plainvalue",
        "wrote CUSTOM_TOKEN=plainvalue",
        "sent Authorization: Bearer tokenvalue",
        "sent Authorization: Basic dXNlcjpwYXNz",
    ],
)
def test_memory_fully_redacts_prefixed_assignments_and_authorization_values(summary: str) -> None:
    store = MemoryStore(run_id="run-a", max_entries=3, max_bytes=128)

    store.remember(MemoryEvent(run_id="run-a", summary=summary))

    stored_summary = store.relevant(limit=1)[0].summary

    assert stored_summary.endswith("[REDACTED]")
    assert "plainvalue" not in stored_summary
    assert "tokenvalue" not in stored_summary
    assert "dXNlcjpwYXNz" not in stored_summary


def test_memory_events_are_immutable_and_caller_mutation_cannot_pollute_storage() -> None:
    store = MemoryStore(run_id="run-a", max_entries=3, max_bytes=128)
    provided_details = {"source": "caller"}
    event = MemoryEvent(run_id="run-a", summary="safe summary", details=provided_details)

    store.remember(event)
    provided_details["source"] = "changed after remember"
    stored = store.relevant(limit=1)[0]

    assert stored.details == {}
    with pytest.raises(TypeError):
        stored.details["poison"] = "outside mutation"
    assert store.relevant(limit=1)[0].details == {}


def test_memory_returns_no_events_for_an_empty_store() -> None:
    store = MemoryStore(run_id="run-a", max_entries=3, max_bytes=64)

    assert store.relevant(limit=5) == []

import pytest

from safe_code_harness.llm.mock import MockLLM


def test_mock_llm_returns_responses_in_configured_order() -> None:
    client = MockLLM(['{"type":"read_file","args":{}}', '{"type":"stop","args":{}}'])

    assert client.next_action("first context") == '{"type":"read_file","args":{}}'
    assert client.next_action("second context") == '{"type":"stop","args":{}}'


def test_mock_llm_rejects_calls_after_responses_are_exhausted() -> None:
    client = MockLLM([])

    with pytest.raises(RuntimeError, match="exhausted"):
        client.next_action("context")

import json

import pytest

from safe_code_harness.core.action import parse_action


def test_parse_action_returns_the_declared_protocol_fields() -> None:
    action = parse_action(
        '{"type":"run_tests","args":{"path":"backend/tests"},"thought":"verify changes"}'
    )

    assert action.type == "run_tests"
    assert action.args == {"path": "backend/tests"}
    assert action.thought == "verify changes"


def test_parse_action_rejects_non_object_args() -> None:
    with pytest.raises(ValueError, match="args must be an object"):
        parse_action('{"type":"run_tests","args":[]}')


def test_parse_action_rejects_invalid_json() -> None:
    with pytest.raises(json.JSONDecodeError):
        parse_action("not json")


def test_parse_action_requires_type() -> None:
    with pytest.raises(KeyError):
        parse_action('{"args":{}}')

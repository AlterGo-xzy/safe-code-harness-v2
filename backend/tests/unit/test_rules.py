import pytest

from safe_code_harness.core.models import Action
from safe_code_harness.governance.rules import RuleEvaluator


@pytest.mark.parametrize("path", [".env", ".git/config", "secrets/token.txt"])
def test_rules_block_secret_bearing_file_actions(path: str) -> None:
    decision = RuleEvaluator().evaluate(Action("read_file", {"path": path}, None))

    assert decision.level == "block"


def test_rules_block_secret_like_write_content() -> None:
    decision = RuleEvaluator().evaluate(
        Action("write_file", {"path": "src/config.py", "content": "API_KEY=top-secret"}, None)
    )

    assert decision.level == "block"


def test_rules_warn_before_a_file_write() -> None:
    decision = RuleEvaluator().evaluate(
        Action("write_file", {"path": "src/main.py", "content": "print('hello')"}, None)
    )

    assert decision.level == "warn"


def test_rules_allow_an_unrestricted_action() -> None:
    decision = RuleEvaluator().evaluate(Action("run_tests", {"path": "backend/tests"}, None))

    assert decision.level == "allow"

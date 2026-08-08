"""Offline contracts for the deterministic Harness mechanism demos."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.run_approval_demo import run_approval_demo
from scripts.run_feedback_demo import run_feedback_demo
from scripts.run_guardrail_demo import run_guardrail_demo


PROJECT_ROOT = Path(__file__).parents[3]


def test_guardrail_demo_reports_a_blocked_destructive_command() -> None:
    """Allowing the destructive command or exposing its text would break this contract."""
    assert run_guardrail_demo() == {
        "scenario": "destructive_command",
        "blocked": True,
        "reason_code": "blocked_command",
    }


def test_feedback_demo_requires_failed_test_feedback_before_the_repair_action() -> None:
    """Skipping feedback context or dispatching the repair first would break this contract."""
    assert run_feedback_demo() == [
        {"action": "run_tests", "ok": False},
        {"action": "write_file", "ok": True},
    ]


def test_approval_demo_projects_actual_approval_and_execution_transitions() -> None:
    """Executing before approval or omitting the real resumed execution would break this contract."""
    assert run_approval_demo() == [
        {"stage": "waiting_approval", "executed": False},
        {"stage": "approved", "executed": False},
        {"stage": "executed", "executed": True},
    ]


@pytest.mark.parametrize(
    ("script_name", "expected"),
    [
        (
            "run_guardrail_demo.py",
            {"scenario": "destructive_command", "blocked": True, "reason_code": "blocked_command"},
        ),
        (
            "run_feedback_demo.py",
            [{"action": "run_tests", "ok": False}, {"action": "write_file", "ok": True}],
        ),
        (
            "run_approval_demo.py",
            [
                {"stage": "waiting_approval", "executed": False},
                {"stage": "approved", "executed": False},
                {"stage": "executed", "executed": True},
            ],
        ),
    ],
)
def test_demo_cli_emits_stable_redacted_json(script_name: str, expected: object) -> None:
    """Adding a path, sensitive value, or non-JSON CLI output would break this contract."""
    completed = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / script_name)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == expected
    rendered = completed.stdout.casefold()
    assert "c:" not in rendered
    assert "d:" not in rendered
    assert "secret" not in rendered

"""Offline contracts for the deterministic Harness mechanism demos."""

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

import pytest

from safe_code_harness.api.run_service import RunService
from scripts.run_approval_demo import _project_approval_transcript, run_approval_demo
from scripts.run_feedback_demo import _remove_demo_workspace, run_feedback_demo
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


def _approval_snapshots() -> tuple[dict[str, object], dict[str, object]]:
    service = RunService(clock=lambda: datetime(2026, 8, 9, tzinfo=timezone.utc))
    pending = service.start("pending_write")
    approval_id = pending["approval_id"]
    assert isinstance(approval_id, str)
    completed = service.decide(str(pending["id"]), approval_id, "approve")
    return pending, completed


def test_approval_projection_rejects_execution_recorded_while_waiting() -> None:
    """Treating a waiting snapshot with executed work as safe would break this contract."""
    pending, completed = _approval_snapshots()
    invalid_pending = deepcopy(pending)
    invalid_pending["events"].append({"summary_code": "tool_succeeded"})

    with pytest.raises(RuntimeError, match="waiting approval evidence already contains execution"):
        _project_approval_transcript(invalid_pending, completed)


def test_approval_projection_rejects_execution_before_approval() -> None:
    """Projecting an event order that executes before approval would break this contract."""
    pending, completed = _approval_snapshots()
    invalid_completed = deepcopy(completed)
    events = invalid_completed["events"]
    approval_index = max(index for index, event in enumerate(events) if event["summary_code"] == "approval_approved")
    execution_index = next(index for index, event in enumerate(events) if event["summary_code"] == "tool_succeeded")
    events[approval_index], events[execution_index] = events[execution_index], events[approval_index]

    with pytest.raises(RuntimeError, match="approval evidence must precede execution"):
        _project_approval_transcript(pending, invalid_completed)


@pytest.mark.skipif(sys.platform != "win32", reason="PowerShell entrypoint is a Windows-only contract")
def test_windows_demo_entrypoint_stops_after_a_child_failure(tmp_path: Path) -> None:
    """Continuing after a nonzero demo process would break the entrypoint contract."""
    failing_script = tmp_path / "fails.py"
    failing_script.write_text("raise SystemExit(7)\n", encoding="utf-8")

    completed = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-File",
            str(PROJECT_ROOT / "scripts" / "run_demos.ps1"),
            "-PythonExecutable",
            sys.executable,
            "-DemoScripts",
            str(failing_script),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "A deterministic demo failed." in completed.stdout + completed.stderr


def test_feedback_demo_cleanup_failure_is_reported(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Silently ignoring a temporary-workspace cleanup error would break this contract."""

    def fail_removal(path: Path) -> None:
        del path
        raise OSError("cleanup failed")

    monkeypatch.setattr("scripts.run_feedback_demo.shutil.rmtree", fail_removal)

    with pytest.raises(RuntimeError, match="demo workspace cleanup failed"):
        _remove_demo_workspace(tmp_path)


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

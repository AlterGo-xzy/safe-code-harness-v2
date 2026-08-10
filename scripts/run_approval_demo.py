"""Emit an offline approval example backed by the real RunService transition."""

from datetime import datetime, timezone
import json
from pathlib import Path
import sys


BACKEND_SRC = Path(__file__).parents[1] / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from safe_code_harness.api.run_service import RunService


_TOOL_RESULT_CODES = frozenset({"tool_succeeded", "tool_failed"})


def _event_codes(snapshot: dict[str, object]) -> list[str]:
    events = snapshot.get("events")
    if not isinstance(events, list):
        raise RuntimeError("approval event evidence is incomplete")
    codes: list[str] = []
    for event in events:
        if not isinstance(event, dict):
            raise RuntimeError("approval event evidence is incomplete")
        code = event.get("summary_code")
        if not isinstance(code, str):
            raise RuntimeError("approval event evidence is incomplete")
        codes.append(code)
    return codes


def _project_approval_transcript(
    pending: dict[str, object], completed: dict[str, object]
) -> list[dict[str, object]]:
    """Derive the stable transcript only from the real pending and completed snapshots."""
    if pending.get("status") != "waiting_approval" or not isinstance(pending.get("approval_id"), str):
        raise RuntimeError("the approval scenario did not pause before execution")
    if any(code in _TOOL_RESULT_CODES for code in _event_codes(pending)):
        raise RuntimeError("waiting approval evidence already contains execution")
    if completed.get("status") != "completed":
        raise RuntimeError("the approval transition did not complete")

    event_codes = _event_codes(completed)
    approval_positions = [index for index, code in enumerate(event_codes) if code == "approval_approved"]
    execution_positions = [index for index, code in enumerate(event_codes) if code == "tool_succeeded"]
    if not approval_positions or len(execution_positions) != 1:
        raise RuntimeError("approval event evidence is incomplete")
    approval_position = approval_positions[-1]
    execution_position = execution_positions[0]
    if any(
        index <= approval_position and code in _TOOL_RESULT_CODES
        for index, code in enumerate(event_codes)
    ):
        raise RuntimeError("approval evidence must precede execution")
    if approval_position >= execution_position:
        raise RuntimeError("approval evidence must precede execution")

    transcript = [{"stage": "waiting_approval", "executed": False}]
    for index, code in enumerate(event_codes):
        if index == approval_position:
            transcript.append({"stage": "approved", "executed": False})
        elif index == execution_position:
            transcript.append({"stage": "executed", "executed": True})
    return transcript


def run_approval_demo() -> list[dict[str, object]]:
    """Start and approve a real run, then project its evidence into stable JSON."""
    service = RunService(clock=lambda: datetime(2026, 8, 9, tzinfo=timezone.utc))
    pending = service.start("pending_write")
    approval_id = pending.get("approval_id")
    if not isinstance(approval_id, str):
        raise RuntimeError("the approval scenario did not pause before execution")
    completed = service.decide(str(pending["id"]), approval_id, "approve")
    return _project_approval_transcript(pending, completed)


def main() -> None:
    print(json.dumps(run_approval_demo(), sort_keys=True))


if __name__ == "__main__":
    main()

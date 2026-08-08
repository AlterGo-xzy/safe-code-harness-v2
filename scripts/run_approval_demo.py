"""Emit an offline approval example backed by the real RunService transition."""

from datetime import datetime, timezone
import json
from pathlib import Path
import sys


BACKEND_SRC = Path(__file__).parents[1] / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from safe_code_harness.api.run_service import RunService


def run_approval_demo() -> list[dict[str, object]]:
    """Project the actual pending, approved-event, and resumed-execution evidence."""
    service = RunService(clock=lambda: datetime(2026, 8, 9, tzinfo=timezone.utc))
    pending = service.start("pending_write")
    approval_id = pending.get("approval_id")
    if pending.get("status") != "waiting_approval" or not isinstance(approval_id, str):
        raise RuntimeError("the approval scenario did not pause before execution")

    completed = service.decide(str(pending["id"]), approval_id, "approve")
    event_codes = [str(event.get("summary_code")) for event in completed.get("events", [])]
    if completed.get("status") != "completed" or "approval_approved" not in event_codes:
        raise RuntimeError("the approval transition did not complete")
    if "tool_succeeded" not in event_codes:
        raise RuntimeError("the approved action was not executed")

    return [
        {"stage": "waiting_approval", "executed": False},
        {"stage": "approved", "executed": False},
        {"stage": "executed", "executed": True},
    ]


def main() -> None:
    print(json.dumps(run_approval_demo(), sort_keys=True))


if __name__ == "__main__":
    main()

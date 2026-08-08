"""Emit a stable offline example of the destructive-command guardrail."""

import json
from pathlib import Path
import sys


BACKEND_SRC = Path(__file__).parents[1] / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from safe_code_harness.governance.command_guard import CommandGuard
from safe_code_harness.governance.policy import RuntimePolicy


def run_guardrail_demo() -> dict[str, object]:
    """Project the real guard decision without exposing the checked command."""
    decision = CommandGuard(RuntimePolicy()).check("rm -rf /")
    if not decision.blocked or decision.reason != "blocked command":
        raise RuntimeError("the destructive-command guardrail did not block the scenario")
    return {
        "scenario": "destructive_command",
        "blocked": True,
        "reason_code": "blocked_command",
    }


def main() -> None:
    print(json.dumps(run_guardrail_demo(), sort_keys=True))


if __name__ == "__main__":
    main()

import json

from safe_code_harness.core.models import Action


def parse_action(raw: str) -> Action:
    payload = json.loads(raw)
    if not isinstance(payload.get("args"), dict):
        raise ValueError("args must be an object")
    return Action(type=payload["type"], args=payload["args"], thought=payload.get("thought"))

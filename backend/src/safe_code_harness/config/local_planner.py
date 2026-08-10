"""Explicit opt-in guard for real Planner calls from a local development process."""

from __future__ import annotations

import os


_FLAG = "SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER"


def real_planner_enabled() -> bool:
    """Return true only for the exact local opt-in value.

    Railway and all other deployments remain Mock-only unless their operator
    deliberately changes this process environment.  There is no silent
    fallback from a requested real run to MockLLM.
    """

    return os.environ.get(_FLAG) == "1" and os.environ.get("SAFE_CODE_HARNESS_DEPLOYMENT") != "mock"

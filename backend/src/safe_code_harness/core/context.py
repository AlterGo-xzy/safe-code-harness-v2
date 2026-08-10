from collections.abc import Iterable, Mapping
from typing import Any


def build_context(task: str, feedback: Iterable[object], memory: Iterable[object]) -> str:
    """Build the bounded, text-only input supplied to one LLM decision call."""

    sections = [f"Task: {task}"]
    feedback_summaries = [_summary(item) for item in feedback]
    memory_summaries = [_summary(item) for item in memory]
    if feedback_summaries:
        sections.append("Feedback:\n" + "\n".join(feedback_summaries))
    if memory_summaries:
        sections.append("Memory:\n" + "\n".join(memory_summaries))
    return "\n\n".join(sections)


def _summary(value: object) -> str:
    if isinstance(value, Mapping):
        return str(value.get("summary", value))
    summary = getattr(value, "summary", None)
    return str(summary if summary is not None else value)

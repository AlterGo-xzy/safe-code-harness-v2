from dataclasses import dataclass
from typing import Literal


ApprovalStatus = Literal["pending", "approved", "rejected"]


class ApprovalStateError(ValueError):
    """Raised when a request is missing or no longer pending."""


@dataclass(frozen=True)
class Approval:
    id: str
    summary: str
    status: ApprovalStatus


class ApprovalStore:
    """In-memory approval state machine; it never executes the requested action."""

    def __init__(self) -> None:
        self._requests: dict[str, Approval] = {}
        self._next_id = 1

    def create(self, summary: str) -> Approval:
        approval_id = f"approval-{self._next_id}"
        self._next_id += 1
        approval = Approval(id=approval_id, summary=summary, status="pending")
        self._requests[approval_id] = approval
        return approval

    def approve(self, approval_id: str) -> Approval:
        return self._transition(approval_id, "approved")

    def reject(self, approval_id: str) -> Approval:
        return self._transition(approval_id, "rejected")

    def _transition(self, approval_id: str, status: ApprovalStatus) -> Approval:
        approval = self._requests.get(approval_id)
        if approval is None:
            raise ApprovalStateError("approval request not found")
        if approval.status != "pending":
            raise ApprovalStateError("approval request is not pending")
        updated = Approval(id=approval.id, summary=approval.summary, status=status)
        self._requests[approval_id] = updated
        return updated

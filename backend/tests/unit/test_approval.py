import pytest

from safe_code_harness.governance.approval import ApprovalStateError, ApprovalStore


def test_approval_store_creates_a_pending_request_then_approves_it() -> None:
    store = ApprovalStore()

    created = store.create("run command")
    approved = store.approve(created.id)

    assert created.status == "pending"
    assert approved.id == created.id
    assert approved.status == "approved"


def test_approval_store_can_reject_a_pending_request() -> None:
    store = ApprovalStore()
    created = store.create("write file")

    rejected = store.reject(created.id)

    assert rejected.status == "rejected"


def test_approval_store_rejects_repeat_or_illegal_transitions() -> None:
    store = ApprovalStore()
    approved = store.approve(store.create("run command").id)
    rejected = store.reject(store.create("write file").id)

    with pytest.raises(ApprovalStateError, match="not pending"):
        store.approve(approved.id)
    with pytest.raises(ApprovalStateError, match="not pending"):
        store.approve(rejected.id)
    with pytest.raises(ApprovalStateError, match="not pending"):
        store.reject(rejected.id)

import pytest


@pytest.fixture
def client():
    from safe_code_harness.api.main import create_app
    from fastapi.testclient import TestClient

    with TestClient(create_app()) as test_client:
        yield test_client


def test_fastapi_testclient_uses_the_declared_httpx_client() -> None:
    import httpx
    from fastapi.testclient import TestClient

    assert issubclass(TestClient, httpx.Client)


def _start_run(client, scenario: str) -> str:
    response = client.post("/api/runs", json={"scenario": scenario})

    assert response.status_code == 201
    return response.json()["id"]


def test_run_list_is_empty_before_any_runs_are_created(client) -> None:
    """Removing the empty-list route must make this test fail."""
    response = client.get("/api/runs")

    assert response.status_code == 200
    assert response.json() == []


def test_run_list_returns_creation_ordered_safe_summaries(client) -> None:
    """Returning events, paths, or non-creation order must make this test fail."""
    first_run_id = _start_run(client, "pending_write")
    second_run_id = _start_run(client, "secret_write")

    response = client.get("/api/runs")

    assert response.status_code == 200
    summaries = response.json()
    assert [summary["id"] for summary in summaries] == [first_run_id, second_run_id]
    assert [summary["scenario"] for summary in summaries] == ["pending_write", "secret_write"]
    assert [summary["status"] for summary in summaries] == ["waiting_approval", "blocked"]
    assert all(set(summary) == {"id", "scenario", "status", "updated_at"} for summary in summaries)
    assert all(isinstance(summary["updated_at"], str) and summary["updated_at"] for summary in summaries)
    rendered = repr(summaries).lower()
    assert "notes.txt" not in rendered
    assert "api_key" not in rendered
    assert "secret-value" not in rendered


def test_run_detail_preserves_existing_fields_and_includes_safe_metadata(client) -> None:
    """Omitting retained scenario or timestamps from a run must make this test fail."""
    run_id = _start_run(client, "pending_write")

    detail = client.get(f"/api/runs/{run_id}")

    assert detail.status_code == 200
    body = detail.json()
    assert body["id"] == run_id
    assert body["scenario"] == "pending_write"
    assert isinstance(body["created_at"], str) and body["created_at"]
    assert isinstance(body["updated_at"], str) and body["updated_at"]
    assert body["status"] == "waiting_approval"
    assert body["approval_id"]
    assert isinstance(body["events"], list)


def test_pending_write_only_runs_after_explicit_approval(client) -> None:
    """Removing the AgentLoop resume after approval must make this test fail."""
    run_id = _start_run(client, "pending_write")

    pending = client.get(f"/api/runs/{run_id}").json()
    assert pending["status"] == "waiting_approval"
    assert pending["approval_id"]
    assert all(event["kind"] != "tool_result" for event in pending["events"])

    approved = client.post(f"/api/runs/{run_id}/approvals/{pending['approval_id']}/approve")

    assert approved.status_code == 200
    completed = client.get(f"/api/runs/{run_id}").json()
    assert completed["status"] == "completed"
    assert [event["kind"] for event in completed["events"]].count("tool_result") == 1


def test_rejected_pending_write_never_runs_the_action(client) -> None:
    """Dispatching a rejected action would make this test fail."""
    run_id = _start_run(client, "pending_write")
    pending = client.get(f"/api/runs/{run_id}").json()

    rejected = client.post(f"/api/runs/{run_id}/approvals/{pending['approval_id']}/reject")

    assert rejected.status_code == 200
    blocked = client.get(f"/api/runs/{run_id}").json()
    assert blocked["status"] == "blocked"
    assert all(event["kind"] != "tool_result" for event in blocked["events"])


def test_unknown_run_returns_a_structured_404(client) -> None:
    response = client.get("/api/runs/missing-run")

    assert response.status_code == 404
    assert response.json() == {"code": "run_not_found", "message": "run not found"}


def test_unknown_approval_returns_a_structured_404(client) -> None:
    run_id = _start_run(client, "pending_write")

    response = client.post(f"/api/runs/{run_id}/approvals/missing-approval/approve")

    assert response.status_code == 404
    assert response.json() == {"code": "approval_not_found", "message": "approval not found"}


def test_repeat_approval_returns_a_safe_structured_error(client) -> None:
    run_id = _start_run(client, "pending_write")
    approval_id = client.get(f"/api/runs/{run_id}").json()["approval_id"]

    assert client.post(f"/api/runs/{run_id}/approvals/{approval_id}/approve").status_code == 200
    repeated = client.post(f"/api/runs/{run_id}/approvals/{approval_id}/approve")

    assert repeated.status_code == 409
    assert repeated.json() == {"code": "approval_not_pending", "message": "approval request is not pending"}


def test_run_events_are_json_serializable_and_redact_secret_values(client) -> None:
    secret_value = "secret-value"
    run_id = _start_run(client, "secret_write")

    response = client.get(f"/api/runs/{run_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "blocked"
    assert isinstance(body["events"], list)
    assert secret_value not in repr(body)
    assert "[REDACTED]" in repr(body)

from dataclasses import replace

import pytest

from safe_code_harness.core.agent_loop import RunEvent


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


def test_run_detail_preserves_existing_fields_and_projects_only_safe_timeline_fields(client) -> None:
    """Returning raw event content or omitting retained run metadata must make this test fail."""
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
    assert all(
        set(event) == {"type", "created_at", "level", "display_status", "summary_code"}
        for event in body["events"]
    )
    assert all(isinstance(event["created_at"], str) and event["created_at"] for event in body["events"])
    assert {event["summary_code"] for event in body["events"]} >= {
        "approval_pending",
        "unknown_governed_event",
    }


def test_pending_write_only_runs_after_explicit_approval(client) -> None:
    """Removing the AgentLoop resume after approval must make this test fail."""
    run_id = _start_run(client, "pending_write")

    pending = client.get(f"/api/runs/{run_id}").json()
    assert pending["status"] == "waiting_approval"
    assert pending["approval_id"]
    assert all(event["summary_code"] != "tool_succeeded" for event in pending["events"])

    approved = client.post(f"/api/runs/{run_id}/approvals/{pending['approval_id']}/approve")

    assert approved.status_code == 200
    completed = client.get(f"/api/runs/{run_id}").json()
    assert completed["status"] == "completed"
    assert [event["summary_code"] for event in completed["events"]].count("tool_succeeded") == 1
    assert "approval_approved" in [event["summary_code"] for event in completed["events"]]
    assert "run_finished" in [event["summary_code"] for event in completed["events"]]


def test_rejected_pending_write_never_runs_the_action(client) -> None:
    """Dispatching a rejected action would make this test fail."""
    run_id = _start_run(client, "pending_write")
    pending = client.get(f"/api/runs/{run_id}").json()

    rejected = client.post(f"/api/runs/{run_id}/approvals/{pending['approval_id']}/reject")

    assert rejected.status_code == 200
    blocked = client.get(f"/api/runs/{run_id}").json()
    assert blocked["status"] == "blocked"
    assert "approval_rejected" in [event["summary_code"] for event in blocked["events"]]
    assert all(event["summary_code"] != "tool_succeeded" for event in blocked["events"])


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


def test_run_timeline_uses_fixed_safe_mappings_and_never_leaks_raw_event_text(client) -> None:
    """Replacing fixed display values with event text must make this test fail."""
    run_id = _start_run(client, "secret_write")

    response = client.get(f"/api/runs/{run_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "blocked"
    timeline = body["events"]
    assert {
        "type": "rule_decision",
        "level": "blocked",
        "display_status": "规则已阻止操作",
        "summary_code": "rule_blocked",
    } in [{key: value for key, value in event.items() if key != "created_at"} for event in timeline]
    assert all(event["display_status"] != "[REDACTED]" for event in timeline)
    rendered = repr(body).lower()
    assert "notes.txt" not in rendered
    assert "api_key" not in rendered
    assert "secret-value" not in rendered
    assert "sk-proj-" not in rendered


def test_unknown_and_failed_tool_events_fail_closed_to_fixed_safe_timeline_entries(client) -> None:
    """Exposing event summary, failure, details, or tool output must make this test fail."""
    run_id = _start_run(client, "pending_write")
    service = client.app.state.run_service
    managed = service._runs[run_id]
    managed.state = replace(
        managed.state,
        events=(
            RunEvent("tool_result", 1, summary="D:/private/secret.txt", ok=False, failure="token=do-not-leak"),
            RunEvent("context", 2, summary="LLM action: API_KEY=do-not-leak"),
        ),
    )

    response = client.get(f"/api/runs/{run_id}")

    assert response.status_code == 200
    timeline = response.json()["events"]
    assert [
        {key: value for key, value in event.items() if key != "created_at"}
        for event in timeline
    ] == [
        {
            "type": "tool_result",
            "level": "error",
            "display_status": "工具执行失败",
            "summary_code": "tool_failed",
        },
        {
            "type": "unknown",
            "level": "warning",
            "display_status": "未知受治理事件",
            "summary_code": "unknown_governed_event",
        },
    ]
    rendered = repr(response.json()).lower()
    assert "private" not in rendered
    assert "secret.txt" not in rendered
    assert "api_key" not in rendered
    assert "do-not-leak" not in rendered

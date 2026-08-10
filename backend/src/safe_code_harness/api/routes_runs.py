from typing import Literal

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from safe_code_harness.api.run_service import (
    ApprovalNotFoundError,
    ApprovalNotPendingError,
    RunNotFoundError,
    RunService,
)
from safe_code_harness.config.local_planner import real_planner_enabled
from safe_code_harness.llm.openai_compatible import PlannerNotConfiguredError


router = APIRouter(prefix="/api/runs", tags=["runs"])


class CreateRunRequest(BaseModel):
    mode: Literal["mock", "real"] = "mock"
    scenario: Literal["pending_write", "secret_write"] | None = None
    task: str | None = None
    workspace_id: str | None = None


def _service(request: Request) -> RunService:
    return request.app.state.run_service


def _not_found(code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"code": code, "message": message})


@router.post("", status_code=status.HTTP_201_CREATED)
def create_run(payload: CreateRunRequest, request: Request) -> dict[str, object]:
    if payload.mode == "mock":
        if payload.scenario is None:
            raise HTTPException(status_code=422, detail="mock scenario is required")
        return _service(request).start(payload.scenario)

    if not real_planner_enabled():
        raise HTTPException(status_code=403, detail="local real Planner mode is disabled")
    if not payload.task or not payload.workspace_id:
        raise HTTPException(status_code=422, detail="task and workspace_id are required")
    try:
        workspace = request.app.state.workspace_registry.get(payload.workspace_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="workspace not found") from None
    try:
        llm = request.app.state.planner_configuration.create_llm()
        return _service(request).start_real(payload.task, workspace, llm)
    except PlannerNotConfiguredError:
        raise HTTPException(status_code=409, detail="Planner API key is not configured") from None


@router.get("")
def list_runs(request: Request) -> list[dict[str, object]]:
    return _service(request).list_summaries()


@router.get("/{run_id}", response_model=None)
def get_run(run_id: str, request: Request) -> dict[str, object] | JSONResponse:
    try:
        return _service(request).snapshot(run_id)
    except RunNotFoundError:
        return _not_found("run_not_found", "run not found")


@router.post("/{run_id}/approvals/{approval_id}/{decision}", response_model=None)
def decide_approval(
    run_id: str, approval_id: str, decision: Literal["approve", "reject"], request: Request
) -> dict[str, object] | JSONResponse:
    try:
        return _service(request).decide(run_id, approval_id, decision)
    except RunNotFoundError:
        return _not_found("run_not_found", "run not found")
    except ApprovalNotFoundError:
        return _not_found("approval_not_found", "approval not found")
    except ApprovalNotPendingError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"code": "approval_not_pending", "message": "approval request is not pending"},
        )

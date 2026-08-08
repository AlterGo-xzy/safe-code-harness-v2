from pathlib import Path

from fastapi import FastAPI

from safe_code_harness.api.routes_runs import router as runs_router
from safe_code_harness.api.run_service import RunService
from safe_code_harness.api.routes_workspaces import router as workspaces_router
from safe_code_harness.workspaces.registry import WorkspaceRegistry


def create_app() -> FastAPI:
    app = FastAPI(title="SafeCodeHarness API")
    app.state.run_service = RunService()
    app.state.workspace_registry = WorkspaceRegistry(Path.cwd() / "workspaces")
    app.include_router(runs_router)
    app.include_router(workspaces_router)
    return app


app = create_app()

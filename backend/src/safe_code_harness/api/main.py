from fastapi import FastAPI

from safe_code_harness.api.routes_runs import router as runs_router
from safe_code_harness.api.run_service import RunService


def create_app() -> FastAPI:
    app = FastAPI(title="SafeCodeHarness API")
    app.state.run_service = RunService()
    app.include_router(runs_router)
    return app


app = create_app()

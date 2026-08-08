from fastapi import FastAPI

from safe_code_harness.api.routes_config import PlannerConfiguration, router as config_router
from safe_code_harness.api.routes_runs import router as runs_router
from safe_code_harness.api.run_service import RunService
from safe_code_harness.config.secret_store import SecretStore


def create_app(secret_store: SecretStore | None = None) -> FastAPI:
    app = FastAPI(title="SafeCodeHarness API")
    app.state.run_service = RunService()
    app.state.planner_configuration = PlannerConfiguration(secret_store or SecretStore())
    app.include_router(runs_router)
    app.include_router(config_router)
    return app


app = create_app()

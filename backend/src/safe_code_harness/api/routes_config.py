from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, field_validator

from safe_code_harness.config.planner_settings import PlannerSettings
from safe_code_harness.config.secret_store import SecretStore, SecretStoreUnavailableError


router = APIRouter(prefix="/api/config/planner", tags=["config"])


class UpdatePlannerRequest(BaseModel):
    base_url: str
    model: str
    api_key: str

    @field_validator("base_url", "model", "api_key")
    @classmethod
    def require_non_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class PlannerConfiguration:
    def __init__(self, secret_store: SecretStore) -> None:
        self._secret_store = secret_store
        self._base_url = "https://api.openai.com/v1"
        self._model = "gpt-4o-mini"

    def snapshot(self) -> PlannerSettings:
        return PlannerSettings.from_secret(self._base_url, self._model, self._secret_store.get())

    def update(self, base_url: str, model: str, api_key: str) -> PlannerSettings:
        self._secret_store.set(api_key)
        self._base_url = base_url
        self._model = model
        return self.snapshot()

    def clear(self) -> PlannerSettings:
        self._secret_store.clear()
        return self.snapshot()


def _configuration(request: Request) -> PlannerConfiguration:
    return request.app.state.planner_configuration


def _response(settings: PlannerSettings) -> dict[str, str | bool | None]:
    return {
        "configured": settings.configured,
        "masked_suffix": settings.masked_suffix,
        "base_url": settings.base_url,
        "model": settings.model,
    }


def _unavailable() -> HTTPException:
    return HTTPException(status_code=503, detail="secure credential storage is unavailable")


@router.get("")
def get_planner(request: Request) -> dict[str, str | bool | None]:
    try:
        return _response(_configuration(request).snapshot())
    except SecretStoreUnavailableError as exc:
        raise _unavailable() from None


@router.put("")
def update_planner(payload: UpdatePlannerRequest, request: Request) -> dict[str, str | bool | None]:
    try:
        return _response(_configuration(request).update(payload.base_url, payload.model, payload.api_key))
    except SecretStoreUnavailableError as exc:
        raise _unavailable() from None


@router.delete("")
def clear_planner(request: Request) -> dict[str, str | bool | None]:
    try:
        return _response(_configuration(request).clear())
    except SecretStoreUnavailableError as exc:
        raise _unavailable() from None

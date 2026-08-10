from pathlib import Path


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_publish_workflow_targets_ghcr_and_never_reads_dotenv() -> None:
    workflow = _read(".github/workflows/publish-image.yml")

    assert "ghcr.io" in workflow
    assert ".env" not in workflow


def test_publish_workflow_is_default_branch_only_and_uses_package_permission() -> None:
    workflow = _read(".github/workflows/publish-image.yml")

    assert "github.event.repository.default_branch" in workflow
    assert "packages: write" in workflow
    assert "secrets.GITHUB_TOKEN" in workflow
    assert "push: true" in workflow


def test_publish_workflow_waits_for_successful_default_branch_push_ci() -> None:
    workflow = _read(".github/workflows/publish-image.yml")

    assert "workflow_run:" in workflow
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "github.event.workflow_run.event == 'push'" in workflow
    assert "github.event.workflow_run.head_branch == github.event.repository.default_branch" in workflow
    assert "ref: ${{ github.event.workflow_run.head_sha }}" in workflow


def test_github_push_ci_runs_core_e2e_and_container_checks() -> None:
    workflow = _read(".github/workflows/ci.yml")

    assert "push:" in workflow
    assert "pytest backend/tests" in workflow
    assert "npm.cmd test" in workflow
    assert "playwright install chromium" in workflow
    assert "npm.cmd run test:e2e" in workflow
    assert "docker build" in workflow


def test_gitlab_has_exact_unit_test_job_for_backend_and_frontend() -> None:
    pipeline = _read(".gitlab-ci.yml")

    assert "\nunit-test:\n" in f"\n{pipeline}"
    assert "pytest backend/tests" in pipeline
    assert "npm --prefix frontend test" in pipeline


def test_make_test_runs_backend_and_frontend_core_tests() -> None:
    makefile = _read("Makefile")
    readme = _read("README.md")

    assert "PYTHON ?= .venv/bin/python" in makefile
    assert "test: backend-test frontend-test" in makefile
    assert "pytest backend/tests" in makefile
    assert "--prefix frontend test" in makefile
    assert ".venv/bin/python -m uvicorn" in readme
    assert r".\.venv\Scripts\python.exe -m uvicorn" in readme
    assert r".venv\\Scripts\\python.exe" not in readme


def test_container_builds_webui_and_serves_it_from_fastapi_without_baked_key() -> None:
    dockerfile = _read("Dockerfile")
    lowered = dockerfile.lower()

    assert "as web-builder" in lowered
    assert "npm run build" in dockerfile
    assert "COPY --from=web-builder" in dockerfile
    assert "StaticFiles" in dockerfile
    assert 'app.mount("/"' in dockerfile
    assert "COPY .env" not in dockerfile
    assert "/app/.env" not in dockerfile
    assert "dotenv" not in lowered
    assert "ARG SAFE_CODE_HARNESS_PLANNER_API_KEY" not in dockerfile
    assert "ENV SAFE_CODE_HARNESS_PLANNER_API_KEY" not in dockerfile


def test_compose_builds_image_and_checks_runs_api_without_key_configuration() -> None:
    compose = _read("docker-compose.yml")
    readme = _read("README.md")

    assert "build:" in compose
    assert '"127.0.0.1:8000:8000"' in compose
    assert "healthcheck:" in compose
    assert "/api/runs" in compose
    assert ".env" not in compose
    assert "API_KEY" not in compose
    assert "-p 127.0.0.1:8000:8000" in readme
    assert "does not implement authentication" in readme
    assert "authentication and TLS gateway" in readme


def test_docker_context_excludes_root_and_nested_dotenv_variants() -> None:
    patterns = {
        line.strip()
        for line in _read(".dockerignore").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    assert {".env", ".env.*", "**/.env", "**/.env.*"} <= patterns

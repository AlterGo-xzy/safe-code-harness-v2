# SafeCodeHarness v2

SafeCodeHarness v2 is a self-implemented Coding Agent Harness: an LLM proposes a constrained action, while local code controls parsing, governance, approval, tool dispatch, feedback and stopping conditions.

## Local development

Prerequisites are Python 3.12 or newer and Node.js 20. Create a virtual environment, install the backend and install the locked frontend dependencies:

```sh
python -m venv .venv
.venv/bin/python -m pip install -e "backend[dev]"
npm --prefix frontend ci --ignore-scripts
```

On Windows, use `.venv\\Scripts\\python.exe` instead of `.venv/bin/python`. Run the API with `python -m uvicorn safe_code_harness.api.main:app --app-dir backend/src --host 127.0.0.1 --port 8000` and run `npm --prefix frontend run dev` in another terminal.

## Tests

On a Unix-like system with the dependencies above installed, the one-command core suite covers all backend tests and frontend unit tests:

```sh
make test
```

CI additionally runs the deterministic mechanism demos, the frontend production build, real Chromium E2E, and a Docker image build. Windows contributors can use `scripts/test.ps1` for the backend unit entrypoint and the commands below for the broader suites.

## Offline deterministic demonstrations

The three demonstrations use only deterministic local components. They do not call an LLM provider, configure credentials, access a network, mutate a project workspace, or expose temporary paths in their JSON output.

On a Unix-like system with Python available, run:

```sh
make demos
```

On Windows, after creating the Task 13 worktree-local Python environment, run:

```powershell
.\scripts\run_demos.ps1
```

They print one stable JSON value each, in this order:

1. The existing command guard blocks a destructive command.
2. The real harness loop receives failed-test feedback before its fixed mock LLM selects the repair action.
3. The real run service pauses for approval, records approval, and only then resumes execution.

These offline checks are mechanism demonstrations, not browser E2E, CI, container, or deployment evidence.

## Local browser E2E

After installing the backend development dependencies into the Task 13 worktree-local `.venv`, installing the frontend packages, and installing Playwright Chromium, run from `frontend`:

```powershell
npm.cmd run test:e2e
```

This command starts a real local FastAPI server and Vite UI, creates a deterministic run through the real API, approves it through the browser, and checks the final API state without route interception. The FastAPI E2E entrypoint injects an initially empty process-local credential store, so this test does not read or write Windows Credential Manager, use a real key, or call an external Planner. It is local E2E evidence only—not CI, container, deployment, or production credential-storage evidence.

## Container distribution

Build and run the OCI image with one command each:

```sh
docker build -t safe-code-harness-v2:local .
docker run --rm --name safe-code-harness -p 8000:8000 safe-code-harness-v2:local
```

Open `http://localhost:8000`. The image uses a multi-stage Node build and serves the compiled WebUI from the FastAPI process. The equivalent Compose command is `docker compose up --build`.

The default-branch publish workflow targets this GHCR package:

```sh
docker pull ghcr.io/altergo-xzy/safe-code-harness-v2:latest
docker run --rm -p 8000:8000 ghcr.io/altergo-xzy/safe-code-harness-v2:latest
```

These pull commands become usable only after the publish workflow has run and the GitHub package visibility is set to public. Package visibility is a repository-owner setting; it is not claimed as verified by the local Task 14 implementation.

## Planner key safety

The harness runs in deterministic offline mode without any external key. A native Windows source run stores an optional Planner key only in Windows Credential Manager and exposes only masked status through the API.

The Linux container keeps a key only in process memory. Entering it through the WebUI password control is the preferred local container flow; it is lost when the container restarts. A managed deployment may inject `SAFE_CODE_HARNESS_PLANNER_API_KEY` through its platform secret manager. Do not put a key literal in `docker run`, shell history, Compose YAML, an image build argument, or a committed `.env` file. Environment injection remains visible to sufficiently privileged host/container inspection, so a platform secret manager and HTTPS are required for a hosted instance. The image never bakes a key into a layer.

## CI/CD

`.github/workflows/ci.yml` runs tests on every push and pull request, installs Playwright Chromium, runs the real browser E2E, and builds the container image. `.github/workflows/publish-image.yml` uses the scoped GitHub token with `packages: write` only on the repository default branch. `.gitlab-ci.yml` supplies the required `unit-test` job for backend tests, demos, frontend tests and the frontend build on pushes and merge requests.

## Repository layout

- `backend/`: FastAPI API, the self-implemented harness, and deterministic tests.
- `frontend/`: React/Vite workbench, unit tests, and Playwright E2E.
- `scripts/`: repeatable offline mechanism demonstrations and Windows test helpers.
- `.github/workflows/` and `.gitlab-ci.yml`: CI and image publication definitions.
- `Dockerfile` and `docker-compose.yml`: OCI build and local container entrypoints.
- `SPEC.md`, `PLAN.md`, and the progress/log files: requirements and process evidence.

## Security boundaries and known limitations

- The LLM proposes actions; local parser, policy, path sandbox, command guard, approval state machine and dispatcher decide what executes.
- Core tests and demos use Mock/stub components and need no network or key.
- The container process-memory key store is deliberately non-persistent; Windows Credential Manager is unavailable inside the Linux image.
- The image is designed for port 8000 and runs as an unprivileged user with a writable temporary workspace. Compose also drops capabilities and uses a read-only root filesystem.
- The local build currently targets the Docker engine's selected architecture. Multi-architecture publication, an externally verified public GHCR pull, hosted HTTPS, and a public deployment URL remain Task 15 verification work.
- External GitHub Actions, GitLab CI, GHCR visibility and registry pull/run results are not local evidence and must be recorded only after those services actually run.

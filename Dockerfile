FROM node:20-alpine AS web-builder

WORKDIR /web
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --ignore-scripts
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SAFE_CODE_HARNESS_DEPLOYMENT=mock

WORKDIR /app
COPY backend/ /app/backend/
RUN python -m pip install --no-cache-dir /app/backend "uvicorn>=0.35,<1"
COPY --from=web-builder /web/dist /app/static

RUN printf '%s\n' \
    'import os' \
    'from fastapi.staticfiles import StaticFiles' \
    'from safe_code_harness.api.main import create_app' \
    '' \
    'class ProcessSecretStore:' \
    '    """Keep a container Planner key in memory only."""' \
    '    def __init__(self):' \
    '        self._secret = os.environ.get("SAFE_CODE_HARNESS_PLANNER_API_KEY") or None' \
    '    def set(self, secret):' \
    '        self._secret = secret' \
    '    def get(self):' \
    '        return self._secret' \
    '    def clear(self):' \
    '        self._secret = None' \
    '' \
    'app = create_app(ProcessSecretStore())' \
    'app.mount("/", StaticFiles(directory="/app/static", html=True), name="webui")' \
    > /app/container_app.py

RUN useradd --create-home --uid 10001 harness \
    && mkdir -p /app/workspaces \
    && chown -R harness:harness /app/workspaces

USER harness
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/runs', timeout=3)"

CMD ["python", "-m", "uvicorn", "container_app:app", "--host", "0.0.0.0", "--port", "8000"]

import { defineConfig } from "@playwright/test";

const apiBase = "http://127.0.0.1:8000";
const uiBase = "http://127.0.0.1:5173";

export default defineConfig({
  testDir: "./e2e",
  workers: 1,
  use: {
    baseURL: uiBase,
  },
  webServer: [
    {
      command: "..\\.venv\\Scripts\\python.exe -m uvicorn safe_code_harness.api.main:app --app-dir ..\\backend\\src --host 127.0.0.1 --port 8000",
      url: `${apiBase}/api/runs`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: "npm.cmd run dev -- --host 127.0.0.1 --port 5173",
      url: uiBase,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});

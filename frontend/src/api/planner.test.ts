import { afterEach, expect, it, vi } from "vitest";

import { clearPlanner, getPlanner, savePlanner } from "./planner";

const plannerOperations = [
  { method: "GET", run: () => getPlanner(), error: "无法加载 Planner 配置" },
  {
    method: "PUT",
    run: () => savePlanner({ baseUrl: "https://example.test/v1", model: "test-model", apiKey: "secret" }),
    error: "无法保存 Planner 配置",
  },
  { method: "DELETE", run: () => clearPlanner(), error: "无法清除 Planner 配置" },
] as const;

async function expectFixedPlannerError(run: () => Promise<unknown>, expected: string, leaked: string) {
  let caught: unknown;
  try {
    await run();
  } catch (error) {
    caught = error;
  }

  expect(caught).toBeInstanceOf(Error);
  expect((caught as Error).message).toBe(expected);
  expect((caught as Error).message).not.toContain(leaked);
}

afterEach(() => {
  vi.unstubAllGlobals();
});

it("projects Planner status without the submitted key", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
    configured: true, masked_suffix: "...1234", base_url: "https://example.test/v1", model: "test-model", api_key: "secret",
  }), { status: 200 })));
  await expect(getPlanner()).resolves.toEqual({ configured: true, maskedSuffix: "...1234", baseUrl: "https://example.test/v1", model: "test-model" });
});

it("sends a Planner key only in its update request body", async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({
    configured: true, masked_suffix: "...1234", base_url: "https://example.test/v1", model: "test-model", api_key: "secret",
  }), { status: 200 }));
  vi.stubGlobal("fetch", fetchMock);

  await expect(savePlanner({ baseUrl: "https://example.test/v1", model: "test-model", apiKey: "secret" })).resolves.toEqual({
    configured: true, maskedSuffix: "...1234", baseUrl: "https://example.test/v1", model: "test-model",
  });

  expect(fetchMock).toHaveBeenCalledWith("/api/config/planner", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ base_url: "https://example.test/v1", model: "test-model", api_key: "secret" }),
  });
});

it("rejects malformed Planner output with a fixed error", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ configured: true }), { status: 200 })));

  await expect(clearPlanner()).rejects.toThrow(/^无法清除 Planner 配置$/);
});

it.each(plannerOperations)("replaces a $method non-OK response body with its fixed error", async ({ run, error }) => {
  const leaked = "D:/private/response-body-secret";
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(leaked, { status: 500 })));

  await expectFixedPlannerError(run, error, leaked);
});

it.each(plannerOperations)("replaces a $method network rejection with its fixed error", async ({ run, error }) => {
  const leaked = "D:/private/network-rejection-secret";
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error(leaked)));

  await expectFixedPlannerError(run, error, leaked);
});

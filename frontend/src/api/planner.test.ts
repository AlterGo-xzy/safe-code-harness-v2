import { afterEach, expect, it, vi } from "vitest";

import { clearPlanner, getPlanner, savePlanner } from "./planner";

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

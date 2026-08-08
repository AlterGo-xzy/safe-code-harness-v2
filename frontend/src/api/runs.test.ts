import { afterEach, expect, it, vi } from "vitest";

import { getRun, listRuns } from "./runs";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("loads only the run summaries returned by the API", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([
    { id: "r-1", scenario: "pending_write", status: "waiting_approval", updated_at: "2026-08-08T10:00:00Z" },
  ]), { status: 200 })));
  await expect(listRuns()).resolves.toEqual([{ id: "r-1", scenario: "pending_write", status: "waiting_approval", updatedAt: "2026-08-08T10:00:00Z" }]);
});

it("rejects a non-success detail response without exposing its body", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("/private/path", { status: 500 })));
  await expect(getRun("r-1")).rejects.toThrow("无法加载运行详情");
});

it("returns only the allowed detail fields", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
    id: "r-1",
    scenario: "pending_write",
    status: "waiting_approval",
    events: [{ kind: "approval", step: 1, summary: "pending", action_type: "write_file", ok: null, failure: null }],
    approval_id: "private-approval-id",
  }), { status: 200 })));

  await expect(getRun("r-1")).resolves.toEqual({
    id: "r-1",
    scenario: "pending_write",
    status: "waiting_approval",
    events: [{ kind: "approval", step: 1, summary: "pending", actionType: "write_file", ok: null, failure: null }],
  });
});

it("rejects malformed list data", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "r-1" }), { status: 200 })));
  await expect(listRuns()).rejects.toThrow("无法加载运行列表");
});

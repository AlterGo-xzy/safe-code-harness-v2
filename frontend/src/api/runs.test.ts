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
    events: [{
      type: "approval",
      created_at: "2026-08-08T10:00:00Z",
      level: "warning",
      display_status: "需要审批",
      summary_code: "approval_pending",
      summary: "D:/private/API_KEY=do-not-leak",
      failure: "secret=do-not-leak",
    }],
    approval_id: "private-approval-id",
  }), { status: 200 })));

  await expect(getRun("r-1")).resolves.toEqual({
    id: "r-1",
    scenario: "pending_write",
    status: "waiting_approval",
    events: [{
      type: "approval",
      createdAt: "2026-08-08T10:00:00Z",
      level: "warning",
      displayStatus: "需要审批",
      summaryCode: "approval_pending",
    }],
    approvalId: "private-approval-id",
  });
});

it("keeps approval ID only for a waiting-approval detail", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
    id: "run-1", scenario: "pending_write", status: "waiting_approval",
    approval_id: "approval-1", events: [],
  }), { status: 200 })));
  await expect(getRun("run-1")).resolves.toMatchObject({ approvalId: "approval-1" });
});

it("never includes an approval ID for a completed detail", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
    id: "run-1", scenario: "pending_write", status: "completed",
    approval_id: "approval-1", events: [],
  }), { status: 200 })));
  await expect(getRun("run-1")).resolves.toMatchObject({ approvalId: null });
});

it("rejects malformed list data", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "r-1" }), { status: 200 })));
  await expect(listRuns()).rejects.toThrow("无法加载运行列表");
});

it("replaces a list fetch exception with the fixed Chinese error", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("D:/private/API_KEY=do-not-leak")));

  await expect(listRuns()).rejects.toThrow(/^无法加载运行列表$/);
});

it("replaces a detail JSON exception with the fixed Chinese error", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
    ok: true,
    json: vi.fn().mockRejectedValue(new Error("D:/private/secret.txt")),
  }));

  await expect(getRun("r-1")).rejects.toThrow(/^无法加载运行详情$/);
});

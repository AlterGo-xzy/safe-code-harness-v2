import { afterEach, expect, it, vi } from "vitest";

import { decideApproval } from "./approvals";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("rejects an approval error without exposing its body", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("/private/path", { status: 409 })));
  await expect(decideApproval("run-1", "approval-1", "approve")).rejects.toThrow("无法提交审批决定");
});

it("posts the encoded approval decision to the governed route", async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(null, { status: 204 }));
  vi.stubGlobal("fetch", fetchMock);

  await expect(decideApproval("run /1", "approval /1", "reject")).resolves.toBeUndefined();

  expect(fetchMock).toHaveBeenCalledWith(
    "/api/runs/run%20%2F1/approvals/approval%20%2F1/reject",
    { method: "POST" },
  );
});

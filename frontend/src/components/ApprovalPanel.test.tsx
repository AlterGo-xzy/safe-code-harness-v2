// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { decideApproval } from "../api/approvals";
import { ApprovalPanel } from "./ApprovalPanel";

vi.mock("../api/approvals", () => ({ decideApproval: vi.fn() }));

const mockedDecideApproval = vi.mocked(decideApproval);

afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});

describe("ApprovalPanel", () => {
  it("submits an approval once and then asks its parent to refresh", async () => {
    mockedDecideApproval.mockResolvedValue();
    const onResolved = vi.fn();
    render(<ApprovalPanel runId="run-1" approvalId="approval-1" onResolved={onResolved} />);

    fireEvent.click(screen.getByRole("button", { name: "批准" }));

    await waitFor(() => expect(mockedDecideApproval).toHaveBeenCalledWith("run-1", "approval-1", "approve"));
    expect(onResolved).toHaveBeenCalledOnce();
  });

  it("disables both decisions while its request is pending", () => {
    mockedDecideApproval.mockReturnValue(new Promise(() => {}));
    render(<ApprovalPanel runId="run-1" approvalId="approval-1" onResolved={vi.fn()} />);

    fireEvent.click(screen.getByRole("button", { name: "拒绝" }));

    expect(screen.getByRole("button", { name: "批准" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "拒绝" })).toBeDisabled();
  });
});

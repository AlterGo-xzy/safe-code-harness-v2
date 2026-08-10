// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";
import { decideApproval } from "./api/approvals";
import { getRun, listRuns } from "./api/runs";

vi.mock("./api/approvals", () => ({ decideApproval: vi.fn() }));
vi.mock("./api/runs", () => ({
  getRun: vi.fn(),
  listRuns: vi.fn(),
}));

const mockedGetRun = vi.mocked(getRun);
const mockedListRuns = vi.mocked(listRuns);
const mockedDecideApproval = vi.mocked(decideApproval);

const pendingWrite = {
  id: "r-1",
  scenario: "pending_write",
  status: "waiting_approval",
  updatedAt: "2026-08-08T10:00:00Z",
};

afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});

describe("App", () => {
  it("shows the fixed Chinese loading state while the run list is pending", () => {
    mockedListRuns.mockReturnValue(new Promise(() => {}));

    render(<App />);

    expect(screen.getByText("正在加载运行…")).toBeInTheDocument();
  });

  it("shows the fixed Chinese empty state when no runs are returned", async () => {
    mockedListRuns.mockResolvedValue([]);

    render(<App />);

    expect(await screen.findByText("暂无运行记录")).toBeInTheDocument();
  });

  it("shows the fixed Chinese error state when the run list fails", async () => {
    mockedListRuns.mockRejectedValue(new Error("network unavailable"));

    render(<App />);

    expect(await screen.findByText("无法加载运行列表")).toBeInTheDocument();
  });

  it("selects a run card and shows only its returned event data", async () => {
    const reviewRun = {
      id: "r-2",
      scenario: "review_patch",
      status: "completed",
      updatedAt: "2026-08-08T10:10:00Z",
    };
    mockedListRuns.mockResolvedValue([pendingWrite, reviewRun]);
    mockedGetRun.mockImplementation(async (runId) => runId === "r-1" ? {
      id: "r-1",
      scenario: "pending_write",
      status: "waiting_approval",
      approvalId: null,
      events: [{
        type: "approval",
        level: "warning",
        displayStatus: "等待审批",
        summaryCode: "approval_pending",
        createdAt: "2026-08-08T10:00:00Z",
      }],
    } : {
      id: "r-2",
      scenario: "review_patch",
      status: "completed",
      approvalId: null,
      events: [{
        type: "rule_decision",
        level: "block",
        displayStatus: "已阻止",
        summaryCode: "dangerous_command_blocked",
        createdAt: "2026-08-08T10:10:00Z",
      }],
    });

    render(<App />);

    await screen.findByText("approval_pending");
    screen.getByRole("button", { name: /运行 review_patch/ }).click();

    expect(await screen.findByText("dangerous_command_blocked")).toBeInTheDocument();
    expect(screen.queryByText("approval_pending")).not.toBeInTheDocument();
  });

  it("does not render detail whose id differs from the selected run", async () => {
    mockedListRuns.mockResolvedValue([pendingWrite]);
    mockedGetRun.mockResolvedValue({
      id: "r-stale",
      scenario: "stale_scenario",
      status: "completed",
      approvalId: null,
      events: [{
        type: "rule_decision",
        level: "block",
        displayStatus: "已阻止",
        summaryCode: "stale_detail_must_not_render",
        createdAt: "2026-08-08T09:00:00Z",
      }],
    });

    render(<App />);

    await waitFor(() => expect(mockedGetRun).toHaveBeenCalledWith("r-1"));
    expect(screen.queryByText("stale_detail_must_not_render")).not.toBeInTheDocument();
  });

  it("keeps the selected detail when requests resolve out of order", async () => {
    const reviewRun = {
      id: "r-2",
      scenario: "review_patch",
      status: "completed",
      updatedAt: "2026-08-08T10:10:00Z",
    };
    let resolveFirst!: (detail: Awaited<ReturnType<typeof getRun>>) => void;
    let resolveSecond!: (detail: Awaited<ReturnType<typeof getRun>>) => void;
    const first = new Promise<Awaited<ReturnType<typeof getRun>>>((resolve) => { resolveFirst = resolve; });
    const second = new Promise<Awaited<ReturnType<typeof getRun>>>((resolve) => { resolveSecond = resolve; });

    mockedListRuns.mockResolvedValue([pendingWrite, reviewRun]);
    mockedGetRun.mockImplementation((runId) => runId === "r-1" ? first : second);

    render(<App />);
    fireEvent.click(await screen.findByRole("button", { name: /运行 review_patch/ }));

    await act(async () => {
      resolveSecond({
        id: "r-2",
        scenario: "review_patch",
        status: "completed",
        approvalId: null,
        events: [{
          type: "rule_decision",
          level: "info",
          displayStatus: "已完成",
          summaryCode: "selected_detail",
          createdAt: "2026-08-08T10:10:00Z",
        }],
      });
    });
    expect(await screen.findByText("selected_detail")).toBeInTheDocument();

    await act(async () => {
      resolveFirst({
        id: "r-1",
        scenario: "pending_write",
        status: "waiting_approval",
        approvalId: null,
        events: [{
          type: "approval",
          level: "warning",
          displayStatus: "等待审批",
          summaryCode: "late_stale_detail",
          createdAt: "2026-08-08T10:00:00Z",
        }],
      });
    });

    expect(screen.getByText("selected_detail")).toBeInTheDocument();
    expect(screen.queryByText("late_stale_detail")).not.toBeInTheDocument();
  });

  it("renders approval controls only for a selected waiting-approval detail with an approval ID", async () => {
    mockedListRuns.mockResolvedValue([pendingWrite]);
    mockedGetRun.mockResolvedValue({
      id: "r-1",
      scenario: "pending_write",
      status: "completed",
      approvalId: "approval-1",
      events: [],
    });

    render(<App />);

    await waitFor(() => expect(mockedGetRun).toHaveBeenCalledWith("r-1"));
    expect(screen.queryByRole("button", { name: "批准" })).not.toBeInTheDocument();
  });

  it("reloads the selected run detail after a successful approval decision", async () => {
    mockedListRuns.mockResolvedValue([pendingWrite]);
    mockedDecideApproval.mockResolvedValue();
    mockedGetRun
      .mockResolvedValueOnce({
        id: "r-1",
        scenario: "pending_write",
        status: "waiting_approval",
        approvalId: "approval-1",
        events: [],
      })
      .mockResolvedValueOnce({
        id: "r-1",
        scenario: "pending_write",
        status: "completed",
        approvalId: null,
        events: [{
          type: "approval",
          level: "info",
          displayStatus: "已批准",
          summaryCode: "approval_resolved",
          createdAt: "2026-08-08T10:01:00Z",
        }],
      });

    render(<App />);
    fireEvent.click(await screen.findByRole("button", { name: "批准" }));

    await waitFor(() => expect(mockedGetRun).toHaveBeenCalledTimes(2));
    expect(await screen.findByText("approval_resolved")).toBeInTheDocument();
  });

  it("keeps a newly selected detail when an earlier approval finishes late", async () => {
    const reviewRun = {
      id: "r-2",
      scenario: "review_patch",
      status: "completed",
      updatedAt: "2026-08-08T10:10:00Z",
    };
    let resolveApproval!: () => void;
    let resolveReviewRun!: (detail: Awaited<ReturnType<typeof getRun>>) => void;
    const approval = new Promise<void>((resolve) => { resolveApproval = resolve; });
    const reviewDetail = new Promise<Awaited<ReturnType<typeof getRun>>>((resolve) => { resolveReviewRun = resolve; });

    mockedListRuns.mockResolvedValue([pendingWrite, reviewRun]);
    mockedDecideApproval.mockReturnValue(approval);
    mockedGetRun.mockImplementation((runId) => runId === "r-1" ? Promise.resolve({
      id: "r-1",
      scenario: "pending_write",
      status: "waiting_approval",
      approvalId: "approval-1",
      events: [],
    }) : reviewDetail);

    render(<App />);
    fireEvent.click(await screen.findByRole("button", { name: "批准" }));
    fireEvent.click(screen.getByRole("button", { name: /运行 review_patch/ }));
    await waitFor(() => expect(mockedGetRun).toHaveBeenLastCalledWith("r-2"));

    await act(async () => { resolveApproval(); });
    await act(async () => {
      resolveReviewRun({
        id: "r-2",
        scenario: "review_patch",
        status: "completed",
        approvalId: null,
        events: [{
          type: "rule_decision",
          level: "info",
          displayStatus: "已完成",
          summaryCode: "selected_after_late_approval",
          createdAt: "2026-08-08T10:10:00Z",
        }],
      });
    });

    expect(await screen.findByText("selected_after_late_approval")).toBeInTheDocument();
  });
});

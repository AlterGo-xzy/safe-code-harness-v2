// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { createRun } from "../api/runs";
import { RunLauncher } from "./RunLauncher";

vi.mock("../api/runs", () => ({ createRun: vi.fn() }));

afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});

describe("RunLauncher", () => {
  it("does not allow a real run until an uploaded workspace and a task are supplied", () => {
    render(<RunLauncher workspaceId={null} onStarted={vi.fn()} />);
    fireEvent.change(screen.getByLabelText("运行模式"), { target: { value: "real" } });
    expect(screen.getByText("请先上传本地项目 ZIP。")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "创建运行" })).toBeDisabled();
  });

  it("sends an explicit real-mode launch after user input", async () => {
    const onStarted = vi.fn();
    vi.mocked(createRun).mockResolvedValue({ id: "run-1", scenario: "local_real_planner", status: "waiting_approval", approvalId: "approval-1", events: [] });
    render(<RunLauncher workspaceId="workspace-1" onStarted={onStarted} />);
    fireEvent.change(screen.getByLabelText("运行模式"), { target: { value: "real" } });
    fireEvent.change(screen.getByLabelText("工作任务"), { target: { value: "read README" } });
    fireEvent.click(screen.getByRole("button", { name: "创建运行" }));
    await waitFor(() => expect(createRun).toHaveBeenCalledWith({ mode: "real", task: "read README", workspaceId: "workspace-1" }));
    expect(onStarted).toHaveBeenCalledWith(expect.objectContaining({ id: "run-1" }));
  });
});

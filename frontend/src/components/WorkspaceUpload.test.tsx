// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { uploadWorkspace } from "../api/workspaces";
import { WorkspaceUpload } from "./WorkspaceUpload";

vi.mock("../api/workspaces", () => ({ uploadWorkspace: vi.fn() }));

const mockedUploadWorkspace = vi.mocked(uploadWorkspace);

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.resetAllMocks();
});

describe("WorkspaceUpload", () => {
  it("shows only safe workspace metadata and does not write browser storage", async () => {
    const setItem = vi.spyOn(Storage.prototype, "setItem");
    mockedUploadWorkspace.mockResolvedValue({ id: "ws-1", fileCount: 3 });
    render(<WorkspaceUpload />);
    const file = new File(["zip"], "project.zip", { type: "application/zip" });

    fireEvent.change(screen.getByLabelText("项目 ZIP"), { target: { files: [file] } });
    fireEvent.click(screen.getByRole("button", { name: "上传工作区" }));

    await waitFor(() => expect(mockedUploadWorkspace).toHaveBeenCalledWith(file));
    expect(await screen.findByText("工作区 ws-1：3 个文件")).toBeInTheDocument();
    expect(setItem).not.toHaveBeenCalled();
  });

  it("keeps upload disabled until a ZIP file is selected", () => {
    render(<WorkspaceUpload />);

    expect(screen.getByRole("button", { name: "上传工作区" })).toBeDisabled();
    expect(screen.getByLabelText("项目 ZIP")).toHaveAttribute("accept", ".zip,application/zip");
  });
});

// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { clearPlanner, getPlanner, savePlanner } from "../api/planner";
import { PlannerSettings } from "./PlannerSettings";

vi.mock("../api/planner", () => ({
  clearPlanner: vi.fn(),
  getPlanner: vi.fn(),
  savePlanner: vi.fn(),
}));

const mockedClearPlanner = vi.mocked(clearPlanner);
const mockedGetPlanner = vi.mocked(getPlanner);
const mockedSavePlanner = vi.mocked(savePlanner);
const configuredPlanner = {
  configured: true,
  maskedSuffix: "...1234",
  baseUrl: "https://example.test/v1",
  model: "test",
};

afterEach(() => {
  cleanup();
  vi.resetAllMocks();
});

describe("PlannerSettings", () => {
  it("does not render or retain a Planner key after save", async () => {
    mockedGetPlanner.mockResolvedValue(configuredPlanner);
    mockedSavePlanner.mockResolvedValue(configuredPlanner);
    render(<PlannerSettings />);

    fireEvent.change(await screen.findByLabelText("API 密钥"), { target: { value: "secret-value" } });
    fireEvent.click(screen.getByRole("button", { name: "保存 Planner 配置" }));

    await waitFor(() => expect(mockedSavePlanner).toHaveBeenCalledWith({
      baseUrl: "https://example.test/v1", model: "test", apiKey: "secret-value",
    }));
    expect(screen.queryByDisplayValue("secret-value")).not.toBeInTheDocument();
    expect(screen.queryByText("secret-value")).not.toBeInTheDocument();
    expect(screen.getByText("…1234")).toBeInTheDocument();
  });

  it("clears the configured Planner status", async () => {
    mockedGetPlanner.mockResolvedValue(configuredPlanner);
    mockedClearPlanner.mockResolvedValue({ configured: false, maskedSuffix: null, baseUrl: "", model: "" });
    render(<PlannerSettings />);

    fireEvent.click(await screen.findByRole("button", { name: "清除 Planner 配置" }));

    await waitFor(() => expect(mockedClearPlanner).toHaveBeenCalledOnce());
    expect(screen.getByText("尚未配置")).toBeInTheDocument();
  });

  it("uses the fixed clear error without rendering the request error", async () => {
    mockedGetPlanner.mockResolvedValue(configuredPlanner);
    mockedClearPlanner.mockRejectedValue(new Error("private-clear-error"));
    render(<PlannerSettings />);

    fireEvent.click(await screen.findByRole("button", { name: "清除 Planner 配置" }));

    expect(await screen.findByText("无法清除 Planner 配置")).toBeInTheDocument();
    expect(screen.queryByText("private-clear-error")).not.toBeInTheDocument();
  });
});

// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
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
  it("shows a fixed loading message while the initial Planner request is pending", async () => {
    let resolveInitialLoad!: (settings: typeof configuredPlanner) => void;
    mockedGetPlanner.mockReturnValue(new Promise((resolve) => { resolveInitialLoad = resolve; }));
    render(<PlannerSettings />);

    expect(screen.getByText("正在加载 Planner 配置…")).toBeInTheDocument();

    await act(async () => { resolveInitialLoad(configuredPlanner); });
    expect(screen.queryByText("正在加载 Planner 配置…")).not.toBeInTheDocument();
  });

  it("disables Planner controls until the initial configuration is loaded", () => {
    mockedGetPlanner.mockReturnValue(new Promise(() => {}));
    render(<PlannerSettings />);

    expect(screen.getByRole("button", { name: "保存 Planner 配置" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "清除 Planner 配置" })).toBeDisabled();
  });

  it("does not render or retain a Planner key after save", async () => {
    mockedGetPlanner.mockResolvedValue(configuredPlanner);
    mockedSavePlanner.mockResolvedValue(configuredPlanner);
    render(<PlannerSettings />);

    await screen.findByDisplayValue("https://example.test/v1");
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

  it("saves a Planner configuration after the initial load completes", async () => {
    let resolveInitialLoad!: (settings: typeof configuredPlanner) => void;
    const initialLoad = new Promise<typeof configuredPlanner>((resolve) => { resolveInitialLoad = resolve; });
    const savedPlanner = {
      configured: true,
      maskedSuffix: "...9876",
      baseUrl: "https://saved.example.test/v1",
      model: "saved-model",
    };
    mockedGetPlanner.mockReturnValue(initialLoad);
    mockedSavePlanner.mockResolvedValue(savedPlanner);
    render(<PlannerSettings />);

    await act(async () => { resolveInitialLoad(configuredPlanner); });
    fireEvent.change(screen.getByLabelText("Planner 地址"), { target: { value: savedPlanner.baseUrl } });
    fireEvent.change(screen.getByLabelText("模型"), { target: { value: savedPlanner.model } });
    fireEvent.click(screen.getByRole("button", { name: "保存 Planner 配置" }));
    await waitFor(() => expect(mockedSavePlanner).toHaveBeenCalledOnce());

    expect(screen.getByDisplayValue(savedPlanner.baseUrl)).toBeInTheDocument();
    expect(screen.getByDisplayValue(savedPlanner.model)).toBeInTheDocument();
    expect(screen.getByText("…9876")).toBeInTheDocument();
  });

  it("clears the password after a failed save without disclosing the request error", async () => {
    mockedGetPlanner.mockResolvedValue(configuredPlanner);
    mockedSavePlanner.mockRejectedValue(new Error("private-save-error"));
    render(<PlannerSettings />);

    fireEvent.change(await screen.findByLabelText("API 密钥"), { target: { value: "failed-secret" } });
    fireEvent.click(screen.getByRole("button", { name: "保存 Planner 配置" }));

    expect(await screen.findByText("无法保存 Planner 配置")).toBeInTheDocument();
    expect(screen.queryByDisplayValue("failed-secret")).not.toBeInTheDocument();
    expect(screen.queryByText("private-save-error")).not.toBeInTheDocument();
  });

  it.each([
    { button: "保存 Planner 配置", pending: mockedSavePlanner },
    { button: "清除 Planner 配置", pending: mockedClearPlanner },
  ])("disables every Planner control while $button is pending", async ({ button, pending }) => {
    mockedGetPlanner.mockResolvedValue(configuredPlanner);
    pending.mockReturnValue(new Promise(() => {}));
    render(<PlannerSettings />);

    fireEvent.click(await screen.findByRole("button", { name: button }));

    expect(screen.getByLabelText("Planner 地址")).toBeDisabled();
    expect(screen.getByLabelText("模型")).toBeDisabled();
    expect(screen.getByLabelText("API 密钥")).toBeDisabled();
    expect(screen.getByRole("button", { name: "保存 Planner 配置" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "清除 Planner 配置" })).toBeDisabled();
  });
});

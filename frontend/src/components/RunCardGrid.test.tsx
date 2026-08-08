// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { RunCardGrid } from "./RunCardGrid";

afterEach(cleanup);

describe("RunCardGrid", () => {
  it("names each run card with its scenario, status, and UTC update time", () => {
    render(<RunCardGrid
      runs={[{
        id: "r-1",
        scenario: "pending_write",
        status: "waiting_approval",
        updatedAt: "2026-08-08T10:00:00Z",
      }]}
      selectedRunId="r-1"
      onSelect={vi.fn()}
    />);

    expect(screen.getByRole("button", {
      name: "运行 pending_write，状态 waiting_approval，更新 2026-08-08 10:00 UTC",
    })).toBeInTheDocument();
  });
});

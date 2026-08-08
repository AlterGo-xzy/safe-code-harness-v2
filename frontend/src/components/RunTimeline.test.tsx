// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { RunTimeline } from "./RunTimeline";

afterEach(cleanup);

describe("RunTimeline", () => {
  it("renders a blocked rule decision in the Chinese event timeline", () => {
    render(<RunTimeline events={[{
      type: "rule_decision",
      level: "block",
      displayStatus: "已阻止",
      summaryCode: "dangerous_command_blocked",
      createdAt: "2026-08-08T10:00:00Z",
    }]} />);

    expect(screen.getByRole("list")).toBeInTheDocument();
    expect(screen.getByText("rule_decision")).toBeInTheDocument();
    expect(screen.getByText("已阻止")).toBeInTheDocument();
    expect(screen.getByText("dangerous_command_blocked")).toBeInTheDocument();
    expect(screen.getByText("2026-08-08 10:00")).toBeInTheDocument();
  });

  it("renders the waiting-approval status as text", () => {
    render(<RunTimeline events={[{
      type: "approval",
      level: "warning",
      displayStatus: "等待审批",
      summaryCode: "approval_pending",
      createdAt: "2026-08-08T10:05:00Z",
    }]} />);

    expect(screen.getByText("等待审批")).toBeInTheDocument();
  });
});

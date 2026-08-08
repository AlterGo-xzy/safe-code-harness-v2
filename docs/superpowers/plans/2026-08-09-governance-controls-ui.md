# Governance Controls UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the Chinese governed-run workbench with safe approval decisions, optional Planner configuration, and ZIP workspace upload controls backed only by the existing Task 8–10 APIs.

**Architecture:** Typed API modules own every response projection and use fixed Chinese errors. `App` keeps the selected run detail and only mounts `ApprovalPanel` when its safe `waiting_approval` detail includes an approval ID; Planner and upload panels are separate components with local transient form state. Policy editing is deliberately excluded because the current repository has no policy API.

**Tech Stack:** React 18, TypeScript, Vite, Vitest, Testing Library, jsdom, existing FastAPI Task 8–10 contracts.

## Global Constraints

- Work only in `D:\safe-code-harness-v2\.worktrees\t12-settings-approval-ui` on `codex/t12-settings-approval-ui`.
- Consume Task 8 `POST /api/runs/{run_id}/approvals/{approval_id}/approve|reject`, Task 9 `GET|PUT|DELETE /api/config/planner`, and Task 10 `POST /api/workspaces/upload-zip`; do not invent routes or mock successful persistence in production code.
- Preserve Task 11’s safe event projection: five event fields only. Add `approvalId` to `RunDetail` only when the returned status is `waiting_approval` and the response contains a string `approval_id`.
- Planner keys are password-input request data only: never render, retain after request completion, log, put in a URL, persist to browser storage, or interpolate into an error.
- Upload UI displays only returned `id` and `file_count`; never show a server filesystem path, write `localStorage`, dispatch workspace-selection events, or imply a current-run workspace switch.
- Do not implement policy read/edit, run creation, raw events, tool output, file display, external Planner calls, or browser persistence in this task. Policy API/UI stays a last extension.
- Tasks 1 and 2 do not read, copy, or consult legacy source. `D:\2026_summer_project\frontend\src\components\ConfigPanel.tsx`, `WorkspaceUploadPanel.tsx`, and `D:\2026_summer_project\backend\src\safe_code_harness\api\routes_config.py` are prospective future-extension references only, not Task 12 implementation guidance. Any future investigation still requires an equivalent failing test first and must exclude policy mutation, paths, `localStorage`, custom events, and full source copy.
- Never commit keys, `.env`, `node_modules`, build output, test caches, virtual environments, or SDD reports. Record actual RED/GREEN, review, legacy non-use, commits, and PR in process documents.

---

## File Structure

- `frontend/src/api/runs.ts`: extends the safe run detail projection with conditional `approvalId`.
- `frontend/src/api/approvals.ts`: fixed-error approval request client.
- `frontend/src/api/planner.ts`: public Planner settings projection and password-key PUT/clear calls.
- `frontend/src/api/workspaces.ts`: ZIP submission and two-field workspace result projection.
- `frontend/src/components/ApprovalPanel.tsx`: pending-only approve/reject controls.
- `frontend/src/components/PlannerSettings.tsx`: masked Planner status, transient password entry, update and clear actions.
- `frontend/src/components/WorkspaceUpload.tsx`: ZIP file picker and safe upload result display.
- `frontend/src/App.tsx`: mounts controls beneath the selected detail and refreshes detail after a successful decision.
- `frontend/src/**/*.test.tsx`, `frontend/src/api/*.test.ts`: API and UI regressions.
- `PROJECT_PROGRESS.md`, `PLAN.md`, `AGENT_LOG.md`, `REQUIREMENTS_TRACEABILITY.md`: truthful process evidence.

### Task 1: Build safe typed API boundaries and conditional approval detail

**Files:**
- Create: `frontend/src/api/approvals.ts`, `frontend/src/api/approvals.test.ts`, `frontend/src/api/planner.ts`, `frontend/src/api/planner.test.ts`, `frontend/src/api/workspaces.ts`, `frontend/src/api/workspaces.test.ts`
- Modify: `frontend/src/api/runs.ts`, `frontend/src/api/runs.test.ts`

**Interfaces:**
- Produces `RunDetail.approvalId: string | null`; `decideApproval(runId, approvalId, decision): Promise<void>`; `getPlanner(): Promise<PlannerSettings>`; `savePlanner(input: PlannerInput): Promise<PlannerSettings>`; `clearPlanner(): Promise<PlannerSettings>`; `uploadWorkspace(file: File): Promise<WorkspaceUploadResult>`.
- `PlannerSettings` is exactly `{ configured: boolean; maskedSuffix: string | null; baseUrl: string; model: string }`; `WorkspaceUploadResult` is exactly `{ id: string; fileCount: number }`.

- [ ] **Step 1: Write failing boundary tests**

```tsx
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

it("rejects an approval error without exposing its body", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("/private/path", { status: 409 })));
  await expect(decideApproval("run-1", "approval-1", "approve")).rejects.toThrow("无法提交审批决定");
});

it("projects Planner status without the submitted key", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
    configured: true, masked_suffix: "...1234", base_url: "https://example.test/v1", model: "test-model", api_key: "secret",
  }), { status: 200 })));
  await expect(getPlanner()).resolves.toEqual({ configured: true, maskedSuffix: "...1234", baseUrl: "https://example.test/v1", model: "test-model" });
});

it("projects upload output to ID and file count only", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "ws-1", file_count: 3, path: "/private/workspace" }), { status: 201 })));
  await expect(uploadWorkspace(new File(["zip"], "project.zip", { type: "application/zip" }))).resolves.toEqual({ id: "ws-1", fileCount: 3 });
});
```

- [ ] **Step 2: Run focused API tests and verify RED**

Run: `cd frontend; npm.cmd test -- --run src/api/runs.test.ts src/api/approvals.test.ts src/api/planner.test.ts src/api/workspaces.test.ts`

Expected: FAIL because the three API modules and conditional approval projection do not exist.

- [ ] **Step 3: Implement the smallest fixed-error clients**

```ts
export async function decideApproval(runId: string, approvalId: string, decision: "approve" | "reject"): Promise<void> {
  try {
    const response = await fetch(`/api/runs/${encodeURIComponent(runId)}/approvals/${encodeURIComponent(approvalId)}/${decision}`, { method: "POST" });
    if (!response.ok) throw new Error();
  } catch {
    throw new Error("无法提交审批决定");
  }
}

function toWorkspace(value: unknown): WorkspaceUploadResult {
  if (!isRecord(value) || typeof value.id !== "string" || typeof value.file_count !== "number") {
    throw new Error("无法上传工作区");
  }
  return { id: value.id, fileCount: value.file_count };
}
```

Keep API-key values only in `savePlanner`’s request body. `getPlanner`, save and clear must project only the four public settings fields; invalid payload and every HTTP/network error use fixed Chinese errors.

- [ ] **Step 4: Run focused API tests and verify GREEN**

Run: `cd frontend; npm.cmd test -- --run src/api/runs.test.ts src/api/approvals.test.ts src/api/planner.test.ts src/api/workspaces.test.ts`

Expected: PASS, including all projections and fixed-error assertions.

- [ ] **Step 5: Commit API boundary**

```powershell
git add frontend/src/api
git commit -m "feat: add governed controls API clients"
```

### Task 2: Add approval, Planner, and upload panels to the workbench

**Files:**
- Create: `frontend/src/components/ApprovalPanel.tsx`, `frontend/src/components/ApprovalPanel.test.tsx`, `frontend/src/components/PlannerSettings.tsx`, `frontend/src/components/PlannerSettings.test.tsx`, `frontend/src/components/WorkspaceUpload.tsx`, `frontend/src/components/WorkspaceUpload.test.tsx`
- Modify: `frontend/src/App.tsx`, `frontend/src/App.test.tsx`, `frontend/src/styles/app.css`

**Interfaces:**
- `ApprovalPanel({ runId, approvalId, onResolved })` renders decision buttons only for supplied IDs and calls `onResolved` after a successful request.
- `PlannerSettings()` loads `getPlanner` and shows the fixed `正在加载 Planner 配置…` message while that initial request is pending; it reads `apiKey` from an uncontrolled password-input ref only at submit time, sends `{ baseUrl, model, apiKey }` to `savePlanner`, and clears the input in `finally` without retaining the key in React state.
- `WorkspaceUpload()` accepts a selected ZIP, calls `uploadWorkspace`, and renders only its safe result.

- [ ] **Step 1: Write failing component tests**

```tsx
it("submits an approval once and then asks its parent to refresh", async () => {
  mockedDecideApproval.mockResolvedValue();
  const onResolved = vi.fn();
  render(<ApprovalPanel runId="run-1" approvalId="approval-1" onResolved={onResolved} />);
  await userEvent.click(screen.getByRole("button", { name: "批准" }));
  expect(mockedDecideApproval).toHaveBeenCalledWith("run-1", "approval-1", "approve");
  expect(onResolved).toHaveBeenCalledOnce();
});

it("does not render or retain a Planner key after save", async () => {
  mockedGetPlanner.mockResolvedValue({ configured: true, maskedSuffix: "...1234", baseUrl: "https://example.test/v1", model: "test" });
  mockedSavePlanner.mockResolvedValue({ configured: true, maskedSuffix: "...1234", baseUrl: "https://example.test/v1", model: "test" });
  render(<PlannerSettings />);
  await userEvent.type(await screen.findByLabelText("API 密钥"), "secret-value");
  await userEvent.click(screen.getByRole("button", { name: "保存 Planner 配置" }));
  expect(screen.queryByDisplayValue("secret-value")).not.toBeInTheDocument();
  expect(screen.queryByText("secret-value")).not.toBeInTheDocument();
  expect(screen.getByText("…1234")).toBeInTheDocument();
});

it("shows only safe workspace metadata and does not write browser storage", async () => {
  const setItem = vi.spyOn(Storage.prototype, "setItem");
  mockedUploadWorkspace.mockResolvedValue({ id: "ws-1", fileCount: 3 });
  render(<WorkspaceUpload />);
  await userEvent.upload(screen.getByLabelText("项目 ZIP"), new File(["zip"], "project.zip", { type: "application/zip" }));
  await userEvent.click(screen.getByRole("button", { name: "上传工作区" }));
  expect(await screen.findByText("工作区 ws-1：3 个文件")).toBeInTheDocument();
  expect(setItem).not.toHaveBeenCalled();
});
```

Add App regressions proving an approval panel appears only for a selected `waiting_approval` detail with `approvalId`, and a successful decision reloads that run detail.

- [ ] **Step 2: Run focused UI tests and verify RED**

Run: `cd frontend; npm.cmd test -- --run src/components/ApprovalPanel.test.tsx src/components/PlannerSettings.test.tsx src/components/WorkspaceUpload.test.tsx src/App.test.tsx`

Expected: FAIL because panels and their App composition are absent.

- [ ] **Step 3: Implement minimal accessible panels and App composition**

```tsx
{detail?.id === selectedRunId && detail.status === "waiting_approval" && detail.approvalId ? (
  <ApprovalPanel runId={detail.id} approvalId={detail.approvalId} onResolved={() => reloadRun(detail.id)} />
) : null}
```

Use `<label>` for all inputs and a `type="password"` API-key field with an uncontrolled `useRef<HTMLInputElement>`; read `.current.value` only inside the submit handler and set it to `""` in `finally`. While each mutation is pending, disable its own action controls. Planner and upload errors use fixed Chinese text; do not print caught error values. CSS may add panel grouping but must retain visible focus and Task 11’s narrow-layout safeguards.

- [ ] **Step 4: Run focused UI tests and verify GREEN**

Run: `cd frontend; npm.cmd test -- --run src/components/ApprovalPanel.test.tsx src/components/PlannerSettings.test.tsx src/components/WorkspaceUpload.test.tsx src/App.test.tsx`

Expected: PASS, including approval gating, key clearing, no storage, and safe metadata.

- [ ] **Step 5: Commit controls UI**

```powershell
git add frontend/src/App.tsx frontend/src/App.test.tsx frontend/src/components frontend/src/styles/app.css
git commit -m "feat: add governed controls panels"
```

### Task 3: Verify, review, and record Task 12 without policy expansion

**Files:**
- Modify: `PROJECT_PROGRESS.md`, `PLAN.md`, `AGENT_LOG.md`, `REQUIREMENTS_TRACEABILITY.md`

**Interfaces:**
- Consumes actual RED/GREEN outputs, exact old-file reference/adaptation scope, two-stage reviews, and final verification.
- Produces an accurate handoff, including that Task 12’s policy expansion and Task 13’s real API/browser verification remain unfinished.

- [ ] **Step 1: Run spec-compliance review**

Inspect the diff for the following invariants: no policy route/UI, no fake success, no raw event fields, no write operation without a documented Task 8–10 route, no key in JSX/state/error/URL, no localStorage, and no path display.

- [ ] **Step 2: Run code-quality and accessibility review**

Inspect labels, keyboard buttons, pending-state disabling, error/empty feedback, panel headings, App refresh after approval, file-type limitation, component boundaries, and stale-detail guard. For every Critical or Important finding, add a failing regression before fixing it.

- [ ] **Step 3: Run controller verification**

Run: `cd frontend; npm.cmd ci --ignore-scripts; npm.cmd test; npm.cmd run build`

Run: `git diff --check codex/t11-workbench-ui..HEAD`

Expected: clean dependency install, all tests and build PASS, diff check has no output. Scan changed tracked files for credential-like patterns and report only the count.

- [ ] **Step 4: Update evidence and commit**

Record exact RED/GREEN commands/counts, reviewers, safe contracts, legacy non-use and prospective-reference boundary, Task 12’s deliberately deferred policy extension, and unresolved Task 13 E2E. Do not enter a PR number until it exists.

```powershell
git add PROJECT_PROGRESS.md PLAN.md AGENT_LOG.md REQUIREMENTS_TRACEABILITY.md
git commit -m "docs: record task 12 verification"
```

- [ ] **Step 5: Finish the branch**

Run `finishing-a-development-branch`; present its integration choices. If the user selects PR, push `codex/t12-settings-approval-ui`, create a draft PR against `codex/t11-workbench-ui`, read back its state/base/head, and commit the real URL plus worktree retention decision.

## Self-Review

- Spec coverage: Task 1 owns every safe data projection; Task 2 owns all three approved interactions and their App integration; Task 3 enforces the review, evidence, and PR lifecycle. The deliberately deferred policy extension has no implementation task.
- Placeholder scan: every command, type, endpoint, failure condition, file, and commit boundary is concrete; no TBD/TODO or generic test instruction remains.
- Type consistency: Task 1 defines every API type used by Task 2. `approvalId` is conditional in `RunDetail`; panel props use the same camelCase names; only snake_case wire fields are read at the API boundary.

# Governed Run Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Chinese card-overview workbench that reads task 8's four-field run summaries and exposes a selected run's five-field safe event timeline.

**Architecture:** A typed `api/runs.ts` isolates all read-only HTTP calls and data normalization. `App` owns request and selection state, `RunCardGrid` renders selectable run summaries, and `RunTimeline` renders only events supplied by the selected API response. CSS implements the Open Design-informed, restrained visual hierarchy with responsive cards and a detail pane.

**Tech Stack:** React 18, TypeScript, Vite, Vitest, Testing Library, jsdom, CSS, npm lockfile.

## Global Constraints

- Work only in `D:\safe-code-harness-v2\.worktrees\t11-workbench-ui` on `codex/t11-workbench-ui`.
- Use Chinese for visible UI text and accessible names.
- Before reading or adapting any legacy frontend source, add and run the corresponding failing test in this repository; document exact legacy paths and adaptations.
- The UI calls only task 8 read endpoints in this task. It must not create/approve/reject runs, store Planner keys, create fake events, or infer a backend state.
- Treat the Open Design 0.18.1 installation/checksum note only as an unreproducible historical record because no artifact, asset URL, or exact digest remains; never invent a digest. Use the recorded skills/design-system/real-artifact principles without adding an Open Design runtime dependency.
- Never commit secrets, `.env`, `node_modules`, build output, virtual environments, test caches, or SDD artifacts.
- Require keyboard-accessible selection and text equivalents for all color-coded states. Keep the CSS responsive intent, but leave actual 320px browser verification to unfinished Task 13.

---

## File Structure

- `frontend/package.json` and `frontend/package-lock.json`: Vite, React, Vitest, Testing Library and jsdom scripts, declared dependencies and reproducible resolution.
- `frontend/vite.config.ts`: Vitest jsdom configuration.
- `frontend/index.html`: Vite mount document with Chinese language declaration.
- `frontend/src/main.tsx`: React entry point.
- `frontend/src/api/runs.ts`: typed, read-only run list/detail requests.
- `frontend/src/components/RunCardGrid.tsx`: keyboard-selectable run summary cards.
- `frontend/src/components/RunTimeline.tsx`: semantic event timeline.
- `frontend/src/App.tsx`: request, selection, loading, empty and error state composition.
- `frontend/src/styles/app.css`: responsive card-grid and timeline presentation.
- `frontend/src/test/setup.ts`: Testing Library matchers.
- `frontend/src/components/RunTimeline.test.tsx`: timeline event, block and waiting-approval tests.
- `frontend/src/App.test.tsx`: API loading, empty, failure and card-selection tests.

### Task 1: Create the typed, read-only frontend boundary and scaffold

**Files:**
- Create: `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/src/test/setup.ts`, `frontend/src/api/runs.ts`, `frontend/src/api/runs.test.ts`

**Interfaces:**
- Produces: `type RunSummary`, `type RunEvent`, `type RunDetail`, `listRuns(signal?: AbortSignal): Promise<RunSummary[]>`, `getRun(runId: string, signal?: AbortSignal): Promise<RunDetail>`.
- Consumes: task 8 `GET /api/runs` and `GET /api/runs/{run_id}` JSON only.

- [ ] **Step 1: Write the failing API-boundary tests**

```tsx
import { getRun, listRuns } from "./runs";

it("loads only the run summaries returned by the API", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([
    { id: "r-1", scenario: "pending_write", status: "waiting_approval", updated_at: "2026-08-08T10:00:00Z" },
  ]), { status: 200 }))));
  await expect(listRuns()).resolves.toEqual([{ id: "r-1", scenario: "pending_write", status: "waiting_approval", updatedAt: "2026-08-08T10:00:00Z" }]);
});

it("rejects a non-success detail response without exposing its body", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("/private/path", { status: 500 })));
  await expect(getRun("r-1")).rejects.toThrow("无法加载运行详情");
});
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `cd frontend; npm.cmd test -- --run src/api/runs.test.ts`

Expected: FAIL because the frontend project and `runs` module do not exist.

- [ ] **Step 3: Add the minimal Vite/Vitest scaffold and typed API client**

```ts
export async function listRuns(signal?: AbortSignal): Promise<RunSummary[]> {
  const response = await fetch("/api/runs", { signal });
  if (!response.ok) throw new Error("无法加载运行列表");
  return (await response.json()).map(toSummary);
}
```

Define `toSummary` to read only `id`, `scenario`, `status` and `updated_at`; throw `无法加载运行列表` for malformed data. `getRun` must similarly return only `{ id, scenario, status, events }` and throw the fixed Chinese message above without including response body text.

- [ ] **Step 4: Run focused API tests to verify they pass**

Run: `cd frontend; npm.cmd test -- --run src/api/runs.test.ts`

Expected: PASS.

- [ ] **Step 5: Commit the scaffold and API boundary**

```powershell
git add frontend
git commit -m "feat: add run workbench frontend scaffold"
```

### Task 2: Build card overview, selected timeline, and resilient UI states

**Files:**
- Create: `frontend/src/components/RunCardGrid.tsx`, `frontend/src/components/RunTimeline.tsx`, `frontend/src/components/RunTimeline.test.tsx`, `frontend/src/App.test.tsx`, `frontend/src/styles/app.css`
- Modify: `frontend/src/App.tsx`, `frontend/src/main.tsx`

**Interfaces:**
- Consumes: `RunSummary`, `RunDetail`, `RunEvent`, `listRuns`, `getRun` from `api/runs.ts`.
- Produces: `RunCardGrid({ runs, selectedRunId, onSelect })`, `RunTimeline({ events })`, `App()`.

- [ ] **Step 1: Write the failing component and state tests**

```tsx
it("renders a blocked rule decision in the Chinese event timeline", () => {
  render(<RunTimeline events={[{ type: "rule_decision", level: "block", displayStatus: "已阻止", summaryCode: "dangerous_command_blocked", createdAt: "2026-08-08T10:00:00Z" }]} />);
  expect(screen.getByText("dangerous_command_blocked")).toBeInTheDocument();
  expect(screen.getByText("已阻止")).toBeInTheDocument();
});

it("selects a run card and shows only its returned event data", async () => {
  render(<App />);
  await userEvent.click(await screen.findByRole("button", { name: /运行 pending_write/ }));
  expect(await screen.findByText("dangerous_command_blocked")).toBeInTheDocument();
});
```

Add separate tests that mock `listRuns` as `[]` (empty Chinese state), reject it (fixed error state), and resolve a delayed promise (loading state). Add a waiting-approval event assertion for `等待审批` text.

- [ ] **Step 2: Run focused UI tests to verify they fail**

Run: `cd frontend; npm.cmd test -- --run src/components/RunTimeline.test.tsx src/App.test.tsx`

Expected: FAIL because `App`, `RunCardGrid`, and `RunTimeline` do not exist.

- [ ] **Step 3: Implement the smallest accessible card and timeline components**

```tsx
export function RunCardGrid({ runs, selectedRunId, onSelect }: Props) {
  return <div className="run-card-grid" aria-label="运行列表">{runs.map((run) => (
    <button key={run.id} className="run-card" aria-pressed={run.id === selectedRunId}
      onClick={() => onSelect(run.id)}>{run.scenario}</button>
  ))}</div>;
}
```

`App` must call `listRuns` on mount, automatically select the first returned run, then call `getRun` only for the selected id. Render exact Chinese states `正在加载运行…`, `暂无运行记录`, and `无法加载运行列表`. `RunTimeline` must use a semantic list and show only the safe event type, UTC time, fixed summary code and fixed text status; `level` may affect auxiliary styling. Do not implement any mutation button or original-event text path.

- [ ] **Step 4: Implement responsive, text-first Open Design-informed styling**

```css
.workbench { display: grid; grid-template-columns: minmax(0, 1fr) minmax(20rem, 0.9fr); gap: 1rem; }
.run-card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: .75rem; }
@media (max-width: 44rem) { .workbench { grid-template-columns: 1fr; } }
```

Use neutral surfaces, consistent spacing, visible focus rings, `overflow-wrap:anywhere`, and labels in addition to status color. Record the CSS responsive rules, but do not claim a 320px browser result; Task 13 owns that verification.

- [ ] **Step 5: Run frontend verification**

Run: `cd frontend; npm.cmd test; npm.cmd run build`

Expected: both commands PASS.

- [ ] **Step 6: Commit the workbench UI**

```powershell
git add frontend
git commit -m "feat: add governed run workbench"
```

### Task 3: Review, document, and verify the task boundary

**Files:**
- Modify: `PROJECT_PROGRESS.md`, `PLAN.md`, `AGENT_LOG.md`, `REQUIREMENTS_TRACEABILITY.md`

**Interfaces:**
- Consumes: task 11 commits, actual RED/GREEN output, two-stage review findings, and the non-reproducible historical Open Design installation record.
- Produces: accurate process handoff and PR description evidence.

- [ ] **Step 1: Run spec-compliance review**

Inspect the diff for: API-only rendering; no approval/config/upload write path; no secret value or local storage; selected-card events originate from `getRun`; Chinese accessible states remain present.

- [ ] **Step 2: Run code-quality and visual review**

Inspect keyboard focus, `aria-pressed`, text equivalents for status, loading/error/empty transitions, and static CSS overflow controls. Record each Critical/Important issue; add a failing regression before every fix. Keep 320px browser evidence explicitly unfinished for Task 13.

- [ ] **Step 3: Run controller verification**

Run: `cd frontend; npm.cmd ci --ignore-scripts; npm.cmd test; npm.cmd run build; git diff --check 2de48a2..HEAD`

Expected: test and build PASS; diff command has no output. Scan changed-file credential patterns without printing matches.

- [ ] **Step 4: Update process evidence and commit it**

Record the Open Design historical version/source claim and its unreproducible checksum boundary without inventing a digest, plus design principles, legacy reuse boundary, RED/GREEN, review findings and final counts. Do not mark a PR number until it exists.

```powershell
git add PROJECT_PROGRESS.md PLAN.md AGENT_LOG.md REQUIREMENTS_TRACEABILITY.md
git commit -m "docs: record task 11 verification"
```

- [ ] **Step 5: Use finishing-a-development-branch and create the draft PR**

Push `codex/t11-workbench-ui`, create a draft PR to `codex/t08-api-runs`, read back its state/base/head, and commit the real PR URL and retention decision to process records.

## Self-Review

- Spec coverage: Task 1 creates only the read API boundary; Task 2 implements Chinese card overview, selected timeline, loading/empty/error, accessibility and responsive behavior; Task 3 enforces review, Open Design evidence and PR workflow.
- Placeholder scan: no TBD/TODO, undefined function, or generic test instruction remains.
- Type consistency: all UI data types and API functions originate in `api/runs.ts`; components consume those exact names.

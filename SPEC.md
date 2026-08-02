# SafeCodeHarness v2 Specification

## 1. Problem Statement

SafeCodeHarness v2 is a deployable coding-agent harness for developers who need to run bounded code-repair and code-audit workflows without delegating execution authority to an LLM. The product accepts an operator task and a controlled workspace, asks a replaceable action provider for one structured next action, and applies deterministic local governance before any tool can execute.

The project addresses the reliability gap between a model that can suggest a coding step and a system that can safely execute, verify, explain, and stop that step. It is a real operator tool rather than a demonstration wrapper: operators can inspect a run, configure policy, review pending changes, and use deterministic test feedback to drive a bounded repair loop.

Primary users are individual developers and evaluators who want inspectable local coding automation. The primary engineering contribution is governance: policy evaluation, sandboxing, and human approval are implemented as deterministic project code rather than prompt instructions.

## 2. User Stories

1. As a developer, I can start a repair run for a controlled workspace and see every proposed action and result.
2. As an operator, I can configure which tools are allowed and which commands or paths are blocked without editing Python source.
3. As an operator, I can inspect a pending command or file diff and explicitly approve or reject it before it changes the workspace.
4. As a developer, I can see a failed test result returned to the action provider and verify that the next mock action changes accordingly.
5. As an evaluator, I can run all core mechanism tests without network access or a real LLM key.
6. As a user of an optional OpenAI-compatible planner, I can enter, update, inspect the masked status of, and clear a provider key without the plaintext key appearing in Git, logs, API responses, or settings JSON.
7. As a hosted user, I can upload a safe zip workspace and run it in an isolated server-side workspace.

## 3. Functional Specification

### 3.1 Agent Loop

Input: operator task, controlled workspace, runtime policy, a maximum step count, and an injected `LLMClient`.

Behavior: build bounded context; request one JSON action; parse it; enforce configured tool permissions; audit it with deterministic rules; apply sandbox, command, and approval policy; dispatch only permitted actions; record events; convert the result into structured feedback; stop on finish, block, parse failure, rejected approval, or maximum steps.

Output: a persistent run summary plus an ordered event timeline. Invalid JSON, unknown tools, invalid arguments, disabled tools, tool errors, unsafe paths, and blocked commands are surfaced as structured events and feedback rather than silently ignored.

### 3.2 Action and Tool Protocol

Every action is a JSON object with `type`, object `args`, and optional short `thought`. Supported actions are `list_files`, `read_file`, `write_file`, `run_tests`, `run_command`, `remember`, and `finish`.

Tools have one responsibility each. File tools use the path sandbox. Test and shell tools use the controlled command policy. Memory tools validate keys and preserve bounded records. The dispatcher is the only execution entry point.

### 3.3 Governance and Human Approval

The governance module is the principal contribution. It resolves all paths before access, blocks workspace escapes and configured sensitive paths, normalizes commands before matching, blocks configured destructive patterns, and evaluates rules before dispatch.

Configured shell commands and file writes can require approval. A pending write exposes a unified diff without touching disk. A pending command exposes the normalized command. Approval executes the stored action through the same policy path; rejection terminates the run as blocked. Unclear or malformed actions fail closed.

### 3.4 Feedback and Memory

Feedback converts test exits, command results, parse failures, audit results, and guardrail results into concise structured records for the next action-provider call. A deterministic mock sequence must prove that a failed test produces feedback and changes the following action.

Memory stores small, validated operator or run notes and returns only task-relevant bounded entries in context. It is never a substitute for loading arbitrary workspace files.

### 3.5 API and WebUI

FastAPI exposes run lifecycle, timeline, approval, workspace, preflight, configuration, memory, and planner-setting endpoints. The API never bypasses the sandbox or policy layers.

The React WebUI is an operator console: create/resume runs, inspect filtered event timelines, browse permitted files, inspect diffs, approve/reject pending work, edit policy, inspect memory, and configure an optional Planner. It is not the security authority.

### 3.6 Workspaces and Upload

Local workspaces are explicit configuration. Hosted zip uploads extract only into isolated workspaces. Upload handling rejects non-zip archives, traversal paths, symbolic links, oversized archives, excessive file counts, and sensitive/generated entries such as `.git`, `.env`, `node_modules`, and caches.

## 4. Domain and Mechanism Design

The domain is controlled coding work. Its objective feedback signals are test exit status and failure output, command exit status, parser errors, local rule decisions, guardrail decisions, and approval outcomes. These signals are produced by project code, recorded in events, and converted into the next model-feedback message.

Dangerous actions are workspace escape, access to sensitive paths, destructive or remote-execution shell commands, unapproved file writes, and any attempt to persist or expose a secret-like value. The available tools are sandboxed file inspection/editing, a configured test runner, a controlled command runner, and bounded memory notes. Cross-session memory is limited to explicit notes, persisted policy, and workspace metadata; code context is loaded on demand from permitted paths.

Governance is the deep dimension. The rule evaluator, path sandbox, command guard, approval state machine, policy configuration, and event evidence are all deterministic code. They remain testable after the real action provider is removed and replaced with a mock sequence.

## 5. Non-Functional Requirements

- Core mechanism tests are deterministic, offline, and use mock/stub LLM clients.
- The product must not use a high-level agent framework or host-agent loop as its Harness runtime.
- No real credential may enter source, Git history, logs, terminal output, or plaintext settings files.
- Windows stores persisted optional Planner credentials in Windows Credential Manager. On platforms without an implemented secure store, persistent Planner credentials are disabled rather than falling back to plaintext.
- The event model makes policy, feedback, approval, and stop decisions observable.
- A normal API control operation completes within two seconds excluding a configured test or shell command. Test and shell actions have explicit configurable timeouts and report timeout failures as feedback.
- A failed optional Planner request, unavailable credential store, unavailable uploaded workspace, or failed tool action returns a clear event and leaves the run stopped or blocked rather than silently continuing.
- The WebUI remains usable on narrow and desktop screens, with iOS-inspired restrained visual treatment and minimal explanatory copy.
- All safety-sensitive decisions fail closed.

## 6. Architecture and Data Flow

```text
React WebUI -> FastAPI API -> Run Service -> AgentLoop
                                      |-> Context and Memory
                                      |-> LLMClient
                                      |-> Action Parser
                                      |-> Rule Evaluator and Guardrails
                                      |-> Tool Dispatcher
                                      |     |-> File Sandbox
                                      |     |-> Test and Command Runner
                                      |     |-> Memory Store
                                      |-> Feedback Evaluator and Event Log
```

The model can propose actions only. The project-owned parser, rule evaluator, guardrails, dispatcher, and approval state machine decide whether anything executes.

## 7. Data Model

- `Action`: `type`, `args`, `thought`.
- `ToolResult`: `ok`, `output`, `error`, `metadata`.
- `HarnessEvent`: event id, run id, step, type, title, detail, timestamp, payload.
- `RunState`: run id, task, workspace id, mode, status, step count, pending action, final result.
- `RuntimePolicy`: allowed tools, blocked paths, blocked command fragments, approval-required tools, test command, maximum steps.
- `Workspace`: id, root path, origin, created time, size constraints.
- `PlannerSettings`: provider base URL, model, credential configured state, credential store label; no plaintext API key field.

## 8. Credentials and Distribution

The default offline mode needs no external key. The optional Planner setup supports first-use hidden entry, masked status, update, and clear. Windows uses Credential Manager. Non-Windows persistent storage remains unavailable until a platform secure-store adapter is implemented.

Distribution is a public OCI image at GitHub Container Registry. `docker build` and `docker run` must work locally, while the README provides public `docker pull` and run commands, security configuration, supported platforms, and known limitations. GitHub Actions builds, tests, runs browser E2E, and publishes the image. A Render deployment uses the same image and exposes a public WebUI.

## 9. Technology Choices

- Python and FastAPI: explicit, testable Harness mechanics and a compact API.
- React, TypeScript, and Vite: responsive operator console with tested client behavior.
- Pytest, Vitest, and Playwright: deterministic unit/integration/browser verification.
- Docker/OCI and GHCR: repeatable distribution.
- Windows Credential Manager: native secure storage for the target Windows development platform.
- Design system: Open Design is the visual reference and implementation skill to be applied during WebUI work. The UI will use its iOS-style patterns while retaining a dense operational console layout.

## 10. Acceptance Criteria

- `make test`, frontend tests, frontend production build, and Playwright E2E pass from a clean checkout.
- Mock LLM tests prove path/command blocking, feedback-driven action changes, memory behavior, tool dispatch, stop behavior, and approval transitions without network access.
- Mechanism demonstrations deterministically show a dangerous-action block, failed-test feedback changing the next action, and the governance approval state machine.
- API routes cannot bypass file sandboxing or policy.
- A pending write does not modify the file before approval and shows its exact diff.
- Planner key APIs never return plaintext and Windows persistence is visible in Credential Manager, not Git-tracked files.
- CI passes on the final commit; the public image can be pulled and started; the public WebUI is reachable.
- Every implementation task has a worktree, PR, red-green test record, two-stage review, `PLAN.md` update, and `AGENT_LOG.md` entry.

## 11. Risks and Open Questions

- A different-type cold-start agent may not be available in the current environment. The project must pause before implementation until this is resolved without misrepresenting a same-type subagent as independent evidence.
- External Planner providers may return malformed or unsafe actions; local governance remains mandatory and fail-closed.
- Hosted environments have filesystem and secret-store limits; unavailable secure credential storage disables persistent Planner credentials.
- Docker registry visibility and public deployment are external-state checks and cannot be claimed until independently verified.

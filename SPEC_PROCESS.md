# Specification Process

## Process Boundary

This repository starts as a clean rebuild. The previous `safe-code-harness` repository is a read-only technical reference, not a source of imported implementation history. No production Harness source is committed before this specification, the implementation plan, and an independent cold-start validation are complete.

## Brainstorming Record

### Iteration 1: Repository and Product Boundary

Question: should the final submission keep the original repository history or begin a clean rebuild?

Decision: create the separate public repository `AlterGo-xzy/safe-code-harness-v2`. The original project remains available as technical reference only. This prevents the new repository from claiming old implementation history as evidence of the required workflow.

### Iteration 2: Product Form

Question: should the rebuild be a CLI-only Harness or retain a deployable WebUI?

Decision: retain the FastAPI API and React operator WebUI. The WebUI is a real inspection and approval surface, while the project-owned Harness core remains the grading and safety focus.

### Iteration 3: Reuse Policy

Question: may existing code be reused to reduce unnecessary work?

Decision: source may be consulted module by module only after the new repository has a failing test for the behavior. Each reuse is recorded in the task PR and `AGENT_LOG.md`, including what was rewritten and why. No bulk copy or untraceable migration is permitted.

### Iteration 4: Core Contribution

Question: which Harness dimension should receive the deepest engineering treatment?

Decision: deterministic governance. Rules, sandboxes, policy gates, file-diff approval, command approval, event logs, and fail-closed behavior will be implemented as code and tested without a live model.

### Iteration 5: Delivery Boundary

Question: how should the project be distributable and how are keys handled?

Decision: Docker/OCI distributed through public GHCR plus a public WebUI deployment. The default mode needs no key. Optional Planner credentials use Windows Credential Manager on Windows; no plaintext non-Windows fallback is allowed.

## Accepted Constraints

- Follow the official Superpowers sequence: brainstorming, writing-plans, worktrees, subagent-driven development, TDD, code review, and branch finishing.
- Do not write Harness implementation code before a different-type cold-start agent validates `SPEC.md` and `PLAN.md` without prior conversation context.
- Keep `REFLECTION.md` student-authored; it is intentionally absent until the student writes it.
- Record only actions that actually occur. Do not backdate workflow evidence or claim external CI, registry, or deployment state without verification.

## Cold-Start Protocol (Prepared, Not Yet Executed)

The cold-start agent must be a different agent type in a fresh session with no imported memory or main-agent transcript. It receives only `SPEC.md` and `PLAN.md`, selects one or two explicitly named tasks, and pauses to ask when requirements are ambiguous rather than guessing.

This document will record the exact agent type, prompt, observed questions, output, document defects found, and before/after revisions after execution.

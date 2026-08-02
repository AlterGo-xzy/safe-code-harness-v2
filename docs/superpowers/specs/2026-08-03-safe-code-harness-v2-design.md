# SafeCodeHarness v2 Design

This design is the approved outcome of brainstorming for a clean, workflow-auditable rebuild of SafeCodeHarness.

The product is a deployable coding-agent Harness with a React operator console and a Python/FastAPI backend. Its model interface proposes structured actions only; deterministic project code owns parsing, tools, policy, sandboxing, feedback, approval, memory, and stop conditions.

The primary contribution is governance. Every potentially external action is inspected by local rules and guardrails before dispatch. Dangerous commands and unsafe paths are blocked; configured writes and commands pause for human approval with visible diffs or normalized command previews.

The rebuild treats the existing project as a read-only reference. Each reused behavior begins in this repository with a failing test and is reimplemented or adapted in an isolated task worktree. The corresponding PR documents the reference area and human changes.

The build sequence is non-negotiable: specification, detailed plan, different-type cold-start validation, then one task at a time through worktree, fresh subagent, TDD, two-stage review, and PR. CI, public GHCR distribution, and public deployment are verified rather than asserted.

# SafeCodeHarness v2

SafeCodeHarness v2 is a self-implemented Coding Agent Harness: an LLM proposes a constrained action, while local code controls parsing, governance, approval, tool dispatch, feedback and stopping conditions.

## Offline deterministic demonstrations

The three demonstrations use only deterministic local components. They do not call an LLM provider, configure credentials, access a network, mutate a project workspace, or expose temporary paths in their JSON output.

On a Unix-like system with Python available, run:

```sh
make demos
```

On Windows, after creating the Task 13 worktree-local Python environment, run:

```powershell
.\scripts\run_demos.ps1
```

They print one stable JSON value each, in this order:

1. The existing command guard blocks a destructive command.
2. The real harness loop receives failed-test feedback before its fixed mock LLM selects the repair action.
3. The real run service pauses for approval, records approval, and only then resumes execution.

These offline checks are mechanism demonstrations, not browser E2E, CI, container, or deployment evidence.

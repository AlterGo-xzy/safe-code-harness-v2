$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Task 13 local Python environment is missing. Create .venv in this worktree before running demos."
}

& $python (Join-Path $PSScriptRoot "run_guardrail_demo.py")
& $python (Join-Path $PSScriptRoot "run_feedback_demo.py")
& $python (Join-Path $PSScriptRoot "run_approval_demo.py")

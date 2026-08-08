param(
    [string]$PythonExecutable,
    [string[]]$DemoScripts
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $PythonExecutable) {
    $PythonExecutable = Join-Path $projectRoot ".venv\Scripts\python.exe"
}
if (-not (Test-Path -LiteralPath $PythonExecutable)) {
    throw "Task 13 local Python environment is missing. Create .venv in this worktree before running demos."
}
if (-not $DemoScripts) {
    $DemoScripts = @(
        (Join-Path $PSScriptRoot "run_guardrail_demo.py"),
        (Join-Path $PSScriptRoot "run_feedback_demo.py"),
        (Join-Path $PSScriptRoot "run_approval_demo.py")
    )
}

foreach ($demoScript in $DemoScripts) {
    & $PythonExecutable $demoScript
    if ($LASTEXITCODE -ne 0) {
        throw "A deterministic demo failed."
    }
}

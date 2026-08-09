# SafeCodeHarness v2 — 续开发交接（2026-08-10）

## 交接结论

代码和过程证据已保存到 Git；Task 13 Task 2 已闭环，Task 3 实现已提交 `e18422e`。真实 FastAPI/Vite/Chromium E2E 当前 `2 passed`，包含浏览器批准闭环和 320px 证据。**下一步必须先完成 Task 3 的独立 spec/security 与代码质量审查；审查闭环后才可进入 Task 4。仍不得开始任务 14、15 或策略扩展。**

本文件是给全新模型的最短可执行入口。开始工作前仍须依次阅读 `PROJECT_PROGRESS.md`、`AGENTS.md`、`PLAN.md`、`REQUIREMENTS_TRACEABILITY.md`、`AGENT_LOG.md`，并先运行 `git status --short`。

## 精确仓库状态

- 仓库：`D:\safe-code-harness-v2`；公开远程：`https://github.com/AlterGo-xzy/safe-code-harness-v2`。
- 当前工作目录：`D:\safe-code-harness-v2\.worktrees\t13-demos-e2e`。
- 当前分支：`codex/t13-demos-e2e`；Task 3 实现提交为 `e18422e test: add real workbench e2e coverage`。接手时必须以 `git rev-parse HEAD` 获取实际当前 HEAD。
- 已核验：在本交接文档创建前，`git status --short` 无输出；没有需要保留的已跟踪用户改动。
- Task 13 尚未推送、尚未创建 PR #13。不要假称已有 PR。
- Task 1-12 的 stacked draft PR #1-#12 已存在且尚未合并；Task 13 以 Task 12 分支为基线。
- `.venv` 和 `.superpowers/sdd` 位于本 Task 13 worktree、均为忽略项，不能提交。计划中的 `..\.venv` 不存在；本 worktree 本地 `.venv\Scripts\python.exe` 是已实际使用的解释器。

## 已完成并已保存的内容

### 任务 1-12

Harness 内核、治理、工具、反馈/记忆、主循环、运行/审批 API、安全 Planner 配置、安全 ZIP 上传、只读工作台，以及审批/Planner/上传安全 UI 均已经完成并有各自分支、提交、测试和 draft PR。精确历史与每项边界见 `PROJECT_PROGRESS.md` 的“后续执行顺序”及 `PLAN.md`。

关键用户决定仍有效：

- 旧项目 `D:\2026_summer_project` 的代码只可在本仓库先写同等行为的失败测试后，按模块最小迁入/改写；每次必须记录旧路径、范围和人工调整。Task 13 Task 1-2 **未使用旧项目代码**。
- 不配置真实 OpenAI-compatible API key；不得读取、输出、提交或访问真实 key。
- 策略扩展被用户明确推迟到最后；当前不得新增 policy API/UI、假保存或 workspace 切换。
- UI 不得新增 create-run UI、localStorage、原始事件/工具输出/路径展示。

### Task 13 Task 1：真实 API 合并 — 完成且独立审查通过

- 合并提交：`ec613df`（Task 9）、`1664aa2`（Task 10）。
- 集成提交：`fd38e6a feat: integrate planner and workspace APIs`、`fbad783 docs: record task 13 API integration evidence`。
- `create_app(secret_store: SecretStore | None = None)` 现在初始化并注册 Task 8 runs、Task 9 Planner、Task 10 workspaces 三个服务/路由。
- TDD 证据：合并前新增集成测试因 `create_app` 不接受 `secret_store` 预期 RED；随后 focused `1 passed`、完整 `backend/tests` `146 passed, 1 warning`。
- 独立只读审查 PASS（Critical/Important/Minor 全为 0）；Task 9 凭据安全和 Task 10 ZIP 安全源/测试相对其 reviewed branch 无 diff。

### Task 13 Task 2：离线机制演示 — 已完成并审查通过

已提交实现：

- `26f9855 test: add deterministic mechanism demos`
- `b2b7e15 docs: record task 13 demo evidence`
- `7243dfc fix: harden deterministic demo evidence`
- `7bf3d04 docs: record task 13 demo review fixes`
- `7bdd85d fix: reject tool results before approval`
- `1dbcf55 docs: record task 13 approval-boundary fix`

涉及文件：

- `scripts/run_guardrail_demo.py`：调用现有 `CommandGuard`/`RuntimePolicy`，投影危险命令被阻止的稳定 JSON。
- `scripts/run_feedback_demo.py`：调用现有 `AgentLoop`、`MockLLM`、反馈和临时目录，证明失败测试反馈改变下一动作。
- `scripts/run_approval_demo.py`：调用真实 `RunService`/审批恢复并从 snapshots 投影转录。
- `scripts/run_demos.ps1`：Windows 入口；`Makefile` 只提供 Unix-like `demos` target，未在 Windows 假称运行。
- `backend/tests/integration/test_demos.py`：函数与 subprocess JSON 安全测试。
- 根 `README.md`：仅说明离线 demos，未把它们写成 E2E/CI/部署证据。

已验证、可如实引用的结果：

- 初始 RED：缺少 demo 模块时 `ModuleNotFoundError: scripts.run_approval_demo`。
- 历史初次 GREEN：`test_demos.py` `6 passed in 0.23s`；历史修复后的 focused suite `10 passed in 0.47s`。
- 正常 `./scripts/run_demos.ps1`（PowerShell 写法为 `.\scripts\run_demos.ps1`）输出三段稳定 JSON。
- 历史修复后的完整 `backend/tests`：`156 passed, 1 warning`；warning 是既有 Starlette/TestClient 弃用提示。
- 当前第二次复审修复后的 demo suite：`12 passed in 0.46s`；当前完整 `backend/tests`：`158 passed, 1 warning`，warning 同为既有 Starlette/TestClient 弃用提示。
- `git diff --check` 无输出；已变更文件的高置信凭据候选计数为 `0`。

## Task 13 Task 2：已完成并验证

第二次只读独立复审结论为 Critical 0、Important 1、Minor 2，三项均已修复：`7bdd85d` 的真实 snapshot 投影会拒绝 waiting 或最终批准前的 `tool_succeeded`、`tool_failed`；PowerShell 回归已证明 failing first child 后的写 marker later child 不运行；四份过程文档已记录真实验证。随后第三次独立审查发现交接与部分过程文档仍未同步；文档提交 `5bf57a3` 后的 scoped re-review 已批准，Critical/Important/Minor 均为 0。

Task 2 已登记完成。不得重做已关闭的 `tool_failed` 或 later-child 行为修复；Task 3 实现状态与下一步审查要求见下节。若后续审查发现新的 Critical/Important，按 TDD/最小修复/复审处理。

## Task 13 Task 3：真实浏览器 E2E — 实现完成、审查待执行

- `frontend/e2e/workbench.spec.ts` 不拦截 API：API request 创建/核验真实 `pending_write`，page 实际点击中文“批准”。
- `frontend/playwright.config.ts` 以 `reuseExistingServer: false` 启动 t13 `.venv` 的 uvicorn 和 Vite；`frontend/vite.config.ts` 将 `/api` 代理到本地 FastAPI。
- `@playwright/test` 精确固定 1.62.1；Chromium 安装成功并由 `install --list` 确认。`backend[dev]` 增加 `uvicorn>=0.35,<1`，因为批准计划的启动命令直接依赖它。
- 当前验证：`npm.cmd run test:e2e` 2 passed；`npm.cmd test` 10 files/48 tests；`npm.cmd run build` 成功；backend 158 passed, 1 既有 warning。320x720 中批准按钮可见且 HTML/body 无横向溢出，因此未改 CSS。
- TDD 证据：初始缺 Playwright 命令 RED；真实 server 缺 uvicorn RED；Vitest 误收 E2E spec 的回归 RED。三项均有最小修复和 GREEN。npm audit 仍报告 3 moderate、1 high、1 critical，未执行破坏性 `--force` 修复。

## 随后工作顺序（不得提前）

1. Fresh read-only reviewer 对 `c44e5ec..HEAD` 做 Task 3 spec/security 审查，再单独做代码质量审查；重点检查真实 API、浏览器点击、执行证据、320px、端口/生命周期、依赖声明和安全 DTO 不变量。
2. 若有 Critical/Important，先写失败回归再最小修复并 scoped re-review；不得把 npm audit 的上游问题无条件 `--force` 升级。
3. 审查清零后，Task 13 最终 Task 4 执行 backend、三演示、干净 frontend install/unit/build/E2E、diff/凭据扫描；重新核对要求文件追踪；更新过程文件；使用 `finishing-a-development-branch` 决定推送和 draft PR #13。
4. Task 14（CI/容器分发）、Task 15（公网部署/最终交付）和延后的策略扩展都尚未开始。

## 严格流程与安全不变量

- 每个实现 task：独立 `codex/tNN-*` branch/worktree、新鲜 implementer、TDD（先 RED）、最小实现、spec/security review、quality review、真实记录、`finishing-a-development-branch`。
- 不提交 key、`.env`、虚拟环境、`node_modules`、`dist`、浏览器产物、测试缓存或 `.superpowers` 账本；不输出真实凭据或服务器/临时绝对路径。
- Harness 必须保持自实现主循环和确定性治理；不得引入 LangChain/AutoGen/CrewAI/LlamaIndex agent runner 或把宿主 agent/skill 当产品功能。
- Task 9 Planner 公共 DTO 始终只有安全字段，Credential Manager 异常不得泄露 key；Task 10 ZIP 路径/成员/大小/碰撞保护不得回退；Task 11/12 前端仍只使用安全 DTO。
- `REFLECTION.md` 必须由学生本人写作；AI 仅可协助大纲或润色。

## 有用命令

```powershell
Set-Location D:\safe-code-harness-v2\.worktrees\t13-demos-e2e
git status --short
.\.venv\Scripts\python.exe -m pytest backend\tests\integration\test_demos.py --basetemp .pytest-tmp\task13-demos -q
.\scripts\run_demos.ps1
.\.venv\Scripts\python.exe -m pytest backend\tests --basetemp .pytest-tmp\task13-backend -q
git diff --check codex/t12-settings-approval-ui..HEAD
```

PowerShell 环境中 `rg.exe` 曾出现“拒绝访问”；优先使用 `git grep` 或窄范围 `Get-Content`。所有文档/源码修改用 `apply_patch`，保留无关用户改动。

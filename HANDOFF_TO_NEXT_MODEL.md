# SafeCodeHarness v2 — 续开发交接（2026-08-10）

## 交接结论

代码和过程证据已保存到 Git；Task 13 Task 1-3、320px 修复及本地控制验证均已实现。视口 Important 已由 `5ed4bd3` 先 RED 后修复并通过 scoped 双阶段复审。随后最终全分支审查发现 E2E 仍启动生产 `main:app`，Planner 初始 GET 会触及 Windows Credential Manager；`7d66d98` 已以新的失败回归和 E2E-only 内存 SecretStore 入口完成最小修复，生产 app 未改。**最终 scoped re-review 结论为 Critical 0、Important 0、Minor 2；两个文档 Minor 已修正。仍不得假称已推送、已有 PR #13、CI/容器/部署完成或已开始任务 14、15/策略扩展；完成只读文档复核与最终 diff/凭据扫描后，才可运行 `finishing-a-development-branch`。**

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
- Task 2 第二次复审修复当时的 demo suite：`12 passed in 0.46s`；当时完整 `backend/tests`：`158 passed, 1 warning`，warning 同为既有 Starlette/TestClient 弃用提示。当前全仓库控制验证见后文的 `159 passed, 1 warning`。
- `git diff --check` 无输出；已变更文件的高置信凭据候选计数为 `0`。

## Task 13 Task 2：已完成并验证

第二次只读独立复审结论为 Critical 0、Important 1、Minor 2，三项均已修复：`7bdd85d` 的真实 snapshot 投影会拒绝 waiting 或最终批准前的 `tool_succeeded`、`tool_failed`；PowerShell 回归已证明 failing first child 后的写 marker later child 不运行；四份过程文档已记录真实验证。随后第三次独立审查发现交接与部分过程文档仍未同步；文档提交 `5bf57a3` 后的 scoped re-review 已批准，Critical/Important/Minor 均为 0。

Task 2 已登记完成。不得重做已关闭的 `tool_failed` 或 later-child 行为修复；Task 3 实现状态与下一步审查要求见下节。若后续审查发现新的 Critical/Important，按 TDD/最小修复/复审处理。

## Task 13 Task 3/4：真实浏览器 E2E 与最终隔离修复 — scoped re-review 已完成

- `frontend/e2e/workbench.spec.ts` 不拦截 API：API request 创建/核验真实 `pending_write`，page 实际点击中文“批准”。
- `frontend/playwright.config.ts` 以 `reuseExistingServer: false` 启动 t13 `.venv` 的 `safe_code_harness.api.e2e_app:app` 和 Vite；`frontend/vite.config.ts` 将 `/api` 代理到本地 FastAPI。专用 app 向现有 factory 注入初始为空的进程内 SecretStore，避免本地 E2E 读取/写入 Windows Credential Manager；生产 `main:app` 保持 Task 9 的真实存储边界。
- `@playwright/test` 精确固定 1.62.1；Chromium 安装成功并由 `install --list` 确认。`backend[dev]` 增加 `uvicorn>=0.35,<1`，因为批准计划的启动命令直接依赖它。
- 视口修复 TDD 证据：已有质量审查指出 `toBeVisible()` 不足；fresh implementer 先把 `expectFullyInsideViewport` 加入 320x720 E2E，得到真实 RED（底边 `1327.4375 > 720`），随后提交 `5ed4bd3 fix: keep mobile approval action in viewport`，仅将 `ApprovalPanel` 置于事件时间线之前。E2E 随后为 `2 passed`；未改变 API、政策、CSS、旧项目代码或安全 DTO。
- 最终隔离修复 TDD：运行时 probe 已证明默认 app 的 Planner GET 构造一次 Credential Manager；新增 `test_e2e_app.py` 后 focused RED 为缺少 `safe_code_harness.api.e2e_app`，`7d66d98` 后 focused GREEN `1 passed, 1 warning`，且断言精确空 DTO 与零 Credential Manager 构造。
- 当前本地控制验证（2026-08-10）：完整 backend `159 passed, 1 warning`（既有 Starlette/TestClient 弃用警告）；`scripts/run_demos.ps1` 输出三段稳定 JSON；clean `npm.cmd ci --ignore-scripts` 后前端 unit 为 `10 files/48 tests`、build 成功、真实 Chromium E2E 为 `2 passed`。install 仍报告 5 个上游审计风险（3 moderate、1 high、1 critical），未 force fix。
- 审查：Task 4 初始 spec/security review 为 C/I/M `0/0/0`；视口 quality Important 已由 `5ed4bd3` 修复并经 scoped 双阶段 re-review PASS。最终全分支修复的 scoped re-review 为 Critical 0、Important 0、Minor 2；两个 Minor（本文件的历史/当前测试数值措辞及追踪矩阵状态词）已在本次文档修正中关闭。

## 随后工作顺序（不得提前）

1. 不重做已关闭的 demo 或视口修复；最终 scoped re-review 已确认 E2E app 不触及 OS 凭据、Playwright 使用专用入口且生产 app 不变。先对本次两项文档 Minor 做只读复核，再完成最终 diff/凭据扫描。
2. 完成上述复核后，运行 `finishing-a-development-branch`，向用户呈现分支处置选择。仅在用户选择推送/PR 后，才可推送 `codex/t13-demos-e2e`、创建对 `codex/t12-settings-approval-ui` 的 draft PR #13、回读 GitHub 状态并提交实际 URL/保留 worktree 决定。
3. Task 14（CI/容器分发）、Task 15（公网部署/最终交付）和延后的策略扩展都尚未开始；不得把本地验证写成上述外部证据。

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
.\.venv\Scripts\python.exe -m pytest backend\tests\integration\test_e2e_app.py --basetemp .pytest-tmp\task13-e2e-app -q
.\scripts\run_demos.ps1
.\.venv\Scripts\python.exe -m pytest backend\tests --basetemp .pytest-tmp\task13-backend -q
Set-Location frontend
npm.cmd run test:e2e
Set-Location ..
git diff --check codex/t12-settings-approval-ui..HEAD
```

PowerShell 环境中 `rg.exe` 曾出现“拒绝访问”；优先使用 `git grep` 或窄范围 `Get-Content`。所有文档/源码修改用 `apply_patch`，保留无关用户改动。
## 2026-08-10 Task 13 分支收尾更新

Task 13 已推送，并创建目标为 `codex/t12-settings-approval-ui` 的 [draft PR #13](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/13)。保留本 worktree 和分支处理审查反馈；后续从 Task 14 开始，不得把 CI、分发、部署或策略扩展写成已完成。

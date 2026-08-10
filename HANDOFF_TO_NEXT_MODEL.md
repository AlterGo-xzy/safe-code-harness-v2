# SafeCodeHarness v2 — 续开发交接（2026-08-10）

## 交接结论（当前权威状态）

任务 1-14 已形成 stacked draft PR #1-#14；Task 15 位于独立 `codex/t15-release-evidence` worktree，本地发布资料、测试、证据与两阶段审查已经闭环。提交链为 `9acb2ae`、`60528ae`、`84a10b4`、`93f3415`；初审总计 C/I/M=`0/0/1`，唯一 Task 14 PLAN 历史 Minor 经 `93f3415` 修复后，限定复审为 `0/0/0`。本地结果为 backend `169 passed, 1 warning`、三份稳定 JSON demo、frontend `48 passed`、build 和真实 Chromium E2E `2 passed`。

**Task 15 整体仍未完成。** 当前分支已于 2026-08-10 推送至用户提供的 NJU Git remote `https://git.nju.edu.cn/xzy241276010/safe-code-harness-v2.git`（上游 `nju/codex/t15-release-evidence`），但没有 Task 15 PR，也未运行 `finishing-a-development-branch`。首个 GitLab `unit-test` 的真实失败已定位为 Bookworm 系统 Node 缺少全局 `File`；File-free 回归先 RED，`node:buffer` polyfill 和显式 `@types/node` 修复为 `749199a` 后，本地 frontend `49 passed`、build、backend `169 passed, 1 warning`、demos、Chromium E2E `2 passed`。用户提供的 GitLab 页面确认复跑 job #610231（pipeline #319723，`749199a`）和 job #610232（pipeline #319724，`87b432d`）均通过；GitHub Actions [run 31373926124](https://github.com/AlterGo-xzy/safe-code-harness-v2/actions/runs/31373926124) 的 test 和 docker-build job 也均通过。用户确认 Railway HTTPS Mock 演示站 `https://safe-code-harness-v2-production.up.railway.app`，其截图显示首页空状态，协调会话只读根请求返回 HTTP `200`；没有应用认证且未配置真实 Planner key，故不得录入真实 key 或上传敏感工作区，认证生产部署只可列为后续扩展。范围文档提交 `6aa5274` 已推送 GitHub/NJU；GitHub CI [run `31379732809`](https://github.com/AlterGo-xzy/safe-code-harness-v2/actions/runs/31379732809) 已通过，`test` 与 `docker-build` 均成功。GHCR 查询因 `gh` token 缺 `read:packages` 被 403 拒绝；该权限错误不得误写成 package 不存在或不公开。GHCR public 与未登录 pull/run、学生本人 1500-2500 字 `REFLECTION.md` 正文、Task 15 PR 与分支收尾仍是未完成项。不得把 NJU 分支存在或本地审查通过写成这些外部结果。下方 Task 13 细节保留为历史证据；与本节冲突的旧“当前状态”均以本节和 `PROJECT_PROGRESS.md` 为准。

本文件是给全新模型的最短可执行入口。开始工作前仍须依次阅读 `PROJECT_PROGRESS.md`、`AGENTS.md`、`PLAN.md`、`REQUIREMENTS_TRACEABILITY.md`、`AGENT_LOG.md`，并先运行 `git status --short`。

## 精确仓库状态

- 仓库：`D:\safe-code-harness-v2`；公开远程：`https://github.com/AlterGo-xzy/safe-code-harness-v2`。
- 当前工作目录：`D:\safe-code-harness-v2\.worktrees\t15-release-evidence`。
- 当前分支：`codex/t15-release-evidence`；接手时必须以 `git rev-parse HEAD` 获取包含本次状态回填提交在内的实际 HEAD。
- 本轮回填前 `git status --short` 无输出；没有需要保留的已跟踪用户改动。
- Task 1-14 的 stacked draft PR #1-#14 已存在且尚未合并；Task 15 基于 Task 14 分支，已推送 NJU Git，尚未建立 PR。
- `.venv`、`.superpowers/`、`frontend/node_modules`、`frontend/dist` 和浏览器产物均为本 worktree 忽略项，不能提交。

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

1. 不重做已关闭的 Task 13/14 或 Task 15 本地审查修复；NJU Git remote 与 Task 15 分支推送已完成。Railway Mock 演示站 URL 已由用户提供并确认，保持无真实 key/敏感工作区；认证生产部署被用户明确延后为扩展。下一步取得默认分支 GitHub 最终绿色记录、GHCR public/匿名 pull-run，以及学生本人反思正文。
2. 每项外部动作只能在用户授权和账户/远程可用后执行，必须记录真实 URL、日期、commit 和结果；失败或缺输入继续保持外部阻断。
3. 外部门槛满足并回填后，才可运行 `finishing-a-development-branch`、创建 Task 15 PR 或假称最终交付完成。延后策略扩展仍不属于 Task 15 本地发布资料范围。

## 严格流程与安全不变量

## 2026-08-10 Task 15 发布依赖更新

Railway Mock 演示站继续保持无真实 key/敏感工作区；认证生产部署由用户明确延后。只读 GitHub 盘点确认 PR #1-#14 均为 draft、Task 15 无 PR，且 `publish-image.yml` 尚未到达默认分支（查询 404）。下一模型不得在当前分支尝试或宣称 GHCR 发布；须先取得用户对 stacked PR 审查/合并的明确授权，待默认分支 CI 成功后才检查 package public 与匿名 pull/run。学生本人反思正文仍为外部输入门槛。

## 2026-08-10 Task 15 反思正文更新

用户现已在对话提供正文；协调会话仅原样写入 `REFLECTION.md`，未生成或润色。统计中文汉字为 `1583`，非空白字符为 `2852`。中文汉字计数符合 1500–2500 目标；若课程系统按所有非空白字符计数，学生须亲自决定是否缩短。不得由后续 agent 代写或改写其内容。

- 每个实现 task：独立 `codex/tNN-*` branch/worktree、新鲜 implementer、TDD（先 RED）、最小实现、spec/security review、quality review、真实记录、`finishing-a-development-branch`。
- 不提交 key、`.env`、虚拟环境、`node_modules`、`dist`、浏览器产物、测试缓存或 `.superpowers` 账本；不输出真实凭据或服务器/临时绝对路径。
- Harness 必须保持自实现主循环和确定性治理；不得引入 LangChain/AutoGen/CrewAI/LlamaIndex agent runner 或把宿主 agent/skill 当产品功能。
- Task 9 Planner 公共 DTO 始终只有安全字段，Credential Manager 异常不得泄露 key；Task 10 ZIP 路径/成员/大小/碰撞保护不得回退；Task 11/12 前端仍只使用安全 DTO。
- `REFLECTION.md` 必须由学生本人写作；AI 仅可协助大纲或润色。

## 有用命令

```powershell
Set-Location D:\safe-code-harness-v2\.worktrees\t15-release-evidence
git status --short
.\scripts\run_demos.ps1
.\.venv\Scripts\python.exe -m pytest backend\tests --basetemp .pytest-tmp\task15-backend -q
Set-Location frontend
npm.cmd test
npm.cmd run build
npm.cmd run test:e2e
Set-Location ..
git diff --check codex/t14-ci-distribution..HEAD
```

PowerShell 环境中 `rg.exe` 曾出现“拒绝访问”；优先使用 `git grep` 或窄范围 `Get-Content`。所有文档/源码修改用 `apply_patch`，保留无关用户改动。
## 2026-08-10 Task 13 分支收尾更新

Task 13 已推送，并创建目标为 `codex/t12-settings-approval-ui` 的 [draft PR #13](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/13)。保留本 worktree 和分支处理审查反馈；后续从 Task 14 开始，不得把 CI、分发、部署或策略扩展写成已完成。

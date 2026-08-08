# SafeCodeHarness v2 — 续开发交接（2026-08-09）

## 交接结论

代码和过程证据已保存到 Git；当前工作树没有已跟踪的未提交改动。**不要开始 Task 13 Task 3（Playwright/E2E），也不要开始任务 14、15 或策略扩展。**Task 13 Task 2 的第二次独立复审仍有 1 个 Important 和 2 个 Minor 未关闭，必须先按 TDD 修复、全量验证并再次独立复审。

本文件是给全新模型的最短可执行入口。开始工作前仍须依次阅读 `PROJECT_PROGRESS.md`、`AGENTS.md`、`PLAN.md`、`REQUIREMENTS_TRACEABILITY.md`、`AGENT_LOG.md`，并先运行 `git status --short`。

## 精确仓库状态

- 仓库：`D:\safe-code-harness-v2`；公开远程：`https://github.com/AlterGo-xzy/safe-code-harness-v2`。
- 当前工作目录：`D:\safe-code-harness-v2\.worktrees\t13-demos-e2e`。
- 当前分支：`codex/t13-demos-e2e`；运行时实现基线为 `7bf3d04 docs: record task 13 demo review fixes`，其后仅有本交接/进度文档提交。接手时以 `git rev-parse HEAD` 获取实际当前 HEAD。
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

### Task 13 Task 2：离线机制演示 — 代码已保存，但尚未闭环

已提交实现：

- `26f9855 test: add deterministic mechanism demos`
- `b2b7e15 docs: record task 13 demo evidence`
- `7243dfc fix: harden deterministic demo evidence`
- `7bf3d04 docs: record task 13 demo review fixes`

涉及文件：

- `scripts/run_guardrail_demo.py`：调用现有 `CommandGuard`/`RuntimePolicy`，投影危险命令被阻止的稳定 JSON。
- `scripts/run_feedback_demo.py`：调用现有 `AgentLoop`、`MockLLM`、反馈和临时目录，证明失败测试反馈改变下一动作。
- `scripts/run_approval_demo.py`：调用真实 `RunService`/审批恢复并从 snapshots 投影转录。
- `scripts/run_demos.ps1`：Windows 入口；`Makefile` 只提供 Unix-like `demos` target，未在 Windows 假称运行。
- `backend/tests/integration/test_demos.py`：函数与 subprocess JSON 安全测试。
- 根 `README.md`：仅说明离线 demos，未把它们写成 E2E/CI/部署证据。

已验证、可如实引用的结果：

- 初始 RED：缺少 demo 模块时 `ModuleNotFoundError: scripts.run_approval_demo`。
- 初次 GREEN：`test_demos.py` `6 passed in 0.23s`；修复后的 focused suite `10 passed in 0.47s`。
- 正常 `./scripts/run_demos.ps1`（PowerShell 写法为 `.\scripts\run_demos.ps1`）输出三段稳定 JSON。
- 修复后的完整 `backend/tests`：`156 passed, 1 warning`；warning 是既有 Starlette/TestClient 弃用提示。
- `git diff --check` 无输出；已变更文件的高置信凭据候选计数为 `0`。

## 当前阻断：Task 13 Task 2 第二次复审未通过

第二次只读独立复审结论：Critical 0、**Important 1**、Minor 2。没有任何修复在此结论后提交；此前 implementer 已被停止，故当前代码正是 `7bf3d04`。

必须依序完成以下工作，且每个行为修复先有 RED 测试：

1. **Important：审批等待期必须拒绝任何工具结果。**
   - 当前 `scripts/run_approval_demo.py` 仅将 `tool_succeeded` 作为等待期提前执行；`tool_failed` 仍可能被忽略。
   - 在 `backend/tests/integration/test_demos.py` 先加入 `tool_failed` 出现在等待快照或 approval 前的回归，预期 demo 拒绝该不安全事件序列。
   - 最小修复应拒绝 waiting snapshot 或 approval 前出现的任何工具结果（至少 `tool_succeeded`、`tool_failed`）；保留“waiting 未执行、approved 早于 executed”的真实 snapshot 投影，不得回退成硬编码转录。

2. **Minor：PowerShell 失败传播测试必须证明后续脚本不会运行。**
   - 现实现已逐 child 检查 `$LASTEXITCODE`，但测试目前只有一个失败 child，无法防止将来退化成循环后只检查最后一次退出码。
   - 先写“失败 child + 后续成功/写标记 child”的 RED，断言总入口失败且标记未创建/后续脚本未运行；随后最小调整实现或测试辅助。

3. **Minor：修正状态文件的过期文字。**
   - `PROJECT_PROGRESS.md` 顶部仍写 focused `6 passed` 和“两阶段审查尚待”；应改为初审已完成、修复后 focused `10 passed`、第二次复审未通过且上述三项待处理。
   - `REQUIREMENTS_TRACEABILITY.md` 仍把完整回归写为未执行；应如实改为 `156 passed, 1 warning`，并标注复审未闭环。
   - 同步 `PLAN.md`、`AGENT_LOG.md` 和本文件中的完成状态；不要把 Task 2 标为完成。

修复后至少运行：focused demo 测试、`.\scripts\run_demos.ps1`、完整 `backend/tests`、`git diff --check` 和已变更文件凭据候选计数检查。然后用新的独立 reviewer 先做 spec/security、再做质量审查；任何 Critical/Important 必须再走 RED→最小修复→复审。只有两阶段审查通过，才可登记 Task 2 完成并开始 Task 3。

## 随后工作顺序（不得提前）

1. 关闭上述 Task 2 复审发现并记录实际命令、输出、commit、review 到四份过程文档。
2. Task 13 Task 3：按已批准的 `docs/superpowers/plans/2026-08-09-demos-e2e.md` 增加 Playwright。真实 FastAPI API 用于创建和核验；**浏览器必须实际点击“批准”**；直接 API 读取必须证明点击前 `waiting_approval`、点击后 `completed` 和 executed 证据。不得拦截 API、不得用 sleep。
3. Task 3 必须实际验证 320px：批准按钮可见且 `document.documentElement.scrollWidth <= window.innerWidth`。若需修改 CSS，先写失败 E2E。
4. Playwright 需要 `@playwright/test` 和 Chromium。安装依赖/浏览器是受控网络动作；若失败，记录真实阻断，不能宣称 E2E 成功。Windows 没有 GNU make；不要把 Makefile target 当 Windows 验证。
5. Task 13 最终 Task 4：执行 backend、三演示、干净 frontend install/unit/build/E2E、diff/凭据扫描；重新核对要求文件追踪；更新过程文件；使用 `finishing-a-development-branch` 决定推送和 draft PR #13。
6. Task 14（CI/容器分发）、Task 15（公网部署/最终交付）和延后的策略扩展都尚未开始。

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

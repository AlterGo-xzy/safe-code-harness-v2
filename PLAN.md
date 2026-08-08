# SafeCodeHarness v2 实现计划

> **面向执行 agent：必须使用 `superpowers:subagent-driven-development`。每个任务只由一个新鲜 subagent 在独立 worktree 完成，并在任务结束后接受“spec 合规审查 -> 代码质量审查”。**

**目标：** 交付一个可部署的 Coding Agent Harness。模型只能提出 JSON 动作，项目自己的代码负责主循环、工具、治理、反馈、记忆、配置、审批和可观察性。

**架构：** Python/FastAPI 后端拥有 Harness 内核；React 只提供运行、检查、配置和审批界面；Docker 镜像同时服务 API 与 WebUI。所有生产实现都在计划后的独立 worktree 中完成。

**技术栈：** Python 3.12、FastAPI、Pydantic、pytest、React、TypeScript、Vite、Vitest、Playwright、Docker、GHCR、GitHub Actions、GitLab CI。

## 全局约束

- 任务 0 未完成前禁止编写生产 Harness 代码。
- 不使用 LangChain、AutoGen、CrewAI、LlamaIndex agent 或任何高层 agent runner。
- 每个任务必须先记录失败测试命令，再写最小实现使它变绿，最后才可重构。
- 所有机制测试离线运行，使用 Mock/stub LLM，不使用真实 key 或网络。
- 可选 Planner key 在 Windows 只存入 Credential Manager；无安全存储适配器的平台拒绝持久化。
- 每个完成任务将下方“完成记录”改为真实 commit hash、PR、红绿命令和两阶段审查结论；不得预填。
- 每个 PR 必须说明 task、subagent id、旧仓库参考文件（如有）、人工修改、红绿结果与两阶段审查。
- 前端任务开始前必须实际确认或安装 Open Design skill，并将真实证据写入 `AGENT_LOG.md`。

## 依赖与并行

`0 冷启动 -> 1 基座 -> (2 协议, 3 路径治理, 4 命令审批) -> 5 工具 -> 6 反馈记忆 -> 7 主循环 -> 8 API -> (9 凭据, 10 上传, 11 WebUI) -> 12 WebUI 审批配置 -> 13 演示与端到端 -> 14 CI/镜像 -> 15 发布与交付核验`。

任务 2、3、4 可并行；任务 9、10、11 可在任务 8 后并行。每个任务均在以 `codex/tNN-*` 命名的分支及对应 `.worktrees/tNN-*` worktree 中执行，完成后创建一个只包含该任务的 PR 指向 `main`。PR 描述必须注明 task 编号、实际 subagent 标识、参考的旧仓库文件（若使用）、人工修改、红-绿结果和两阶段审查结论；不得预填 hash 或 PR 编号。

本文件以模块覆盖为主而非版面顺序；任何执行 agent 必须以本节依赖图和任务编号作为唯一执行顺序，不能因后文标题的物理位置提前执行任务 5-15。

本文件以模块覆盖为主而非版面顺序；任何执行 agent 必须以本节依赖图和任务编号作为唯一执行顺序，不能因后文标题的物理位置提前执行任务 5-15。

## 任务 0：不同类型 agent 冷启动验证

**文件：** 修改 `SPEC_PROCESS.md`、`AGENT_LOG.md`、`REQUIREMENTS_TRACEABILITY.md`；读取 `SPEC.md`、`PLAN.md`。

**目标：** 在任何实现前用不同类型、全新 session 的 agent 仅凭 SPEC+PLAN 验证清晰度。

- [x] **步骤 1：发送密封 prompt**

```text
你是 SafeCodeHarness v2 的冷启动开发者。只阅读 SPEC.md 和 PLAN.md。
选择任务 1 或任务 2 的一个失败测试步骤，说明需要创建的文件和预期红色结果；
若接口、边界、测试命令或依赖不明确，立即停止并提出问题。不得读取旧仓库或主会话历史。
```

- [x] **步骤 2：记录原始输出**

记录 agent 类型、全新 session 证明、完整 prompt、仅有 SPEC+PLAN 的输入约束、问题和输出。

- [x] **步骤 3：按问题修订文档**

将每个问题判定为规约缺失或误读；在 `SPEC.md`/`PLAN.md` 写出确定答案，在 `SPEC_PROCESS.md` 保留修订前后关键 diff。

- [x] **步骤 4：验证门禁**

人工检查过程文档含不同类型、输入隔离、暂停问题、输出、修订；缺任一项即停止。

- [x] **步骤 5：提交**

```powershell
git add SPEC.md PLAN.md SPEC_PROCESS.md AGENT_LOG.md REQUIREMENTS_TRACEABILITY.md
git commit -m "docs: record independent cold-start validation"
```

**完成记录：** Claude Code `2.1.220`（主开发为 Codex Desktop）在非 `--resume` 新启动会话中，只 Fetch commit `fc9b754` 的 `SPEC.md` 与 `PLAN.md`；原始转录与工具轨迹为 `docs/evidence/cold-start-claude-code-task1.md`。它对任务 1 提出四项规约缺口并暂停；修订提交为 `ecbc418`，隔离核验提交为 `107bda3`。任务 0 是规约门禁，不创建 worktree 或 PR；后续实现任务才逐一使用独立 worktree/PR。

## 任务 1：工程基座与离线测试入口

**工作区与 PR：** `codex/t01-foundation` / `.worktrees/t01-foundation`，独立 PR 指向 `main`。
**文件：** 新建 `backend/pyproject.toml`、`backend/src/safe_code_harness/__init__.py`、`backend/tests/conftest.py`、`backend/tests/unit/test_project_contract.py`、`scripts/test.ps1`；扩展 `.gitignore`。`.gitignore` 已在任务 1 之前的 worktree 流程准备提交中最小创建，仅包含 `.worktrees/` 与 `.superpowers/`；任务 1 在自己的 worktree 补充 Python、Node、测试和凭据忽略项。本任务**不**创建 `Makefile`；它在任务 14 与容器/CI 一并创建。任何共享 fixture 在真实出现需求的任务再加入，`conftest.py` 在本任务只负责测试导入路径。

**固定配置：** 发布名 `safe-code-harness`，导入名 `safe_code_harness`，版本 `0.1.0`，`requires-python = ">=3.12"`。`backend/pyproject.toml` 使用 setuptools 和 src layout：`package-dir = {"" = "src"}`、包发现 `where = ["src"]`，`dependencies = []`，`dev = ["pytest>=8,<9"]`，pytest `testpaths = ["tests"]`。任务 8 才可向运行时依赖添加 FastAPI/Pydantic/HTTP 依赖；任务 11 才创建 Node 依赖。

**测试路径与一键入口：** `backend/tests/conftest.py` 在 pytest 进程把仓库的 `backend/src` 插入 `sys.path`，使红色阶段精确报 `ModuleNotFoundError`，且不依赖工作目录或全局 `PYTHONPATH`。`scripts/test.ps1` 是 Windows 的等价一键测试入口；任务 1 时它只运行已有的 `backend/tests/unit`，后续任务再扩展。

- [x] **步骤 0：仅建立测试环境，不建立生产包**

创建 `.venv`，并安装测试工具：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "pytest>=8,<9"
```

创建 `backend/tests/conftest.py`，其唯一职责是把 `Path(__file__).parents[1] / "src"` 放入 `sys.path`；此文件不导入或定义任何 Harness 机制。这个脚手架不是生产实现，允许早于失败测试存在。

- [x] **步骤 1：写失败测试**

```python
def test_package_exposes_version() -> None:
    from safe_code_harness import __version__
    assert __version__ == "0.1.0"
```

- [x] **步骤 2：确认红色结果**

运行：`.\.venv\Scripts\python.exe -m pytest backend/tests/unit/test_project_contract.py -q`

期望：`ModuleNotFoundError: safe_code_harness`。

- [x] **步骤 3：最小实现**

```python
# backend/src/safe_code_harness/__init__.py
__version__ = "0.1.0"
```

随后创建 `backend/pyproject.toml`，内容必须包含：

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "safe-code-harness"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8,<9"]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-ra"]
```

- [x] **步骤 4：确认绿色结果并重构**

运行：

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests/unit/test_project_contract.py -q
.\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
.\.venv\Scripts\python.exe -c "from safe_code_harness import __version__; assert __version__ == '0.1.0'"
```

期望：pytest 输出 `1 passed`，独立导入命令无输出且退出码为 0。创建 `scripts/test.ps1` 以调用 `.venv\\Scripts\\python.exe -m pytest backend/tests/unit`；`.gitignore` 至少忽略 `.venv/`、`__pycache__/`、`*.py[cod]`、`.pytest_cache/`、`.pytest-tmp/`、`*.egg-info/`、`build/`、`dist/`、`.env`、`.env.*`、`frontend/node_modules/`、`frontend/dist/`、`playwright-report/` 与 `test-results/`，并保留 `.env.example`。不加入业务机制。

- [x] **步骤 5：两阶段审查与提交**

先确认本任务只建立基座；再审查 editable install、测试隔离、PowerShell 入口和 `.gitignore`。提交：

```powershell
git add backend scripts/test.ps1 .gitignore
git commit -m "chore: establish offline test foundation"
```

**完成记录：** 实现 subagent `Arendt` 在 `codex/t01-foundation` worktree 完成，提交 `cc81e31`。RED：`.\.venv\Scripts\python.exe -m pytest backend/tests/unit/test_project_contract.py -q` 得到预期 `ModuleNotFoundError: safe_code_harness`；GREEN：focused pytest、editable install、独立 `python -c` 导入、`scripts/test.ps1` 和当前全部 backend 测试均通过（`1 passed`）。独立 reviewer `Mencius` 的 spec 合规与代码质量审查均批准，Critical/Important/Minor 均为无；主协调会话在创建 PR 前再次运行 `scripts/test.ps1`，得到 `1 passed in 0.01s`，并验证 `git diff --check origin/main...HEAD` 无输出。过程记录提交为 `30dc566`。draft PR 已创建：[\#1](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/1)。按 `finishing-a-development-branch`，用户选择“推送并创建 PR”，因此保留 `codex/t01-foundation` 分支和 worktree 等待审查；可进入任务 2。

## 任务 13：确定性机制演示与浏览器端到端验证

**工作区与 PR：** `codex/t13-demos-e2e` / `.worktrees/t13-demos-e2e`，独立 PR。
**文件：** 新建 `scripts/run_guardrail_demo.py`、`run_feedback_demo.py`、`run_approval_demo.py`、`frontend/e2e/workbench.spec.ts`；修改 `Makefile`、`README.md`；测试 `backend/tests/integration/test_demos.py`。
**接口与验收：** 演示输出稳定 JSON。护栏演示必须有 `blocked: true`；反馈演示必须证明第一次 `run_tests` 失败后下一动作变为 `write_file`；审批演示必须依次显示 `waiting_approval -> approved -> executed`。E2E 必须针对真实本地 API 与 UI，不用页面内容替代后端断言。

**Task 1 API 集成检查点（已完成）：** fresh implementer `/root/t13_task1_implementer` 先新增 `test_integrated_api_surface.py`，在任何 merge 前得到预期 RED：`create_app()` 不接受 `secret_store`。随后按顺序以 merge commit `ec613df`、`1664aa2` 合入已审查的 Task 9/10 分支；仅统一 app factory 为三个 service state 和三个 router，Task 9/10 安全源码与测试相对来源分支无 diff。focused GREEN 为 `1 passed`，完整 backend 为 `146 passed`；均只有既有 Starlette/TestClient 弃用 warning。集成测试与过程记录提交为 `fd38e6a`。此检查点不包含 demo、frontend/E2E、320px 浏览器或 policy 工作，以下 Task 13 主清单仍保持未完成。

**Task 2 演示检查点（实现完成，审查待执行）：** fresh implementer `/root/t13_task2_implementer` 先创建 `backend/tests/integration/test_demos.py`；RED 命令 `.\.venv\Scripts\python.exe -m pytest backend\tests\integration\test_demos.py --basetemp .pytest-tmp\task13-demos-red -q` 因三份脚本缺失而以 `ModuleNotFoundError: scripts.run_approval_demo` 失败。最小实现只复用本仓库的 `CommandGuard`/`RuntimePolicy`、`AgentLoop`/`MockLLM`/反馈/记忆和 `RunService`/`ApprovalStore`，反馈脚本在临时目录中运行并在 `finally` 清理；输出只投影稳定结构，不含命令、临时路径或敏感内容。GREEN 同一测试为 `6 passed in 0.23s`，`.\scripts\run_demos.ps1` 按固定顺序输出三份 JSON；CLI 测试解析 JSON 并拒绝 `C:`、`D:`、`secret`。完整 backend 回归为 `152 passed, 1 warning`（既有 TestClient 弃用），`git diff --check` 无输出、凭据候选计数为 0。新增 `Makefile` 的 Unix-like `demos` target 和最小 README 离线说明；Windows 无 GNU make，故未假称运行 `make demos`。未读、复制或咨询旧项目代码。尚未进行本检查点的 spec/quality 两阶段审查、Playwright 或 320px 验证。

- [ ] **步骤 1：写失败测试**

```python
def test_feedback_demo_proves_feedback_changes_next_action() -> None:
    transcript = run_feedback_demo()
    assert transcript[0]["action"] == "run_tests"
    assert transcript[0]["ok"] is False
    assert transcript[1]["action"] == "write_file"
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/integration/test_demos.py -q`，预期模块不存在或断言失败。
- [ ] **步骤 3：最小实现**：只基于 MockLLM 和临时工作区构建三个演示；编写 Playwright 启动流程，覆盖创建运行、看到阻止事件、待审批和批准。
- [ ] **步骤 4：确认绿色结果与重构**：运行 `make demos`、`python -m pytest backend/tests/integration/test_demos.py -q`、`cd frontend; npm.cmd run test:e2e`，预期输出与浏览器断言均稳定通过。
- [ ] **步骤 5：两阶段审查与提交**：先审查演示分别证明 A 项目三条硬机制而非仅打印文案，再审查临时目录清理、无网络依赖和 Playwright 等待条件；提交 `git commit -m "test: add deterministic mechanism demos and e2e coverage"`。

**完成记录：** 真实红绿命令、审查结论、hash、PR、稳定演示和 E2E 证据。

## 任务 14：GitHub/GitLab CI 与 Docker/GHCR 分发

**工作区与 PR：** `codex/t14-ci-distribution` / `.worktrees/t14-ci-distribution`，独立 PR。
**文件：** 新建 `.github/workflows/ci.yml`、`.github/workflows/publish-image.yml`、`.gitlab-ci.yml`、`Dockerfile`、`docker-compose.yml`、`.dockerignore`；修改 `Makefile`、`README.md`。
**接口与验收：** `make test` 一键运行后端与前端核心测试；每次 push 的 GitHub Actions 和 GitLab `unit-test` 运行测试；默认分支推送构建并将镜像推送 GHCR（在仓库设置公开 package）；镜像在目标机用环境变量/系统凭据配置 Planner key，绝不烘焙入镜像。

- [ ] **步骤 1：写失败测试**

```python
def test_publish_workflow_targets_ghcr_and_never_reads_dotenv() -> None:
    workflow = Path(".github/workflows/publish-image.yml").read_text(encoding="utf-8")
    assert "ghcr.io" in workflow
    assert ".env" not in workflow
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_distribution_config.py -q`，预期工作流文件不存在或断言失败。
- [ ] **步骤 3：最小实现**：配置 Python/Node job、Playwright 浏览器安装及 E2E、Docker build；GitHub publish job 使用 `GITHUB_TOKEN` 的 packages 写权限，GitLab job 名固定 `unit-test`。Docker 多阶段构建 WebUI 并由 FastAPI 提供静态文件。
- [ ] **步骤 4：确认绿色结果与重构**：运行 `make test`、`docker build -t safe-code-harness-v2:local .`、`docker compose up --build` 后调用 `/api/runs`；本地镜像不含 key；推送 PR 后检查两套 CI，默认分支发布后从公开 GHCR pull/run。
- [ ] **步骤 5：两阶段审查与提交**：先审查 CI/镜像没有改变离线机制与凭据边界，再审查缓存、端口、健康检查、失败日志和镜像大小；提交 `git commit -m "build: add ci and container distribution"`。

**完成记录：** 真实红绿命令、GitHub CI、GitLab CI、GHCR pull/run、审查结论、hash、PR。

## 任务 15：发布文档、外部部署与最终交付核验

**工作区与 PR：** `codex/t15-release-evidence` / `.worktrees/t15-release-evidence`，独立 PR。
**文件：** 新建 `README.md`、`LICENSE`、`THIRD_PARTY_NOTICES.md`、`.github/pull_request_template.md`；更新 `SPEC_PROCESS.md`、`AGENT_LOG.md`、`REQUIREMENTS_TRACEABILITY.md`、`PLAN.md`。学生本人负责新建或保留 `REFLECTION.md`，agent 不代写正文。
**外部交付：** 部署至 Render/Railway/Fly.io 等，记录公开 URL；将仓库同步到南京大学 GitLab；所有任务 PR 按 `finishing-a-development-branch` 决定 merge/保留/丢弃；最终主分支通过 CI。

- [ ] **步骤 1：写失败测试**

```python
def test_readme_contains_reproducible_run_and_key_safety_instructions() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docker pull" in readme
    assert "Credential Manager" in readme
    assert "已知限制" in readme
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_release_docs.py -q`，预期 README 或断言尚不满足。
- [ ] **步骤 3：最小实现**：README 说明获取、`docker pull/run`、本地开发、`make test`、演示、Windows 凭据配置/更新/清除、目标平台、已知限制、部署架构和 CI/CD；PR 模板要求 subagent/human/TDD/审查记录；列出第三方许可证。
- [ ] **步骤 4：确认绿色结果与外部核验**：运行该文档测试与 `make test`；检查 GitHub 与 GitLab 最终绿色流水线、GHCR 未登录 pull 后运行、部署 URL 的 UI/审批/Mock 演示、NJU Git 仓库可访问、`git log --all` 无真实凭据。将真实 URL、日期、commit、PR、命令和结果写入追踪表与日志。
- [ ] **步骤 5：最终两阶段审查、分支收尾与提交**：先逐条复核 SPEC/课程 traceability，再通过 `superpowers:requesting-code-review` 完成代码质量审查；所有 Critical 修复后触发 `superpowers:finishing-a-development-branch`，按其真实建议合并或保留 PR。提交 `git commit -m "docs: record verified release evidence"`，不伪造不可验证的外部结果。

**完成记录：** 真实红绿命令、审查结论、合并/保留决定、hash、PR、CI、GHCR、部署及 NJU Git 证据。

## 计划自审

- [ ] **SPEC 覆盖：** 任务 2、5、6、7 覆盖 Harness 六维和 A 项目自主主循环；任务 3、4、7、8、12、13 覆盖深度治理与 HITL；任务 9 覆盖凭据威胁模型；任务 10 覆盖租户/工作区边界；任务 11、12 覆盖 Open Design WebUI；任务 13 覆盖三类机制演示；任务 14、15 覆盖一键测试、CI、分发、公共部署与提交证据。
- [ ] **流程覆盖：** 已完成 brainstorming；本计划由 writing-plans 产出；任务 0 是强制的不同类型 agent 冷启动门槛；任务 1-15 逐个使用 worktree、fresh subagent、TDD、两阶段审查、PR；任务 15 使用 requesting-code-review 与 finishing-a-development-branch。
- [ ] **执行前门槛：** 在 `PLAN.md` 本次提交并由用户确认后，先做任务 0；未把任务 0 的完整证据与修订提交前，禁止创建任何 `backend/` 或 `frontend/` 实现文件。
- [ ] **缺口判定：** 当前不预填任务完成状态、commit、PR、CI、GHCR、云部署或 NJU Git；它们只有在真实执行后才可标记为“已完成并验证”。

## 任务 5：受控工具与分派器

**工作区与 PR：** `codex/t05-tools` / `.worktrees/t05-tools`，独立 PR 指向 `main`。
**文件：** 新建 `backend/src/safe_code_harness/tools/file_tools.py`、`test_tools.py`、`shell_tools.py`、`memory_tools.py`、`dispatcher.py`；测试 `backend/tests/unit/test_dispatcher.py`、`test_file_tools.py`、`test_test_tools.py`。
**接口：** `ToolDispatcher.dispatch(action: Action) -> ToolResult`；`ToolResult` 含 `ok`、`summary`、`details`、`artifacts`。所有文件工具接收 `PathSandbox`，所有命令工具先调用 `CommandGuard`。

- [ ] **步骤 1：写失败测试**

```python
def test_unknown_action_does_not_execute_any_tool() -> None:
    result = ToolDispatcher({}).dispatch(Action(type="unknown", args={}))
    assert result.ok is False
    assert result.summary == "unknown tool"
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_dispatcher.py -q`，预期导入错误或断言失败。
- [ ] **步骤 3：最小实现**：仅建立显式的 handler 白名单；未知动作返回失败 `ToolResult`。文件读写使用已审计路径，测试命令采用无 shell 拼接的参数列表和超时。
- [ ] **步骤 4：确认绿色结果与重构**：补充工作区外路径、禁用工具、超时和命令护栏测试；运行 `python -m pytest backend/tests/unit/test_dispatcher.py backend/tests/unit/test_file_tools.py backend/tests/unit/test_test_tools.py -q`，预期全绿且不联网。
- [ ] **步骤 5：两阶段审查与提交**：先确认工具层没有自行绕过规则或审批，再审查子进程参数、错误结构和资源释放；提交 `git commit -m "feat: add governed tool dispatcher"`。

**完成记录：** 实现 subagent `/root/t05_implementer` 在 stacked 分支 `codex/t05-tools` 完成，提交 `2795539`。按用户授权，RED 后仅参考旧项目 `D:\2026_summer_project\backend\src\safe_code_harness\tools\file_tools.py`、`test_tools.py`、`shell_tools.py`、`dispatcher.py` 与 `tests\unit\test_tool_dispatcher.py`；人工适配为当前 `Action`、`PathSandbox`、`CommandGuard` 和显式 `ToolResult`，未迁入 AgentLoop、API、planner、凭据、反馈或旧 memory。RED：三个 focused 测试按预期报 `ModuleNotFoundError: safe_code_harness.tools`；GREEN：focused `7 passed`、完整 backend `58 passed`。独立 reviewer `/root/t05_reviewer` 审查批准，无 Critical/Important；一个 Minor（安全 shell 的 argv/timeout 及审批短路回归）已登记于 SDD ledger，留待后续测试加固。协调会话从 worktree 根目录运行 `scripts/test.ps1`，为 `58 passed in 0.10s`；`git diff --check 716d246..HEAD` 无输出。凭据形态扫描唯一命中为既有假 token fixture，不是密钥。按既有选项 2，已推送并创建目标为 `codex/t04-command-approval` 的 [stacked draft PR #5](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/5)，保留分支/worktree 等待审查。

## 任务 6：确定性反馈与有界运行记忆

**工作区与 PR：** `codex/t06-feedback-memory` / `.worktrees/t06-feedback-memory`，独立 PR。
**文件：** 新建 `backend/src/safe_code_harness/feedback/evaluator.py`、`memory/store.py`；测试 `backend/tests/unit/test_feedback.py`、`test_memory.py`。
**接口：** `FeedbackEvaluator.from_result(action, result) -> Feedback`；`MemoryStore.remember(event)` 与 `MemoryStore.relevant(limit) -> list[MemoryEvent]`。记忆仅限当前 `run_id`，有条数与字节上限，并且只保存摘要，不保存 API key 或文件原文。

- [ ] **步骤 1：写失败测试**

```python
def test_failed_test_result_produces_actionable_feedback() -> None:
    feedback = FeedbackEvaluator().from_result(
        Action(type="run_tests", args={}), ToolResult(ok=False, summary="2 failed")
    )
    assert feedback.kind == "tool_failure"
    assert "2 failed" in feedback.summary
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_feedback.py -q`，预期导入错误或断言失败。
- [ ] **步骤 3：最小实现**：按成功、工具失败、规则拒绝、审批拒绝四类结果生成结构化反馈；实现 FIFO 有界内存和敏感字段剔除。
- [ ] **步骤 4：确认绿色结果与重构**：补充超过上限、跨 run 隔离、secret-like 键剔除、空结果测试；运行 `python -m pytest backend/tests/unit/test_feedback.py backend/tests/unit/test_memory.py -q`，预期全绿。
- [ ] **步骤 5：两阶段审查与提交**：先审查反馈不会把模型文本变成政策，再审查内存上限和脱敏；提交 `git commit -m "feat: add deterministic feedback and bounded memory"`。

**完成记录：** Task 8 implementer `/root/t08_implementer` 提交 `974d73b`，依赖修复 `7afa279`。RED 为缺少 API 模块；仅在 RED 后局部适配旧 API，所有审批继续均经 `AgentLoop.resume`。独立审查发现 `httpx2` 错误依赖（Important）；干净 venv 安装验证后改为直接 `httpx`，scoped re-review PASS。新鲜 full backend `96 passed`、一键 unit `88 passed`、diff clean；上游 Starlette 1 条弃用警告已记录；PR 收尾另行记录。

## 任务 7：自实现 Agent 主循环

**工作区与 PR：** `codex/t07-agent-loop` / `.worktrees/t07-agent-loop`，独立 PR。
**文件：** 新建 `backend/src/safe_code_harness/core/agent_loop.py`、`core/context.py`；测试 `backend/tests/unit/test_agent_loop.py`、`backend/tests/integration/test_mock_feedback_loop.py`。
**接口：** `AgentLoop(llm, rules, approvals, tools, feedback, memory).run(task, config) -> RunState`；运行事件类型固定为 `context`、`llm_action`、`rule_decision`、`approval`、`tool_result`、`feedback`、`stopped`。循环最大步数、无效 JSON 与工具失败均可观察且有停止原因。

- [ ] **步骤 1：写失败测试**

```python
def test_failed_tests_change_the_next_mock_action() -> None:
    llm = MockLLM([
        '{"type":"run_tests","args":{}}',
        '{"type":"write_file","args":{"path":"a.py","content":"fixed"}}',
        '{"type":"finish","args":{}}',
    ])
    run = build_loop(llm, failing_then_write_dispatcher()).run("repair", RunConfig(max_steps=3))
    assert [event.action_type for event in run.tool_events] == ["run_tests", "write_file"]
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_agent_loop.py backend/tests/integration/test_mock_feedback_loop.py -q`，预期导入错误或断言失败。
- [ ] **步骤 3：最小实现**：按“构造 context -> 请求一个 JSON 动作 -> 解析 -> 规则 -> 审批 -> 工具 -> 反馈/记忆 -> 停止”实现单步循环；模型不能直接执行任何工具。
- [ ] **步骤 4：确认绿色结果与重构**：新增 `finish`、达到最大步数、解析失败、规则阻止、审批拒绝和工具失败后的下一动作测试；运行同一命令，预期全绿且 Mock 序列确定。
- [ ] **步骤 5：两阶段审查与提交**：先对照 SPEC 的“模型仅决策、代码治理执行”边界，再检查状态转换与事件顺序；提交 `git commit -m "feat: implement governed agent loop"`。

**完成记录：** fresh implementer `/root/t07_implementer` 完成 `2ceb6b1`，审查修复为 `e018822`、`328baaf`。RED 为缺少 `agent_loop`；旧项目仅在 RED 后参考 `core\agent_loop.py` 和相关测试的单步循环/事件概念，未迁入框架、API、planner 或凭据。初始完整 backend 为 `83 passed`。独立审查发现命令/写入审批绕过、pending 无法安全恢复（Critical）及工具失败结构化可观察性（Important）；两轮均先新增失败回归，最终 scoped re-review PASS。协调会话新鲜验证：`scripts/test.ps1` unit `88 passed`，显式 `pytest backend/tests`（含 integration）`89 passed in 0.12s`，`git diff --check 124b7f6..HEAD` 无输出；PR 收尾另行记录。

## 任务 8：FastAPI 运行与审批 API

**工作区与 PR：** `codex/t08-api-runs` / `.worktrees/t08-api-runs`，独立 PR。
**文件：** 新建 `backend/src/safe_code_harness/api/main.py`、`run_service.py`、`routes_runs.py`；修改 `backend/pyproject.toml` 以加入首次实际需要的 FastAPI/Pydantic/HTTP 依赖；测试 `backend/tests/integration/test_runs_api.py`。
**接口：** `POST /api/runs` 创建运行；`GET /api/runs/{run_id}` 查询运行和事件；`POST /api/runs/{run_id}/approvals/{approval_id}/approve`、`.../reject` 推进运行。HTTP 响应禁止返回凭据原文。

- [ ] **步骤 1：写失败测试**

```python
def test_pending_write_only_runs_after_explicit_approval(client) -> None:
    run_id = client.post("/api/runs", json={"scenario": "pending_write"}).json()["id"]
    pending = client.get(f"/api/runs/{run_id}").json()
    assert pending["status"] == "waiting_approval"
    client.post(f"/api/runs/{run_id}/approvals/{pending['approval_id']}/approve")
    assert client.get(f"/api/runs/{run_id}").json()["status"] == "completed"
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/integration/test_runs_api.py -q`，预期路由不存在或断言失败。
- [ ] **步骤 3：最小实现**：建立进程内 `RunService`，将审批状态连接到任务 7 的状态机；无效 id 返回结构化 404，拒绝后不得执行待审批动作。
- [ ] **步骤 4：确认绿色结果与重构**：补充未知运行、重复审批、拒绝和不可序列化事件测试；运行 `python -m pytest backend/tests/integration/test_runs_api.py -q`，预期全绿。
- [ ] **步骤 5：两阶段审查与提交**：先审查 API 没有绕过 AgentLoop，再审查状态隔离、错误码和日志脱敏；提交 `git commit -m "feat: expose governed runs through api"`。

**完成记录：** 初始实现/依赖修正提交为 `974d73b`、`7afa279`、过程记录 `2de48a2`；现为解除任务 11 的真实 API 契约阻断，经用户确认补充只读列表。fresh implementer `/root/t08_runlist_implementer` 先在 `GET /api/runs` 得到 405、详情缺 `scenario` 的 `3 failed` RED，后提交 `afd42ae feat(api): add safe run list summaries`。列表只白名单返回 `id`、`scenario`、`status`、`updated_at`，按创建时序稳定排序；详情补同样安全元数据。独立审查 PASS，无 C/I/M；协调验证完整 backend `99 passed, 1 warning`、脚本 unit `88 passed`，warning 是既有 TestClient 弃用提示。更新既有 draft PR #8，保留分支/worktree。

## 任务 2：动作协议、运行模型与 Mock LLM

**文件：** 新建 `backend/src/safe_code_harness/core/action.py`、`backend/src/safe_code_harness/core/models.py`、`backend/src/safe_code_harness/llm/base.py`、`backend/src/safe_code_harness/llm/mock.py`；测试 `backend/tests/unit/test_action_parser.py`、`backend/tests/unit/test_mock_llm.py`。

**接口：** `parse_action(raw: str) -> Action`；`LLMClient.next_action(context: str) -> str`；`MockLLM(responses: list[str])`；`Action(type, args, thought)`。

- [ ] **步骤 1：写失败测试**

```python
def test_parse_action_rejects_non_object_args() -> None:
    with pytest.raises(ValueError, match="args must be an object"):
        parse_action('{"type":"run_tests","args":[]}')
```

- [ ] **步骤 2：确认红色结果**

运行：`python -m pytest backend/tests/unit/test_action_parser.py -q`

期望：导入错误或缺少 `parse_action`。

- [ ] **步骤 3：最小实现**

```python
def parse_action(raw: str) -> Action:
    payload = json.loads(raw)
    if not isinstance(payload.get("args"), dict):
        raise ValueError("args must be an object")
    return Action(type=payload["type"], args=payload["args"], thought=payload.get("thought"))
```

- [ ] **步骤 4：确认绿色结果**

增加 invalid JSON、缺少 type、Mock 响应耗尽测试；运行：`python -m pytest backend/tests/unit/test_action_parser.py backend/tests/unit/test_mock_llm.py -q`；期望：全部通过且不联网。

- [ ] **步骤 5：两阶段审查与提交**

spec 审查确认协议不执行工具；代码审查确认 Mock 无网络依赖。提交：

```powershell
git add backend/src/safe_code_harness/core backend/src/safe_code_harness/llm backend/tests/unit
git commit -m "feat: add deterministic action protocol and mock llm"
```

**完成记录：** 实现 subagent `/root/t02_implementer` 在 `codex/t02-action-protocol` 完成，功能提交 `ba3116a`。获用户明确授权后，GREEN 阶段仅迁入旧项目 `D:\2026_summer_project\backend\src\safe_code_harness\core\action.py`、`llm\base.py` 和 `llm\mock.py` 的相关概念；人工最小适配为本任务接口：`parse_action`、`LLMClient.next_action`、`MockLLM(responses)`，未迁入旧版结构化序列或工具行为。RED：`D:\safe-code-harness-v2\.worktrees\t01-foundation\.venv\Scripts\python.exe -m pytest backend/tests/unit/test_action_parser.py -q` 得到预期 `ModuleNotFoundError: No module named 'safe_code_harness.core'`。GREEN：focused parser/Mock 测试 `6 passed in 0.02s`；协调会话在本 worktree 新建忽略的 `.venv` 后，从仓库根目录运行 `scripts/test.ps1` 与 `python -m pytest backend/tests -q`，两者均为 `7 passed in 0.01s`。独立 reviewer `/root/t02_reviewer` 的 spec 合规为 PASS、Task quality 为 APPROVE，Critical/Important 均无；其唯一 Minor 要求保留独立完整测试证据，已由上述协调复验满足。`git diff --check 9f5eab6..HEAD` 无输出，受跟踪源码 secret scan 为 clean。堆叠 draft PR 已创建：[#2](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/2)，目标为 `codex/t01-foundation`；按收尾选项 2 保留分支/worktree 等待审查，PR #1 合并后改为 `main`。

## 任务 3：策略、规则与路径沙箱

**文件：** 新建 `backend/src/safe_code_harness/governance/policy.py`、`backend/src/safe_code_harness/governance/path_sandbox.py`、`backend/src/safe_code_harness/governance/rules.py`；测试 `backend/tests/unit/test_path_sandbox.py`、`backend/tests/unit/test_rules.py`。

**接口：** `RuntimePolicy`；`PathSandbox(root).resolve(relative_path) -> Path`；`RuleEvaluator.evaluate(action) -> RuleDecision`，其 level 只能为 `allow`、`warn`、`block`。

- [ ] **步骤 1：写失败测试**

```python
def test_sandbox_blocks_workspace_escape(tmp_path: Path) -> None:
    with pytest.raises(PermissionError, match="workspace escape"):
        PathSandbox(tmp_path).resolve("../secret.txt")
```

- [ ] **步骤 2：确认红色结果**

运行：`python -m pytest backend/tests/unit/test_path_sandbox.py -q`

期望：导入错误或未阻断。

- [ ] **步骤 3：最小实现**

```python
candidate = (self.root / relative_path).resolve()
if self.root not in candidate.parents and candidate != self.root:
    raise PermissionError("workspace escape")
```

- [ ] **步骤 4：确认绿色结果**

增加 `.env`、`.git`、`secrets` 和 secret-like write 的阻断测试；运行：`python -m pytest backend/tests/unit/test_path_sandbox.py backend/tests/unit/test_rules.py -q`；期望：全部通过。

- [ ] **步骤 5：两阶段审查与提交**

spec 审查确认规则是确定性代码；代码审查确认所有文件访问先 resolve。提交：

```powershell
git add backend/src/safe_code_harness/governance backend/tests/unit/test_path_sandbox.py backend/tests/unit/test_rules.py
git commit -m "feat: add policy rules and path sandbox"
```

**完成记录：** 实现 subagent `/root/t03_implementer` 在 stacked 分支 `codex/t03-governance` 完成，初始提交 `843e50e`，审查修复提交 `49efb0c`。GREEN 阶段只迁入旧项目 `D:\2026_summer_project\backend\src\safe_code_harness\guardrails\path_sandbox.py` 与 `rules\evaluator.py` 的路径/规则逻辑；人工适配为 `governance` 包、`RuntimePolicy`、在 `resolve()` 内失败关闭及 `RuleDecision(level)`，未迁入命令护栏、审批、工具、循环或 API。RED：focused 测试预期报 `ModuleNotFoundError: safe_code_harness.governance`；初始 GREEN 为 `11 passed`、完整 backend 为 `18 passed`。独立 reviewer `/root/t03_reviewer` 发现 `.env.*` 绕过（Critical）、`sk-`/`sk-proj-` 检测及运行时 level 校验缺失（Important）；原 implementer 按测试先行新增 8 个预期失败后修复。scoped re-reviewer `/root/t03_rereviewer` 确认全部发现已解决且无新 Critical/Important；focused 为 `19 passed`、协调会话新鲜完整 backend 与 `scripts/test.ps1` 均为 `26 passed`。`git diff --check cfc589a..HEAD` 无输出，精确凭据形态扫描为 clean。堆叠 draft PR 已创建：[#3](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/3)，目标为 `codex/t02-action-protocol`；按收尾选项 2 保留分支/worktree 等待审查，上游 PR 合并后依次改为 `main`。

## 任务 4：命令护栏与审批状态机

**文件：** 新建 `backend/src/safe_code_harness/governance/command_guard.py`、`backend/src/safe_code_harness/governance/approval.py`；测试 `backend/tests/unit/test_command_guard.py`、`backend/tests/unit/test_approval.py`。

**接口：** `CommandGuard(policy).check(command) -> GuardDecision`；`ApprovalStore.create/approve/reject`；非法状态转移抛出受控异常。

- [ ] **步骤 1：写失败测试**

```python
def test_guard_blocks_destructive_command() -> None:
    result = CommandGuard(RuntimePolicy()).check("rm -rf /")
    assert result.blocked is True
    assert result.reason == "blocked command"
```

- [ ] **步骤 2：确认红色结果**

运行：`python -m pytest backend/tests/unit/test_command_guard.py -q`

期望：导入错误或断言失败。

- [ ] **步骤 3：最小实现**

```python
normalized = " ".join(command.lower().split())
return GuardDecision(blocked="rm -rf /" in normalized, reason="blocked command")
```

- [ ] **步骤 4：确认绿色结果**

增加规范化、批准后不可再次批准、拒绝后不可执行测试；运行：`python -m pytest backend/tests/unit/test_command_guard.py backend/tests/unit/test_approval.py -q`；期望：全部通过。

- [ ] **步骤 5：两阶段审查与提交**

spec 审查确认审批不直接执行工具；代码审查确认状态机不能被非法转移绕过。提交：

```powershell
git add backend/src/safe_code_harness/governance backend/tests/unit/test_command_guard.py backend/tests/unit/test_approval.py
git commit -m "feat: add command guard and approval state"
```

**完成记录：** 实现 subagent `/root/t04_implementer` 在 stacked 分支 `codex/t04-command-approval` 完成，初始提交 `4707e49`，两轮审查修复提交 `b053032`、`eea0e4d`。获用户明确授权后，仅参考旧项目 `D:\2026_summer_project\backend\src\safe_code_harness\guardrails\command_guard.py` 与 `guardrails\approval.py` 的命令规范化/决策术语；人工适配为当前 `RuntimePolicy` 的命令策略、确定性 `shlex` argv 分析和全新内存 `ApprovalStore`，未迁入 AgentLoop、工具、API、反馈或记忆。初始 RED 为缺少两个 governance 模块；初始 GREEN focused 为 `5 passed`、backend 为 `31 passed`。独立 reviewer `/root/t04_reviewer` 发现等效 `rm` 参数绕过（Critical）及 policy 未参与决策（Important）；修复先以 `9 failed, 4 passed` 复现后转为 `13 passed` / backend `42 passed`。scoped re-reviewer `/root/t04_rereviewer` 又发现 `env`、`sudo`、`command` 包装器绕过（Critical）；第二轮先以 `8 failed, 14 passed` 复现，修复后 focused command+approval `25 passed`、完整 backend `51 passed`。`/root/t04_rereviewer2` scoped re-review 批准，确认包装器、嵌套包装器、普通 `env VAR=value` 和自定义策略均符合预期。协调会话最终从本 worktree 根目录运行完整 pytest 与 `scripts/test.ps1`，均为 `51 passed`；`git diff --check b9f72cf..HEAD` 无输出。精确凭据扫描的唯一命中是既有 `test_rules.py` 的假 token fixture，不是密钥。按既有收尾选项 2，已推送并创建目标为 `codex/t03-governance` 的 [stacked draft PR #4](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/4)，保留分支/worktree 等待审查；上游 PR 合并后依次改为 `main`。

## 任务 9：凭据存储与 OpenAI 兼容 Planner

**工作区与 PR：** `codex/t09-planner-credentials` / `.worktrees/t09-planner-credentials`，独立 PR。
**文件：** 新建 `backend/src/safe_code_harness/config/planner_settings.py`、`secret_store.py`、`llm/openai_compatible.py`、`api/routes_config.py`；测试 `backend/tests/unit/test_secret_store.py`、`backend/tests/integration/test_config_api.py`。
**接口：** `SecretStore.set/get/clear`；`PlannerSettings(base_url, model, configured)`；`OpenAICompatibleLLM.next_action(context)`。Windows 适配器调用 Credential Manager；非 Windows 或适配器失败时返回明确错误且不写磁盘，不提供明文回退。

- [ ] **步骤 1：写失败测试**

```python
def test_config_response_never_contains_planner_key(client) -> None:
    client.put("/api/config/planner", json={"base_url": "https://example.test/v1", "model": "x", "api_key": "secret-value"})
    body = client.get("/api/config/planner").json()
    assert "secret-value" not in repr(body)
    assert body["key_status"] == "configured"
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_secret_store.py backend/tests/integration/test_config_api.py -q`，预期路由或安全断言失败。
- [ ] **步骤 3：最小实现**：将 key 与非秘密设置分离；配置 GET 只返回 `configured`、`masked_suffix`、`base_url`、`model`；PUT 及 clear 不记录 key；请求 LLM 时注入 key，不写入事件或内存。
- [ ] **步骤 4：确认绿色结果与重构**：补充 fake Windows API 调用、非 Windows fail-closed、清除后不可读取、空 URL/模型校验测试；运行同一命令，预期全绿。
- [ ] **步骤 5：两阶段审查与提交**：先对照 SPEC 威胁模型逐项审查流向，再审查异常消息、日志和响应；提交 `git commit -m "feat: add secure optional planner configuration"`。

**完成记录：** 新鲜 implementer `/root/t09_implementer` 在基线 `2de48a2` 完成 `3074085 feat: add secure optional planner configuration`，未使用旧项目代码。用户明确选择暂不配置真实 OpenAI-compatible key；全部验证使用 fixture key、fake Credential Manager / fake transport，未读写真实凭据且未访问网络。初始 RED 运行 `python -m pytest backend/tests/unit/test_secret_store.py backend/tests/unit/test_openai_compatible.py backend/tests/integration/test_config_api.py -q --basetemp .pytest-tmp\\task9-red`，结果 `4 failed, 4 errors`（缺少模块）；最小实现后 focused GREEN 为 `8 passed`。首轮独立安全审查发现异常链会在 traceback 中保留可能含 key 的适配器异常（Important）；修复先加入含 fixture key 的回归，RED 为 `4 failed, 10 passed`，再以六处 `raise ... from None` 隔离底层异常，提交 `51eb9c8 fix: prevent credential exception-chain leaks`。补充无 key 时 fake transport 零调用和空白 key 校验；focused GREEN `14 passed`，scoped re-review PASS，无 C/I/M。协调会话新鲜完整 backend 为 `110 passed, 1 warning`，根目录 `scripts/test.ps1` 为 `96 passed`；warning 是既有 Starlette/TestClient 对 `httpx` 的弃用警告。收尾前 `git diff --check 2de48a2..HEAD` 无输出、已变更文件精确凭据形态扫描为 `0`。依照既有 `finishing-a-development-branch` 选项 2，已推送并建立目标为 `codex/t08-api-runs` 的 [stacked draft PR #9](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/9)，保留分支/worktree 等待审查。

## 任务 10：安全项目压缩包上传与工作区注册

**工作区与 PR：** `codex/t10-workspace-upload` / `.worktrees/t10-workspace-upload`，独立 PR。
**文件：** 新建 `backend/src/safe_code_harness/workspaces/registry.py`、`upload.py`、`api/routes_workspaces.py`；测试 `backend/tests/unit/test_upload.py`、`backend/tests/integration/test_workspace_api.py`。
**接口：** `WorkspaceRegistry.create_from_zip(upload) -> Workspace`；`POST /api/workspaces/upload-zip`。每次上传解压到独立 workspace id，拒绝穿越路径、符号链接、`.env`、`.git`、secret-like 名称、超文件数、超压缩/解压大小和非 zip。

- [ ] **步骤 1：写失败测试**

```python
def test_upload_rejects_zip_slip(client, zip_with_parent_path) -> None:
    response = client.post("/api/workspaces/upload-zip", files={"file": ("bad.zip", zip_with_parent_path, "application/zip")})
    assert response.status_code == 400
    assert response.json()["code"] == "unsafe_archive_path"
```

- [ ] **步骤 2：确认红色结果**：运行 `python -m pytest backend/tests/unit/test_upload.py backend/tests/integration/test_workspace_api.py -q`，预期路由不存在或断言失败。
- [ ] **步骤 3：最小实现**：检查每个 `ZipInfo` 后才解压，路径用 `PathSandbox` 验证；出现任一失败时清理临时目录，响应不泄漏宿主路径。
- [ ] **步骤 4：确认绿色结果与重构**：增加 `.env`、符号链接位、数量/大小上限、成功注册和失败清理测试；运行同一命令，预期全绿。
- [ ] **步骤 5：两阶段审查与提交**：先审查上传不扩大工具权限，再审查归档元数据与清理路径；提交 `git commit -m "feat: add isolated safe workspace uploads"`。

**完成记录：** `/root/t10_implementer` 在基线 `2de48a2` 提交 `698e4dc`，RED 为缺少 `workspaces` 模块；RED 后仅参考旧项目 `D:\\2026_summer_project\\backend\\src\\safe_code_harness\\api\\routes_workspace.py:75-118` 的 ZipInfo/symlink 思路，重写全量预校验与安全响应。首审发现 ADS Critical、重复条目 500、生成目录遗漏和目录元数据计数绕过；均先补 RED 后以 `b546c89` 修复。scoped review 再发现 UUID 碰撞会删除既有目录；先加固定 UUID 的 RED，再以 `d15a4fd` 限定清理所有权。最终复审 PASS，无 C/I/M；协调验证 backend `127 passed, 1 warning`、`scripts/test.ps1` `113 passed`，warning 为既有 TestClient 弃用提示。凭据形态扫描为 0、diff check clean；按既有收尾选项 2，已建立目标为 `codex/t08-api-runs` 的 [stacked draft PR #10](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/10)，保留 branch/worktree 等待审查。

## 任务 11：Open Design 风格运行工作台

**工作区与 PR：** `codex/t11-workbench-ui` / `.worktrees/t11-workbench-ui`，独立 PR。
**前置门槛：** 在任务开始时实际确认或安装选定的 Open Design skill，记录版本、来源和实际使用的设计原则到 `AGENT_LOG.md`；若做不到，停止，不以“iOS 风格”替代此要求。
**文件：** 新建 `frontend/package.json`、`src/main.tsx`、`src/App.tsx`、`src/api/runs.ts`、`src/components/RunTimeline.tsx`、`src/styles/app.css`；测试 `frontend/src/components/RunTimeline.test.tsx`。
**接口：** 工作台只读加载列表四字段安全 DTO（`id`、`scenario`、`status`、`updated_at`）与时间线五字段安全 DTO（`type`、`created_at`、`level`、`display_status`、`summary_code`）；不创建运行，也不接收或展示原始事件文本、工具输出或任意摘要。卡片无障碍名称包含场景、状态和 UTC 更新时间，可供后续 E2E 使用。视觉基调采用记录中的 Open Design 原则与简洁 iOS 控件语言，但不是把文字说明堆进卡片。

- [x] **步骤 1：写失败测试**

```tsx
it("renders a blocked rule decision in the run timeline", () => {
  render(<RunTimeline events={[{ type: "rule_decision", level: "block", displayStatus: "已阻止", summaryCode: "dangerous_command_blocked", createdAt: "2026-08-08T10:00:00Z" }]} />)
  expect(screen.getByText("dangerous_command_blocked")).toBeInTheDocument()
})
```

- [x] **步骤 2：确认红色结果**：运行 `npm.cmd test -- --run RunTimeline.test.tsx`，预期测试/组件不存在。
- [x] **步骤 3：最小实现**：建立 Vite/Vitest，调用任务 8 的只读 API；实现稳定尺寸的运行列表与事件时间线，不伪造后端状态。
- [x] **步骤 4：确认绿色结果与重构**：添加空、加载、API 错误、等待审批状态；运行 `npm.cmd test` 与 `npm.cmd run build`，预期全绿。
- [x] **步骤 5：两阶段审查与提交**：先审查所有状态来自安全 DTO，再审查键盘焦点、色彩对比、文本溢出与静态响应式规则；没有执行窄屏浏览器测试，该项保持为任务 13 未完成工作；提交 `git commit -m "feat: add governed run workbench"`。

**完成记录：** Task 1 提交 `893f01a`、`63749f5`：初始 `runs` 模块缺失 RED，边界初始 GREEN 4/4；在任务 8 固定安全 DTO 后，审查发现两个 Important（异常原文泄露、读取原始 `summary`/`failure`），先有 3/6 RED 回归，修复后 focused/full GREEN 6/6。Task 2 提交 `0dcdca9`：`App`/`RunTimeline` 缺失 RED，focused GREEN 6/6、全套 GREEN 12/12。前端只读调用任务 8 的两个 GET 路由，严格投影列表四字段和时间线安全 DTO 五字段；未读取或迁入旧前端，未实现写 API、审批、配置、上传、凭据或 localStorage。Open Design 只有不可复现的历史记录：记录称当时从 `nexu-io/open-design` Windows x64 Release 安装 0.18.1 并做过 SHA-256 校验，但本地没有安装包、资产 URL 或精确摘要，不能算作当前已验证证据，绝不猜测摘要；任务只采用记录中的技能/设计系统、真实文件产出和可审计原则，未加入运行时依赖。两阶段审查最终 Critical 0、Important 0；CSS 有 `44rem` 单列断点、`min-width: 0`、`overflow-wrap: anywhere`，但没有窄屏浏览器测试，320px 证据明确留给任务 13。最终审查修复提交 `33b5ff0`：依赖 RED 为缺 lockfile 导致 `npm ci` exit 1，行为 RED 为 focused 3 files/9 tests 中 3 failed；新增 lockfile v3 并精确声明 Testing Library/jsdom 依赖，卡片可访问名称加入场景/状态/UTC 更新时间，详情以 id 绑定当前选择并覆盖乱序响应，时间显式标注 UTC。GREEN 为 focused 9/9；clean `npm ci` 成功，完整前端 4 files/15 tests passed，build 通过，credential candidate 0，staged diff check 无输出。设计和 UI 只承诺安全四字段卡片/五字段时间线，绝不恢复原始事件文本。按用户选择已创建目标为 `codex/t08-api-runs` 的 [stacked draft PR #11](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/11)，保留分支/worktree 等待审查。

## 任务 12：审批、Planner 与 ZIP 上传界面（策略扩展延后）

**工作区与 PR：** `codex/t12-settings-approval-ui` / `.worktrees/t12-settings-approval-ui`；已创建目标为 `codex/t11-workbench-ui` 的 [stacked draft PR #12](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/12)，保留 worktree 等待审查。
**实际文件：** `frontend/src/api/approvals.ts`、`planner.ts`、`workspaces.ts`，`runs.ts` 的条件 `approvalId` 投影，`ApprovalPanel.tsx`、`PlannerSettings.tsx`、`WorkspaceUpload.tsx` 及其测试、`App.tsx`/测试和样式。
**安全接口：** 只调用任务 8 的审批 POST、任务 9 的 Planner GET/PUT/DELETE、任务 10 的 ZIP POST。详情仅在 `waiting_approval` 且 wire `approval_id` 为字符串时保留 `approvalId`；Planner 仅投影四个公共字段，密码输入仅在 submit 中读取且 finally 清空；上传仅显示 `id`、`fileCount`。没有 policy route/UI、假成功、raw event、未记录写路由、key 的 JSX/state/error/URL、localStorage、服务器路径、workspace 切换或外部 Planner 调用；用户批准将策略扩展延后。

**完成记录：**

- Task 1 RED：`npm.cmd test -- --run src/api/runs.test.ts src/api/approvals.test.ts src/api/planner.test.ts src/api/workspaces.test.ts` 在安装依赖后为 4 files failed、3 tests failed、5 passed（缺三个模块与 `approvalId` 投影）；GREEN 为 4 files/16 tests passed，`npm.cmd run build` 通过。提交 `1a9074b`。
- Task 2 RED：`npm.cmd test -- --run src/components/ApprovalPanel.test.tsx src/components/PlannerSettings.test.tsx src/components/WorkspaceUpload.test.tsx src/App.test.tsx` 因组件/组合缺失 exit 1；首次 GREEN 后另有 Planner 固定错误的 focused RED，最终 focused GREEN 为 4 files/15 tests。初始全套为 10 files/34 tests，build 通过，提交 `0369c8f`。
- 两阶段审查先覆盖 spec/security，再覆盖质量/无障碍。Task 2 review 为 Critical 0、Important 2、Minor 1；两个 Important 均先新增失败回归，再由 `b22c56d` 修复：过期审批完成不会使当前选择卡住，迟到的 Planner 初始 GET 不会覆盖保存/清除结果。修复后的 focused GREEN 为 3 files/16 tests，完整前端为 10 files/37 tests，build 通过；最终 review clean。
- Task 3 独立复核了 API/JSX/状态边界、labels、键盘 button、pending disabled、错误/空反馈、面板标题、批准后的当前详情刷新、ZIP accept 限制、组件边界和 stale-detail guard；未发现 Critical 或 Important，故不改产品代码。控制器新鲜验证：`npm.cmd ci --ignore-scripts` 成功安装 176 packages；`npm.cmd test` 为 10 files/37 tests passed；`npm.cmd run build` 通过；`git diff --check codex/t11-workbench-ui..HEAD` 无输出；高置信凭据模式扫描只报告计数 `0`，不输出内容。
- 最终审查为 Critical 0、Important 0、Minor 6。最终修复波先新增全部回归；focused `npm.cmd test -- --run src/api/runs.test.ts src/api/planner.test.ts src/components/PlannerSettings.test.tsx src/components/WorkspaceUpload.test.tsx` 得到预期 RED：1 failed、28 passed，唯一失败是缺少 `正在加载 Planner 配置…`，而非字符串 `approval_id`、Planner GET/PUT/DELETE 的 non-OK/网络错误净化、Planner save/clear pending 禁用和 upload pending 禁用均验证了既有安全行为。增加最小 Planner loading state 后同命令为 4 files/29 tests GREEN；完整 `npm.cmd test` 为 10 files/48 tests，`npm.cmd run build` 通过。六项 Minor 全部关闭。
- 旧项目：Task 1/2 没有读取、复制或咨询旧项目源码。旧 `D:\2026_summer_project\frontend\src\components\ConfigPanel.tsx`、`WorkspaceUploadPanel.tsx` 和 `backend\src\safe_code_harness\api\routes_config.py` 只在设计文档中登记为未来扩展调查入口，不是任务 12 的实现指导；未迁入策略、localStorage、路径展示或自定义 workspace 事件。
- 未完成：策略 API/UI 是用户批准的延后扩展；任务 13 仍负责合并后真实本地 API、浏览器和 320px E2E。没有 PR 编号可记录。

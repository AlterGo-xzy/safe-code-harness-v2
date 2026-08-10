# SafeCodeHarness v2 进度与完整目标

更新时间：2026-08-10

本文件是下一次对话的唯一 handoff 入口。先读本文件，再读 `AGENTS.md`（若后续新增）、`PLAN.md`、`REQUIREMENTS_TRACEABILITY.md` 和 `AGENT_LOG.md`；每次编辑前运行 `git status --short`，保留未说明的用户改动。

## 当前真实状态

- 最终仓库：`https://github.com/AlterGo-xzy/safe-code-harness-v2`，公开。
- 主分支最新已推送的流程准备提交：`5dd5da3 chore: prepare isolated task worktrees`。
- 冷启动门禁：已完成。Claude Code `2.1.220` 在非 `--resume` 新会话中只 Fetch `SPEC.md` 和 `PLAN.md`，提出四项规约缺口并停止；证据在 `docs/evidence/cold-start-claude-code-task1.md`、`SPEC_PROCESS.md`，修订提交 `ecbc418`、隔离核验 `107bda3`、门禁回填 `3195ae8`。
- 任务 1 分支/worktree：`codex/t01-foundation` / `D:\safe-code-harness-v2\.worktrees\t01-foundation`。
- 任务 1 实现：`cc81e31 chore: establish offline test foundation`；后续过程记录 `30dc566`、`94b49ee`。
- 任务 1 已验证：RED 为预期 `ModuleNotFoundError: safe_code_harness`；GREEN 包含 focused pytest、editable install、独立导入和 `scripts/test.ps1`。创建 PR 前重新运行 `scripts/test.ps1`，输出 `1 passed in 0.01s`，并确认 `git diff --check origin/main...HEAD` 无输出；两阶段 reviewer 无 Critical/Important/Minor。
- 任务 1 PR：[\#1](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/1)（draft）。GitHub CLI 已由用户重新认证；连接器的历史 403 保留在日志中作为实际发生过的阻断。按 `finishing-a-development-branch`，用户选择推送并创建 PR，故保留分支/worktree 等待审查。任务 2 现可按计划启动。
- 当前源码范围：任务 1-8 的 Harness 核心与受治理运行/审批 API、任务 9 的离线安全 Planner 配置、任务 10 的安全 ZIP 上传和隔离工作区均已完成并经审查；任务 13 Task 1 已把三组真实 API 合并到同一 app factory，Task 2 的三份离线稳定 JSON 机制演示已通过三轮 scoped review，Task 3 的真实 FastAPI/Vite/Chromium 批准闭环及 320x720 视口修复也已完成初始两阶段/scoped 审查。最终全分支凭据隔离修复、复审与收尾已完成，`codex/t13-demos-e2e` 已推送并创建 [stacked draft PR #13](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/13)。任务 11 已完成只读中文运行工作台，任务 12 已在其前端基线完成审批决定、Planner 配置和 ZIP 上传的安全 UI。Task 9 的 Windows Credential Manager-only 生产存储不配置真实 API key；用户批准的策略扩展继续延后。详细续开发指令见 `HANDOFF_TO_NEXT_MODEL.md`。
- **任务 14 已收尾：** `codex/t14-ci-distribution` 已推送，并创建目标为 Task 13 的 stacked draft PR [#14](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/14)。本地 CI/OCI、loopback 安全边界、Docker healthy/API/WebUI 与审查均完成；GitHub/GitLab 外部 pipeline 和 GHCR public/匿名 pull-run 仍未验证。
- **任务 15 当前状态（优先）：** fresh implementer `/root/t15_implementer` 在 `codex/t15-release-evidence` / `D:\safe-code-harness-v2\.worktrees\t15-release-evidence` 完成本地发布资料和测试，提交 `9acb2ae`、`60528ae`、`84a10b4`；Task 14 历史文档 Minor 修复为 `93f3415`。发布文档测试先因缺“已知限制”得到 `1 failed`，后为 `1 passed`；README、MIT LICENSE、第三方声明、PR 模板与只含学生本人写作门禁/提纲的 `REFLECTION.md` 占位均已创建。110 个本地可见提交的高置信扫描只有 2 个已分类合成测试 fixture，排除后未分类候选为 0。独立两阶段审查初审总计 C/I/M=`0/0/1`，唯一 Minor 为 Task 14 PLAN 历史状态；`93f3415` 修复后的限定复审为 `0/0/0`。已把 `codex/t15-release-evidence` 推送到 NJU Git `https://git.nju.edu.cn/xzy241276010/safe-code-harness-v2.git`（远程追踪 `nju/codex/t15-release-evidence`）；首个 GitLab `unit-test` 曾因 Bookworm 系统 Node 无全局 `File` 失败，严格 TDD 修复为 `749199a`。用户提供的 GitLab 截图确认复跑均通过：pipeline `#319723` / job `#610231`（`749199a`）和 pipeline `#319724` / job `#610232`（`87b432d`）。GitHub Actions [run 31373926124](https://github.com/AlterGo-xzy/safe-code-harness-v2/actions/runs/31373926124) 也通过：`test` 与 `docker-build` 两个 job 均成功。本地验证仍为 backend `169 passed, 1 warning`、三 demo、frontend `49 passed`、build、Chromium E2E `2 passed`。Task 15 整体仍未完成：GHCR public/匿名拉取、认证 TLS 公网 URL、学生本人 1500-2500 字反思和分支收尾/PR 仍待完成。

## 不可突破的执行纪律

1. 以 `SPEC.md`、`PLAN.md`、本文件和 `REQUIREMENTS_TRACEABILITY.md` 为准；不把“已设计”写成“已完成”。
2. 每个实现 task：独立 `codex/tNN-*` branch + `.worktrees/tNN-*`、新鲜 implementer subagent、先失败测试再最小实现再重构、先 spec 合规审查再代码质量审查；Critical 未修复不得进入下一个 task。
3. 每个 task 必须把真实 RED/GREEN 命令、subagent、人工修改、审查结论、commit 和 PR 回填 `PLAN.md` 与 `AGENT_LOG.md`。
4. 每个 worktree 的 PR 建立或分支收尾前，使用 `finishing-a-development-branch`；不可因“代码已经写好”跳过 PR。
5. 不提交真实 key、`.env`、虚拟环境、`node_modules`、构建输出、测试缓存或 SDD 账本；提交前执行 secret 扫描。
6. 旧 `D:\2026_summer_project` 的既有代码可按模块复用以节省工作量，但只能在新仓库先写出同等行为的失败测试后迁入/改写；每次在 PR、PLAN、AGENT_LOG 标明旧文件路径、迁入范围和人工调整。不得整体复制，也不得让旧代码绕过本仓库的 TDD、worktree、PR 或审查证据。

## 完整目标清单：通用要求

以下条目逐项覆盖《AI4SE 期末项目·通用要求》。各项具体状态以 `REQUIREMENTS_TRACEABILITY.md` 为准。

### 项目定位与学习目标

- 使用 Superpowers 完成有工程深度、真实可用而非玩具/demo 的个人软件项目，并对全过程负责。
- 证明能以 brainstorming 形成清晰 SPEC、以 plan/subagent 长时间推进、审查并修正智能体代码。
- 达成：从模糊想法到规约/计划；端到端 agent 工作流、task 拆分和并行 worktree；TDD 与先验证后宣称；prompt/context engineering；代码评审/修正；需求到凭据治理和分发闭环；对 agentic SE 的批判性认识。

### 3.1 凭据/API key

- key 不得硬编码、不得提交到 Git 或历史、不得进入日志/终端 history/明文配置。
- 至少一种安全存储：OS keychain、KMS 或主密码加密文件；环境变量若支持须经 `.env` 加载并明确 `.env` 明文和进程环境风险，禁止把 `export` 当推荐做法。
- 首次运行使用隐藏输入安全录入；支持查看掩码状态、更新与清除，绝不回显明文。
- SPEC 安全节必须给出凭据威胁模型及对应对策。

### 3.2 分发、3.3 技术栈、3.4 深度、3.5 独立性

- 选择容器/二进制/包至少一种分发；本项目选择公开 OCI：单条 `docker build`、单条 `docker run`、公开 registry。
- README 写获取、运行、目标机安全配置 key、平台/架构/依赖限制；若改选二进制或包，补充对应平台、签名/拦截或安装命令。
- SPEC 说明语言、框架、LLM 供应商和理由。
- 无硬性行数目标；必须真实可用、至少三个职责清晰模块、可一键测试，并经得起新机器凭据/分发验证。
- 个人独立承担 PM、架构、reviewer 和最终责任。

### 3.6 工具链

- 安装并实际使用 Superpowers；如实记录七步流程的偏离及理由。
- TDD 硬性执行红-绿-重构，禁止先实现后补测试。
- 有 WebUI 时实际使用或如实说明 Open Design 设计系统/skill；不可以假称使用。
- 鼓励比较多种 agent，当前已使用 Codex Desktop 主开发和 Claude Code 冷启动。

### 4.0 总前提与 4.1-4.5 规约阶段

- 完整流程必须可追溯：`brainstorming` → `writing-plans` → `using-git-worktrees` → `subagent-driven-development`/`executing-plans` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`。
- 在 SPEC、PLAN 和不同类型冷启动验证完成前禁止实现代码；该前置门禁已通过，证据见上。
- brainstorming 分块追问并经用户确认；writing-plans 产生 2-5 分钟颗粒度、文件路径、验证步骤明确的计划。
- `SPEC.md` 必须包含：问题/用户/价值；至少 5 个 INVEST 用户故事；模块化输入/行为/输出/边界/错误；性能/安全含威胁模型/可用性/可观测性；架构/数据流/外部依赖；数据模型/关系/约束；key 生命周期及分发/平台；技术选型含 UI/Open Design；客观验收；风险和未决问题；A 的领域与机制设计。
- `PLAN.md` 每个 task 必含目标、文件、实现要点、失败测试与验证，并显示依赖和可并行部分。
- `SPEC_PROCESS.md` 必须保留 brainstorming 问题/修正、至少三轮对话节选及决策、采纳/拒绝、反思；冷启动必须记录第二 agent 的暂停问题、误读判定、产出差距、修订前后 diff。
- 冷启动必须是不同 agent 类型、全新 session、无历史/memory、仅给 SPEC+PLAN、从 1-2 task 推进并在不确定时暂停；该项已由 Claude Code 证据完成。

### 4.6-4.11 实现、仓库、测试、日志、分发、部署

- 每个独立功能/大模块创建 worktree 和一个 PR；每 task 使用新鲜 subagent。
- 每 task 完成后先 spec 合规检查再代码质量检查；Critical 必须修复；所有 task 后用 `finishing-a-development-branch` 决定 merge/PR/保留/丢弃。
- GitHub 必须公开；有多次意图清晰 commit/PR，不能单次提交所有代码；提交前扫描凭据。
- commit message/PR 描述要注明 subagent 和人工改动；PLAN 完成即填 commit hash；持续维护 AGENT_LOG。
- 有一键测试命令；GitHub Actions 每次 push 运行测试；选容器时 CI 也构建镜像，选二进制时建议产物。
- AGENT_LOG 每条包括时间/task、Superpowers skill、关键 prompt/context、subagent 输出或 hash、人工干预和教训。
- README 包含分发命令、目标机 key 安全配置、已知限制；CI 包含相应构建。
- 服务端项目要在截止前提供可访问公网 WebUI；README 写部署架构/CI/CD，使用可控成本免费额度。

### 第五部分最终交付

- 使用同一个 NJU Git 仓库链接提交：`SPEC.md`、`PLAN.md`、`SPEC_PROCESS.md`、完整无凭据源码及规范 commit/PR 历史、分发产物/说明、完整 README、`AGENT_LOG.md`、`.gitlab-ci.yml`（必须有 `unit-test` job）、最后一次通过的 CI/CD 记录、学生本人 1500-2500 字 `REFLECTION.md`、可访问 WebUI URL。
- README 必含项目简介、安装、运行、分发命令、目录结构和安全边界。
- 反思报告必须由学生本人完成；建议覆盖 Superpowers 哪些有效/形式化、TDD 对 AI 协作的影响、subagent 自主边界、task 粒度、规约不清案例、prompt/context 策略、凭据与分发的工程认识、重做改进和对方法论的批判。

### 第六部分学术规范与第七部分资源

- 个人手写的核心算法/函数需在文件或函数顶部明确注释；第三方代码遵守许可证并在 README 列出；反思不得由 AI 代写，AI 润色须标注。
- 过程参考并实际核对 Superpowers 文档、Open Design（UI）、所选 agent 的 Superpowers 文档、系统凭据存储及所选分发文档。

## 完整目标清单：A · Coding Agent Harness

### A.1-A.3 领域定义与四类机制

- 交付的是 `Agent = LLM + Harness` 中自实现的 Harness：代码实现决策封装、动作/工具、上下文/记忆、治理/HITL/沙箱、反馈闭环和声明式配置。
- 面向 coding：读写代码、运行命令和测试，测试结果驱动有限修正。
- SPEC 明确：可执行动作/工具、客观反馈信号、必须暂停审批的危险动作和边界、跨会话记忆及按需提供方案。

### A.4 实现边界与深度

- 开发工具可以使用 Codex/Claude/Superpowers，但最终产物不能调用宿主 agent loop、skill、治理 hook 充当自身功能。
- 必须自实现主循环：上下文 → 单次 LLM 调用 → 动作解析 → 分发 → 结果回灌 → 停机。
- 必须有可注入 Mock 的 LLM 抽象，可接真实供应商的单次补全 API；允许 HTTP/解析/向量等底层零件。
- 禁止 LangChain `AgentExecutor`、AutoGen、CrewAI、LlamaIndex agent 或任何高层 agent runner。
- 反馈校验器和危险动作护栏必须是确定性代码而不是提示词；移除真实 LLM 后，工具、治理、反馈、记忆、停机仍可被 mock/stub LLM 的确定性测试验证。
- 六维均有可运行最低实现；本项目主贡献选择治理，深入实现规则、路径沙箱、命令护栏、HITL 状态机、策略和事件证据。若改为记忆重点，存储/检索也必须自实现。

### A.5-A.7 规格、测试与交付

- SPEC 含“领域与机制设计”，说明 coding 反馈、危险动作、工具、记忆、重点维度与代码实现方式。
- 所有 Harness 核心机制拥有离线、确定性、Mock/stub LLM 单测，不依赖网络或真实 key。
- 提交可重复机制演示：危险动作被护栏拦截；注入失败导致反馈闭环改变下一动作；治理主贡献的确定性行为。
- 最终源码包含自实现 harness 内核（主循环、工具分发、治理、反馈等）、Mock LLM 单测和上述机制演示，并由 README 索引。

## 后续执行顺序

1. 任务 1 的 draft PR 已建立并完成收尾决定；在 [PR #1](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/1) 保留 `codex/t01-foundation` worktree 以处理审查反馈。
2. 任务 2 已在 `codex/t02-action-protocol` / `D:\safe-code-harness-v2\.worktrees\t02-action-protocol` 完成：`ba3116a` 实现确定性动作协议与 Mock LLM，用户授权迁入旧项目三个相关源文件概念并作最小接口适配；RED、GREEN、独立双审查、完整离线测试、diff 检查和 secret scan 已完成。后续只读审计已将误插到任务 13 的完成记录移回任务 2。因任务 1 PR 尚未合并，已创建目标为 `codex/t01-foundation` 的 [stacked draft PR #2](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/2)；保留分支/worktree 等待审查，PR #1 合并后改为 `main`。
3. 任务 3 已在 `codex/t03-governance` / `D:\safe-code-harness-v2\.worktrees\t03-governance` 完成：`843e50e` 与 `49efb0c` 实现并加固确定性规则/路径沙箱；旧项目仅复用两个明确源文件的相关逻辑。初次独立审查发现 1 Critical、2 Important，均经新失败测试、修复及 scoped re-review 清零；完整 backend 与一键测试均为 `26 passed`。已创建目标为 `codex/t02-action-protocol` 的 [stacked draft PR #3](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/3)，保留该 worktree 等待审查；上游 PR 合并后依次改为 `main`。后续从任务 4 继续，任何代码复用均须记录旧文件路径、迁入范围与人工调整。
4. 任务 4 已在 `codex/t04-command-approval` / `D:\safe-code-harness-v2\.worktrees\t04-command-approval` 完成：`4707e49` 新增确定性命令护栏和非执行审批状态机；审查后以 `b053032` 修复等效 `rm` 参数及 policy 配置问题，并以 `eea0e4d` 修复 `env`、`sudo`、`command` 包装器绕过。旧项目仅参考两个 `guardrails` 文件的命令规范化/术语，未迁入 loop、工具或 API。所有修复先有真实 RED 回归；独立复审最终批准。协调会话新鲜完整 pytest 与一键测试均为 `51 passed`；已创建目标为 `codex/t03-governance` 的 [stacked draft PR #4](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/4)，保留该分支/worktree 等待审查，上游 PR 合并后依次改为 `main`。
5. 任务 5 已在 `codex/t05-tools` / `D:\safe-code-harness-v2\.worktrees\t05-tools` 完成：`2795539` 新增受 `PathSandbox` 和 `CommandGuard` 约束的显式工具分派；所有测试先 RED，独立审查无 Critical/Important，协调会话一键测试为 `58 passed`。已创建目标为 `codex/t04-command-approval` 的 [stacked draft PR #5](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/5)，保留该分支/worktree 等待审查。
6. 任务 6 已在 `codex/t06-feedback-memory` / `D:\safe-code-harness-v2\.worktrees\t06-feedback-memory` 完成：`cc5b974` 与 `6b9676b` 实现并加固确定性反馈和有界脱敏记忆；两项 Important 经失败回归与 scoped re-review 修复，一键测试为 `77 passed`。已创建目标为 `codex/t05-tools` 的 [stacked draft PR #6](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/6)，保留分支/worktree 等待审查。
7. 任务 7 已在 `codex/t07-agent-loop` / `D:\safe-code-harness-v2\.worktrees\t07-agent-loop` 完成：自实现循环的审批与恢复边界经两轮 Critical 修复和 scoped re-review；完整 backend/tests 为 `89 passed`。已创建目标为 `codex/t06-feedback-memory` 的 [stacked draft PR #7](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/7)，保留分支/worktree 等待审查。
8. 任务 8 已在 `codex/t08-api-runs` 完成：`974d73b` 增加运行/审批 API，`7afa279` 修复 TestClient 直接依赖声明；任务 11 所需列表和时间线安全 DTO 后续由 `afd42ae`、`6fd3237` 补齐。独立复审通过，最新完整 backend `100 passed`、一键 unit `88 passed`。已创建目标为 `codex/t07-agent-loop` 的 [stacked draft PR #8](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/8)，保留分支/worktree 等待审查。
9. 任务 9 已在 `codex/t09-planner-credentials` 完成：`3074085` 增加仅 Windows Credential Manager 的 Planner 凭据存储、掩码配置 API 与可注入传输的 OpenAI-compatible LLM；`51eb9c8` 修复异常链潜在泄露。未配置、读取、输出或使用真实 key，未访问网络。独立复审最终 PASS；协调会话完整 backend `110 passed`、一键 unit `96 passed`。已创建目标为 `codex/t08-api-runs` 的 [stacked draft PR #9](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/9)，保留分支/worktree 等待审查。
10. 任务 10 已在 `codex/t10-workspace-upload` 完成：`698e4dc`、`b546c89`、`d15a4fd` 实现并加固安全 ZIP 上传与隔离工作区。全量预校验拒绝 ZIP Slip、ADS、NUL、UNC、Windows 设备名、重复条目、symlink、敏感/缓存目录以及成员/大小超限；仅清理当前上传创建的目录并保留 UUID 碰撞下的旧工作区，API 返回固定且不含服务器路径的 400。最终独立审查 PASS、无 C/I/M；完整 backend `127 passed`、一键 unit `113 passed`。已创建目标为 `codex/t08-api-runs` 的 [stacked draft PR #10](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/10)，保留分支/worktree 等待审查。
11. 任务 11 已在 `codex/t11-workbench-ui` / `D:\safe-code-harness-v2\.worktrees\t11-workbench-ui` 实现只读中文工作台：`893f01a` 建立 typed read-only frontend boundary，`63749f5` 以先失败回归修复两个 Important API 安全边界，`0dcdca9` 完成卡片总览、选中时间线和状态 UI，最终审查修复提交 `33b5ff0`。前端只读调用任务 8 的两个 GET 路由，严格消费列表四字段和时间线固定五字段 DTO，未读取或迁入旧前端，也未加入创建运行、审批、配置、上传、凭据或 localStorage。最终修复新增 lockfile 与声明齐全的测试依赖、完整卡片 accessible name、详情 id/乱序保护和 UTC 标注；clean install 后完整前端 4 files/15 tests passed，build 通过。独立 scoped re-review 为 Critical 0、Important 0、Minor 1；Minor 的两处旧详细计划示例已以文档最小修正关闭，不改变运行时行为或安全边界。Open Design 只有一条不可复现的历史记录：记录称当时从 `nexu-io/open-design` Windows x64 Release 安装 `0.18.1` 并做过 SHA-256 校验，但本地没有安装包、资产 URL 或精确摘要，不能算作当前已验证证据，绝不猜测摘要。CSS 有 `44rem` 单列断点、`min-width: 0` 与 `overflow-wrap: anywhere`；没有窄屏浏览器测试，320px 证据仍为任务 13 未完成项。已按用户选择创建目标为 `codex/t08-api-runs` 的 [stacked draft PR #11](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/11)，保留分支/worktree 等待审查。
12. 任务 12 已在 `codex/t12-settings-approval-ui` / `D:\safe-code-harness-v2\.worktrees\t12-settings-approval-ui` 完成：`1a9074b` 建立只投影安全字段的审批、Planner 和 ZIP API 边界；`0369c8f` 增加三个治理面板；Task 2 两项 Important 先有失败回归，再由 `b22c56d` 修复当前选择的审批刷新与 Planner 初始加载覆盖。Task 1/2 没有读取、复制或咨询旧项目源码；旧 `ConfigPanel.tsx`、`WorkspaceUploadPanel.tsx` 和 `routes_config.py` 只是未来扩展调查入口，明确不是任务 12 的实现指导。后续最终审查为 Critical 0、Important 0、Minor 6：补齐非字符串 `approval_id`、Planner 三方法 HTTP/网络固定错误、Planner 初始加载、Planner mutation pending 和 ZIP upload pending 回归，并纠正日期、旧项目和状态归属文档。focused RED 为 1 failed/28 passed，证明缺少 Planner 加载提示；其他新增测试直接验证既有安全行为。最小实现后 focused 为 4 files/29 tests，完整前端为 10 files/48 tests，build 通过；六项 Minor 全部关闭。已按要求创建目标为 `codex/t11-workbench-ui` 的 [stacked draft PR #12](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/12)，保留分支/worktree 等待审查；用户批准的策略扩展和任务 13 的真实 API/浏览器/320px E2E 仍未完成。
13. 任务 13 Task 1-2 的 API 集成、三份稳定 JSON demo 和三轮审查已经完成，历史提交与证据保持不变。Task 3 fresh implementer `/root/t13_task3_implementer` 以缺 Playwright、缺 uvicorn 和 Vitest 误收 E2E spec 的真实 RED 驱动 `e18422e`；Chromium 真实执行批准闭环。Task 4 quality review 的视口 Important 由 `/root/t13_task3_viewport_fixer` 先得按钮底边超出 720px 的 RED，再由 `5ed4bd3` 修复并通过 scoped 双阶段 re-review。最终全分支审查又发现默认 E2E server 的 Planner GET 触及生产 Credential Manager 边界；本修复波先以缺少 `e2e_app` 的自动回归 RED，再提交 `7d66d98`，用进程内空 SecretStore 注入现有 factory 并保持真实 API/browser 流程、无 interception。当前本地验证为 E2E `2 passed`、前端 `48 passed`/build、backend `159 passed, 1 warning`；最终 scoped re-review 为 Critical 0、Important 0、Minor 2，两个文档 Minor 已修正。Task 14/15 和策略扩展均未开始。

## 2026-08-10 最新 Task 13 状态（优先于上方各阶段的历史文字）

Task 13 的 Task 1-3、320px 修复及本地控制验证均已实现。最终全分支 reviewer 仍发现一个凭据隔离 Important：Playwright 原先启动生产 `main:app`，前端正常的 Planner 初始 GET 会经 `PlannerConfiguration.snapshot()` → `SecretStore.get()` 懒加载 Windows Credential Manager。运行时探针实际记录 1 次构造尝试和固定 503。`/root/t13_final_fix` 严格 TDD：新增回归先因 `safe_code_harness.api.e2e_app` 不存在得到 RED，再以 `7d66d98 fix: isolate browser e2e credentials` 增加初始为空的进程内 fake、注入现有 `create_app()`，并让 Playwright 启动该专用入口；生产 `main:app` 与 Task 9 存储保持不变。修复后 focused `1 passed`、完整 backend `159 passed, 1 warning`（既有 Starlette/TestClient 弃用警告）、三项 demo 稳定 JSON、clean frontend install 后 unit `10 files/48 tests`、build、真实 Chromium E2E `2 passed`。clean install 仍报告 5 个上游审计风险（3 moderate、1 high、1 critical），未执行 `--force`。最终 scoped re-review 为 Critical 0、Important 0、Minor 2；追踪矩阵、表格、设计和 README findings 已同步，两个文档 Minor 已修正。Task 13 尚未 push、尚无 PR #13；在只读文档复核与最终 diff/凭据扫描完成前不得运行分支收尾；Task 14、15 和用户延后的策略扩展仍未开始。
## 2026-08-10 Task 13 分支收尾更新

Task 13 最终验证为 backend `159 passed, 1 warning`、三份稳定 JSON demo、前端 48 tests/build、Chromium E2E `2 passed`、diff/高置信凭据候选均为 0。已推送 `codex/t13-demos-e2e`，并创建目标为 `codex/t12-settings-approval-ui` 的 [stacked draft PR #13](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/13)；保留 branch/worktree 以处理审查反馈。任务 14、15 和延后的策略扩展仍未开始。
## 2026-08-10 Task 14 分支收尾更新

Task 14 已完成本地 CI/容器实现、验证与审查，并已推送 `codex/t14-ci-distribution`；已创建目标为 `codex/t13-demos-e2e` 的 [stacked draft PR #14](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/14)。保留 branch/worktree 以处理审查反馈。外部 GitHub/GitLab CI、GHCR 发布/公开性/匿名 pull-run 与任务 15 仍未验证或完成。

# SafeCodeHarness v2 进度与完整目标

更新时间：2026-08-04

本文件是下一次对话的唯一 handoff 入口。先读本文件，再读 `AGENTS.md`（若后续新增）、`PLAN.md`、`REQUIREMENTS_TRACEABILITY.md` 和 `AGENT_LOG.md`；每次编辑前运行 `git status --short`，保留未说明的用户改动。

## 当前真实状态

- 最终仓库：`https://github.com/AlterGo-xzy/safe-code-harness-v2`，公开。
- 主分支最新已推送的流程准备提交：`5dd5da3 chore: prepare isolated task worktrees`。
- 冷启动门禁：已完成。Claude Code `2.1.220` 在非 `--resume` 新会话中只 Fetch `SPEC.md` 和 `PLAN.md`，提出四项规约缺口并停止；证据在 `docs/evidence/cold-start-claude-code-task1.md`、`SPEC_PROCESS.md`，修订提交 `ecbc418`、隔离核验 `107bda3`、门禁回填 `3195ae8`。
- 任务 1 分支/worktree：`codex/t01-foundation` / `D:\safe-code-harness-v2\.worktrees\t01-foundation`。
- 任务 1 实现：`cc81e31 chore: establish offline test foundation`；后续过程记录 `30dc566`、`94b49ee`。
- 任务 1 已验证：RED 为预期 `ModuleNotFoundError: safe_code_harness`；GREEN 包含 focused pytest、editable install、独立导入和 `scripts/test.ps1`。创建 PR 前重新运行 `scripts/test.ps1`，输出 `1 passed in 0.01s`，并确认 `git diff --check origin/main...HEAD` 无输出；两阶段 reviewer 无 Critical/Important/Minor。
- 任务 1 PR：[\#1](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/1)（draft）。GitHub CLI 已由用户重新认证；连接器的历史 403 保留在日志中作为实际发生过的阻断。按 `finishing-a-development-branch`，用户选择推送并创建 PR，故保留分支/worktree 等待审查。任务 2 现可按计划启动。
- 当前源码范围：只有任务 1 的包基座与测试入口；尚未开始 AgentLoop、MockLLM、治理、工具、反馈、记忆、API、凭据、上传、前端、CI、容器或部署。

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
2. 开始任务 2：动作协议、运行模型和 Mock LLM。先新 worktree，再 fresh subagent、RED/GREEN、双评审、PR。
3. 按 `PLAN.md` 依赖图完成任务 3-15；任何代码复用按本文件第 6 条执行。
4. 在每个 task、PR、CI、容器、部署、NJU Git、反思发生时即时更新本文件、`PLAN.md`、`AGENT_LOG.md` 和 `REQUIREMENTS_TRACEABILITY.md`。

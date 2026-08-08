# 要求追踪矩阵

本文件把《AI4SE 期末项目·通用要求》与《AI4SE 期末项目·A·Coding Agent Harness》逐项映射到仓库证据。状态只使用四种含义：`已完成并验证`、`部分完成`、`已设计，尚未执行`、`外部阻断`。没有对应的真实证据不得标记完成。

## 通用要求

| 编号 | 正式要求 | 当前状态 | 目标证据与完成门槛 |
| --- | --- | --- | --- |
| G-3.1-1 | key 不得硬编码、提交、写日志/history/明文配置 | 部分完成（任务 9、12） | `3074085`、`51eb9c8`：Credential Manager-only、掩码 API、异常链/503 不含 fixture key；Task 12 密钥仅在密码输入提交中读取、finally 清空，且不进 JSX/state/error/URL/localStorage。最终 Git 历史扫描仍待完成。 |
| G-3.1-2 | 至少一种安全存储；说明环境变量/`.env` 明文风险 | 部分完成（任务 9） | Windows Credential Manager 适配器、fake adapter 和非 Windows fail-closed 测试已完成；README 的环境变量/`.env` 风险说明仍待任务 14/15。 |
| G-3.1-3 | 首次安全录入，支持查看状态、更新、清除，不回显 | 部分完成（任务 9、12） | Task 9 API 支持掩码状态、更新、清除且无明文/异常链泄露；Task 12 有隐藏输入、初始加载、保存/清除、mutation pending 禁用和固定错误单测。任务 13 仍需针对合并后真实 API 的浏览器 E2E。 |
| G-3.1-4 | SPEC 有凭据威胁模型与对策 | 已完成并验证 | `SPEC.md` 8.1。 |
| G-3.2-1 | 选择分发形态；容器须单条 build/run 且推送公开 registry | 已设计，尚未执行 | Dockerfile、GHCR publish workflow、公开 `docker pull` 和全新机器运行证据。 |
| G-3.2-2 | README 写获取、运行、目标机安全 key 配置、限制 | 已设计，尚未执行 | README 分发/安全章节和命令验证。 |
| G-3.3 | SPEC 说明技术栈、LLM 供应商与理由 | 已完成并验证 | `SPEC.md` 9；可选 Planner 明确为 OpenAI-compatible 单次动作提供方。 |
| G-3.4-1 | 真实、非玩具项目，至少三个职责清晰模块 | 已设计，尚未执行 | Core、Governance、Tools、Feedback/Memory、API、WebUI 六类模块及可运行工作流。 |
| G-3.4-2 | 一键测试；新机器验证凭据与分发 | 已设计，尚未执行 | `make test`、CI、OCI pull/run、README 新机器步骤。 |
| G-3.5 | 个人负责 PM/架构/reviewer | 已完成并验证 | 用户作为最终决策者；PR 日志记录人工决策与修改。 |
| G-3.6-1 | 安装并使用 Superpowers | 已完成并验证 | 本会话实际使用 `brainstorming`；后续每一步在 `AGENT_LOG.md` 记录对应官方 skill。 |
| G-3.6-2 | 如实遵循七步流程；偏离须记录 | 部分完成（任务 1-8、11、12） | `AGENT_LOG.md` 记录任务 1-8、11、12 的 worktree、fresh分段实现、TDD、两阶段审查、修复和分支状态；Task 12 最终审查的 6 个 Minor 已关闭，已按用户选择完成 [stacked draft PR #12](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/12)，策略扩展仍为用户批准的延后范围。 |
| G-3.6-3 | TDD：红-绿-重构，不得先实现后补测 | 部分完成（任务 1-8、11、12） | `PLAN.md` 与 `AGENT_LOG.md` 保留 Task 12 API/面板及最终修复的真实 RED/GREEN；最终 focused RED 为 1 failed/28 passed（缺 Planner 初始加载提示），最小实现后为 4 files/29 tests，完整前端新鲜验证为 10 files/48 tests。 |
| G-3.6-4 | 有 UI 时说明 Open Design 系统与 skill | 部分完成（任务 11） | 任务 11 的历史记录称当时从 `nexu-io/open-design` Windows x64 Release 安装 `0.18.1` 并做过 SHA-256 校验，但本地未保留安装包、资产 URL 或精确摘要，当前不可复现，不能算作已验证证据，且绝不猜测摘要。任务只采用记录中的技能/设计系统、真实文件产出、可审计原则，未将运行时纳入产品依赖。 |
| G-4.1 | brainstorming 分块确认后 writing-plans | 已完成并验证 | 本会话逐段确认、`SPEC_PROCESS.md` 四轮节选；用户批准 SPEC 后才可调用 `writing-plans`。 |
| G-4.2 | `SPEC.md` 的十类内容及 A 赛道附加节 | 已完成并验证 | `SPEC.md` 1-11，含“领域与机制设计”。 |
| G-4.3 | `PLAN.md`：细任务、文件、要点、失败测试、依赖/并行 | 已完成并验证 | `PLAN.md` 已由 `writing-plans` 生成并在任务 1-4 记录实际 RED/GREEN、审查与提交。 |
| G-4.4 | `SPEC_PROCESS.md`：关键问题、至少三轮节选、采纳/拒绝、反思 | 已完成并验证 | `SPEC_PROCESS.md` 的五次迭代、四轮节选、采纳/拒绝与 brainstorming 反思。 |
| G-4.5 | 不同类型陌生 agent 的冷启动，且只给 SPEC+PLAN | 已完成并验证 | Claude Code `2.1.220` 非 `--resume` 启动，仅 Fetch `SPEC.md` 与 `PLAN.md` 两个 raw URL，发现四项规约缺口后暂停；原始转录、工具轨迹、修订前后 diff 见 `docs/evidence/cold-start-claude-code-task1.md`、`SPEC_PROCESS.md` 与 commit `ecbc418`。 |
| G-4.6-1 | 每个独立模块一个 worktree/PR | 部分完成（任务 1-5） | 任务 1-5 均在独立 worktree 完成并各有 draft PR；后续模块继续。 |
| G-4.6-2 | 每 task 一个新鲜 subagent | 部分完成（任务 1-5） | `AGENT_LOG.md` 记录任务 1-5 的 fresh implementer、reviewer 与输出。 |
| G-4.6-3 | 红-绿-重构 | 部分完成（任务 1-5） | 每个任务记录 RED/GREEN；任务 4 的两轮安全审查问题均新增失败回归后修复。 |
| G-4.6-4 | 每 task 先 spec 合规审查，再代码质量审查 | 部分完成（任务 1-5、12） | Task 12 先审 spec/security 边界，再审质量/无障碍；Task 2 的 Critical 0、Important 2、Minor 1 在 fix round 后 clean。后续最终审查为 Critical 0、Important 0、Minor 6，六项已用覆盖、Planner loading 和文档一致性最小修正全部关闭。 |
| G-4.6-5 | `finishing-a-development-branch` 决定分支去向 | 部分完成（任务 1-5） | 任务 1-5 均按 skill 的既有选项 2 保留 branch/worktree 并建立 draft PR。 |
| G-4.7-1 | 公开 GitHub、完整 commit/PR 历史、无凭据 | 部分完成（任务 1-4） | 公开仓库、任务 1-3 draft PR、任务 4 分支及精确凭据扫描；仍需后续 task 和最终历史扫描。 |
| G-4.7-2 | commit/PR 标注 subagent 和人工修改 | 部分完成（任务 1-4） | 任务 1-4 的 PR/日志均已标注 subagent、人工调整与旧代码复用边界。 |
| G-4.7-3 | PLAN 持续标注完成与 commit hash | 部分完成（任务 1-4） | `PLAN.md` 已填任务 1-4 实际提交和证据；后续 task 继续。 |
| G-4.7-4 | 维护 `AGENT_LOG.md` | 部分完成（任务 1-4） | 日志已追加任务 1-4 的时间、agent、验证、审查、人工动作和教训。 |
| G-4.8 | 一键测试、GitHub Actions push 测试、容器构建 | 部分完成（本地一键测试） | `scripts/test.ps1` 在任务 1-4 本地验证；CI/容器构建留待任务 14。 |
| G-4.9 | AGENT_LOG 包含时间、task、skill、prompt、输出、人工干预、教训 | 部分完成（任务 1-4） | D0 及任务 1-4 日志包含上述字段；后续持续维护。 |
| G-4.10 | README 分发与 key 配置，CI 对应构建 | 已设计，尚未执行 | README、Docker/GHCR workflow 和 pull/run 验证。 |
| G-4.11 | 服务端项目提供截止前可访问 WebUI、说明部署与 CI/CD | 已设计，尚未执行 | Render 或等效部署 URL、README 架构、部署验证。 |
| G-5-1 | 同一个 NJU Git 链接提交所有交付 | 外部阻断 | 等待用户提供 NJU Git 远程地址；推送后记录 URL/commit。 |
| G-5-2 | `.gitlab-ci.yml` 有名为 `unit-test` 的 job，最后 CI/CD 为 pass | 已设计，尚未执行 | GitLab pipeline 绿灯 URL/截图或平台记录。 |
| G-5-3 | `REFLECTION.md` 为学生本人 1500-2500 字 | 外部阻断 | 由学生独立写作；AI 仅可润色并记录边界。 |
| G-5-4 | 线上 WebUI URL | 已设计，尚未执行 | 已部署 URL 与可访问性检查。 |
| G-6 | 学术规范：个人手写核心处注释、第三方许可证、反思不可 AI 代写 | 已设计，尚未执行 | 源码中学生手写标注（如有）、README 许可证清单、学生本人反思。 |

## A 赛道要求

| 编号 | 正式要求 | 当前状态 | 目标证据与完成门槛 |
| --- | --- | --- |
| A-1/A-2 | 交付 Coding Agent Harness：决策封装、工具、上下文/记忆、治理、反馈、配置 | 部分完成（任务 2-5） | 动作协议、离线 Mock、治理和受控工具已实现；主循环、反馈/记忆、配置、集成测试与运行时间线仍待后续任务。 |
| A-3 | SPEC 说明动作、客观反馈、危险动作、记忆 | 已完成并验证 | `SPEC.md` 3、4。 |
| A-4-A | 自实现主循环、可注入 Mock LLM；不得使用高层 agent 编排框架 | 部分完成（任务 2） | `ba3116a` 提供自实现 `Action`、`parse_action`、单次 `LLMClient.next_action` 与离线 `MockLLM`；完整 `AgentLoop` 留待任务 7。 |
| A-4-B | 反馈与危险动作必须是确定性代码，而非提示词 | 部分完成（任务 3-4） | `843e50e`/`49efb0c` 提供路径/secret 规则和失败关闭沙箱；`4707e49`、`b053032`、`eea0e4d` 提供确定性命令解析/阻断与审批状态机；反馈校验器和机制演示仍待后续任务。 |
| A-4-C | 移除真实 LLM 后所有核心机制仍可单测 | 部分完成（任务 2-5） | 已实现动作、治理和工具的离线确定性单测；完整 loop、反馈/记忆与集成测试仍待后续任务。 |
| A-4-D | 六维最低实现，并选择一个深入维度 | 部分完成（任务 3-4） | 治理主贡献已实现规则、路径沙箱、命令护栏与 HITL 审批状态机；其余五维仍待后续任务。 |
| A-5 | SPEC 增加“领域与机制设计” | 已完成并验证 | `SPEC.md` 4。 |
| A-6-1 | Mock/stub LLM 的确定性核心机制单测 | 已设计，尚未执行 | 测试目录按机制分类，CI 离线运行。 |
| A-6-2 | 三项机制演示：危险阻断、失败反馈改变动作、主贡献行为 | 已设计，尚未执行 | 可重复脚本或测试，保存预期输出/断言。 |
| A-7 | 提交自实现 Harness 内核、Mock 单测、机制演示 | 已设计，尚未执行 | 最终源码、测试、演示和 README 索引。 |

## 实现前绝对门禁

1. 用户明确批准 `SPEC.md` 的本轮修订。
2. `writing-plans` 产生并提交符合 G-4.3 的 `PLAN.md`。
3. 使用不同类型的新 agent，仅凭 SPEC+PLAN 完成冷启动验证，并据结果修订 SPEC/PLAN。
4. 为所有实现模块建立 worktree/PR 与 task 编号。前三项任一缺失时，不得编写实现代码。

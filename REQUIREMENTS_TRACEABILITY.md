# 要求追踪矩阵

本文件把《AI4SE 期末项目·通用要求》与《AI4SE 期末项目·A·Coding Agent Harness》逐项映射到仓库证据。状态只使用三种含义：`已完成并验证`、`已设计，尚未执行`、`外部阻断`。没有对应的真实证据不得标记完成。

## 通用要求

| 编号 | 正式要求 | 当前状态 | 目标证据与完成门槛 |
| --- | --- | --- | --- |
| G-3.1-1 | key 不得硬编码、提交、写日志/history/明文配置 | 已设计，尚未执行 | `SPEC.md` 8.1；实现后的 secret 扫描、API/日志测试、提交前 Git 历史扫描。 |
| G-3.1-2 | 至少一种安全存储；说明环境变量/`.env` 明文风险 | 已设计，尚未执行 | Windows Credential Manager 适配器和确定性 Mock 测试；README 说明 `.env` 风险与不推荐命令行 `export`。 |
| G-3.1-3 | 首次安全录入，支持查看状态、更新、清除，不回显 | 已设计，尚未执行 | 隐藏输入、掩码状态、更新/清除 API 与 E2E；测试断言 API 响应无明文。 |
| G-3.1-4 | SPEC 有凭据威胁模型与对策 | 已完成并验证 | `SPEC.md` 8.1。 |
| G-3.2-1 | 选择分发形态；容器须单条 build/run 且推送公开 registry | 已设计，尚未执行 | Dockerfile、GHCR publish workflow、公开 `docker pull` 和全新机器运行证据。 |
| G-3.2-2 | README 写获取、运行、目标机安全 key 配置、限制 | 已设计，尚未执行 | README 分发/安全章节和命令验证。 |
| G-3.3 | SPEC 说明技术栈、LLM 供应商与理由 | 已完成并验证 | `SPEC.md` 9；可选 Planner 明确为 OpenAI-compatible 单次动作提供方。 |
| G-3.4-1 | 真实、非玩具项目，至少三个职责清晰模块 | 已设计，尚未执行 | Core、Governance、Tools、Feedback/Memory、API、WebUI 六类模块及可运行工作流。 |
| G-3.4-2 | 一键测试；新机器验证凭据与分发 | 已设计，尚未执行 | `make test`、CI、OCI pull/run、README 新机器步骤。 |
| G-3.5 | 个人负责 PM/架构/reviewer | 已完成并验证 | 用户作为最终决策者；PR 日志记录人工决策与修改。 |
| G-3.6-1 | 安装并使用 Superpowers | 已完成并验证 | 本会话实际使用 `brainstorming`；后续每一步在 `AGENT_LOG.md` 记录对应官方 skill。 |
| G-3.6-2 | 如实遵循七步流程；偏离须记录 | 已设计，尚未执行 | G-4.1 至 G-4.6 的真实时间序列与本矩阵；任何例外写入日志。 |
| G-3.6-3 | TDD：红-绿-重构，不得先实现后补测 | 已设计，尚未执行 | 每个任务 PR 的失败命令、最小实现、通过命令和重构记录。 |
| G-3.6-4 | 有 UI 时说明 Open Design 系统与 skill | 已设计，尚未执行 | `SPEC.md` 9 已指定；前端任务开始前确认/安装 skill，并记录实际调用或诚实替代证据。 |
| G-4.1 | brainstorming 分块确认后 writing-plans | 已完成并验证 | 本会话逐段确认、`SPEC_PROCESS.md` 四轮节选；用户批准 SPEC 后才可调用 `writing-plans`。 |
| G-4.2 | `SPEC.md` 的十类内容及 A 赛道附加节 | 已完成并验证 | `SPEC.md` 1-11，含“领域与机制设计”。 |
| G-4.3 | `PLAN.md`：细任务、文件、要点、失败测试、依赖/并行 | 已设计，尚未执行 | 用户确认 SPEC 后由 `writing-plans` 生成并提交。 |
| G-4.4 | `SPEC_PROCESS.md`：关键问题、至少三轮节选、采纳/拒绝、反思 | 已完成并验证 | `SPEC_PROCESS.md` 的五次迭代、四轮节选、采纳/拒绝与 brainstorming 反思。 |
| G-4.5 | 不同类型陌生 agent 的冷启动，且只给 SPEC+PLAN | 已完成并验证 | Claude Code `2.1.220` 非 `--resume` 启动，仅 Fetch `SPEC.md` 与 `PLAN.md` 两个 raw URL，发现四项规约缺口后暂停；原始转录、工具轨迹、修订前后 diff 见 `docs/evidence/cold-start-claude-code-task1.md`、`SPEC_PROCESS.md` 与 commit `ecbc418`。 |
| G-4.6-1 | 每个独立模块一个 worktree/PR | 已设计，尚未执行 | PLAN 为每个模块标注 worktree 和独立 PR；不在 `main` 直接实现。 |
| G-4.6-2 | 每 task 一个新鲜 subagent | 已设计，尚未执行 | 每个任务 `AGENT_LOG.md` 记录新 agent id、prompt、输出和 commit。 |
| G-4.6-3 | 红-绿-重构 | 已设计，尚未执行 | 每个 PR 的测试记录与审查。 |
| G-4.6-4 | 每 task 先 spec 合规审查，再代码质量审查 | 已设计，尚未执行 | 两份独立审查结论；Critical 未清零不得继续。 |
| G-4.6-5 | `finishing-a-development-branch` 决定分支去向 | 已设计，尚未执行 | 每个完成模块的 skill 调用、PR 结论和合并证据。 |
| G-4.7-1 | 公开 GitHub、完整 commit/PR 历史、无凭据 | 已设计，尚未执行 | 公开仓库已创建；后续用 secret scan、分支 PR、commit 说明建立完整历史。 |
| G-4.7-2 | commit/PR 标注 subagent 和人工修改 | 已设计，尚未执行 | PR 模板和每个任务的 commit/PR 描述。 |
| G-4.7-3 | PLAN 持续标注完成与 commit hash | 已设计，尚未执行 | PLAN task checklist 逐项更新。 |
| G-4.7-4 | 维护 `AGENT_LOG.md` | 已设计，尚未执行 | 当前日志是起点；每一次 task、审查、外部验证即时追加。 |
| G-4.8 | 一键测试、GitHub Actions push 测试、容器构建 | 已设计，尚未执行 | Makefile、CI 后端/前端/E2E/Docker jobs 和最终绿灯。 |
| G-4.9 | AGENT_LOG 包含时间、task、skill、prompt、输出、人工干预、教训 | 已设计，尚未执行 | D0 已有；所有后续任务必须填满字段。 |
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
| A-1/A-2 | 交付 Coding Agent Harness：决策封装、工具、上下文/记忆、治理、反馈、配置 | 已设计，尚未执行 | 六模块源码、集成测试与运行时间线。 |
| A-3 | SPEC 说明动作、客观反馈、危险动作、记忆 | 已完成并验证 | `SPEC.md` 3、4。 |
| A-4-A | 自实现主循环、可注入 Mock LLM；不得使用高层 agent 编排框架 | 部分完成（任务 2） | `ba3116a` 提供自实现 `Action`、`parse_action`、单次 `LLMClient.next_action` 与离线 `MockLLM`；完整 `AgentLoop` 留待任务 7。 |
| A-4-B | 反馈与危险动作必须是确定性代码，而非提示词 | 已设计，尚未执行 | Feedback evaluator、rule/guardrail 单测和机制演示。 |
| A-4-C | 移除真实 LLM 后所有核心机制仍可单测 | 已设计，尚未执行 | 离线单元/集成测试禁止网络和真实 key。 |
| A-4-D | 六维最低实现，并选择一个深入维度 | 已设计，尚未执行 | 六模块实现；治理的规则、沙箱和 HITL 状态机作为主贡献。 |
| A-5 | SPEC 增加“领域与机制设计” | 已完成并验证 | `SPEC.md` 4。 |
| A-6-1 | Mock/stub LLM 的确定性核心机制单测 | 已设计，尚未执行 | 测试目录按机制分类，CI 离线运行。 |
| A-6-2 | 三项机制演示：危险阻断、失败反馈改变动作、主贡献行为 | 已设计，尚未执行 | 可重复脚本或测试，保存预期输出/断言。 |
| A-7 | 提交自实现 Harness 内核、Mock 单测、机制演示 | 已设计，尚未执行 | 最终源码、测试、演示和 README 索引。 |

## 实现前绝对门禁

1. 用户明确批准 `SPEC.md` 的本轮修订。
2. `writing-plans` 产生并提交符合 G-4.3 的 `PLAN.md`。
3. 使用不同类型的新 agent，仅凭 SPEC+PLAN 完成冷启动验证，并据结果修订 SPEC/PLAN。
4. 为所有实现模块建立 worktree/PR 与 task 编号。前三项任一缺失时，不得编写实现代码。

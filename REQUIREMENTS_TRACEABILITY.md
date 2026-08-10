# 要求追踪矩阵

本文件把《AI4SE 期末项目·通用要求》与《AI4SE 期末项目·A·Coding Agent Harness》逐项映射到仓库证据。状态只使用四种含义：`已完成并验证`、`部分完成`、`已设计，尚未执行`、`外部阻断`。没有对应的真实证据不得标记完成。

## 通用要求

| 编号 | 正式要求 | 当前状态 | 目标证据与完成门槛 |
| --- | --- | --- | --- |
| G-3.1-1 | key 不得硬编码、提交、写日志/history/明文配置 | 部分完成（任务 9、12） | `3074085`、`51eb9c8`：Credential Manager-only、掩码 API、异常链/503 不含 fixture key；Task 12 密钥仅在密码输入提交中读取、finally 清空，且不进 JSX/state/error/URL/localStorage。最终 Git 历史扫描仍待完成。 |
| G-3.1-2 | 至少一种安全存储；说明环境变量/`.env` 明文风险 | 部分完成（任务 9、14） | Windows Credential Manager 适配器和非 Windows fail-closed 测试已完成；Task 14 README 已说明容器进程内存、平台 secret 环境可见风险及禁止提交 `.env`/命令行明文。托管平台 secret 与最终部署仍待 Task 15。 |
| G-3.1-3 | 首次安全录入，支持查看状态、更新、清除，不回显 | 部分完成（任务 9、12、13 Task 1） | Task 9 API 支持掩码状态、更新、清除且无明文/异常链泄露；Task 12 有隐藏输入、初始加载、保存/清除、mutation pending 禁用和固定错误单测。Task 13 Task 1 已验证合并后真实 Planner API 返回固定四字段 DTO；Task 3 浏览器只覆盖审批，不把它误写成 Planner 凭据浏览器验证。 |
| G-3.1-1 | key 不得硬编码、提交、写日志/history/明文配置 | 部分完成（任务 12 前端边界） | `SPEC.md` 8.1；Task 12 密钥仅在密码输入的提交中读取、finally 清空，且不进 JSX/state/error/URL/localStorage；对 `codex/t11-workbench-ui..HEAD` 的高置信凭据扫描只报告计数 0。仍需最终 Git 历史扫描。 |
| G-3.1-2 | 至少一种安全存储；说明环境变量/`.env` 明文风险 | 已设计，尚未执行 | Windows Credential Manager 适配器和确定性 Mock 测试；README 说明 `.env` 风险与不推荐命令行 `export`。 |
| G-3.1-3 | 首次安全录入，支持查看状态、更新、清除，不回显 | 部分完成（任务 12 前端单测） | Task 12 有隐藏输入、掩码后缀、初始加载、保存/清除、mutation pending 禁用和不回显单测；Planner GET/PUT/DELETE 的 non-OK 与网络异常均验证只返回固定中文错误。任务 13 仍需针对合并后真实 API 的浏览器 E2E，安全存储本身也仍须按后续任务完成。 |
| G-3.1-4 | SPEC 有凭据威胁模型与对策 | 已完成并验证 | `SPEC.md` 8.1。 |
| G-3.2-1 | 选择分发形态；容器须单条 build/run 且推送公开 registry | 部分完成（任务 14 本地） | `0f2b35f` 提供并实际验证单条 Docker build、Compose healthy/API/WebUI；默认分支 GHCR workflow 已配置。GHCR push、package public 设置及未登录 pull/run 是外部证据，尚未完成。 |
| G-3.2-2 | README 写获取、运行、目标机安全 key 配置、限制 | 已完成并验证 | README 已包含 loopback-only build/run、未来 GHCR pull/run、Windows Credential Manager、容器进程内存/平台 secret 环境风险、无认证边界与公网认证/TLS gateway 前提、目录及外部限制；本地容器 Planner 初始为空且不烘焙 key。 |
| G-3.3 | SPEC 说明技术栈、LLM 供应商与理由 | 已完成并验证 | `SPEC.md` 9；可选 Planner 明确为 OpenAI-compatible 单次动作提供方。 |
| G-3.4-1 | 真实、非玩具项目，至少三个职责清晰模块 | 已完成并验证 | Action/LLM、Governance、Tools、Feedback/Memory、AgentLoop、API/WebUI 均已有职责分离的实现与离线测试；任务 13 又以真实本地 API/浏览器串联运行与审批。 |
| G-3.4-2 | 一键测试；新机器验证凭据与分发 | 部分完成（任务 14 本地） | `Makefile test` 默认使用 README 安装的 `.venv/bin/python` 并串联 backend/frontend；当前 Windows 无 GNU Make，未虚称运行，但两个实际 target 命令分别为 backend `168 passed`、frontend `48 passed`。本地 OCI loopback build/healthy/API/WebUI 已验证；新机器与公开 pull 仍待 Task 15。 |
| G-3.5 | 个人负责 PM/架构/reviewer | 已完成并验证 | 用户作为最终决策者；PR 日志记录人工决策与修改。 |
| G-3.6-1 | 安装并使用 Superpowers | 已完成并验证 | 本会话实际使用 `brainstorming`；后续每一步在 `AGENT_LOG.md` 记录对应官方 skill。 |
| G-3.6-2 | 如实遵循七步流程；偏离须记录 | 部分完成（任务 1-14 实现） | Task 13 已以 PR #13 收尾。Task 14 初审 C/I/M=`0/3/3`，fix `1434a64` 后 scoped spec/security 与质量 re-review 均通过；最终 review C/I/M=`0/0/1`，本次正关闭唯一文档 Minor。无 GNU Make、外部 CI/GHCR 未验证均如实保留。 |
| G-3.6-3 | TDD：红-绿-重构，不得先实现后补测 | 部分完成（任务 1-14 实现） | Task 14 初始 RED/GREEN 为 `7 failed`→`7 passed`；审查修复又先得到 Make/loopback/dotenv/CI gate 的 `4 failed, 5 passed`，再转为 `9 passed`。完整 backend 当前 `168 passed, 1 warning`、frontend `48 passed`、E2E `2 passed`。 |
| G-3.6-4 | 有 UI 时说明 Open Design 系统与 skill | 部分完成（任务 11、13 Task 3） | 任务 11 的 Open Design 安装历史仍不可复现且不猜测摘要；Task 13 Task 3 已用真实 Chromium 在 320x720 验证批准控件可见及 DOM 无横向溢出，未把静态 CSS 检查替代为浏览器证据。 |
| G-4.1 | brainstorming 分块确认后 writing-plans | 已完成并验证 | 本会话逐段确认、`SPEC_PROCESS.md` 四轮节选；用户批准 SPEC 后才可调用 `writing-plans`。 |
| G-4.2 | `SPEC.md` 的十类内容及 A 赛道附加节 | 已完成并验证 | `SPEC.md` 1-11，含“领域与机制设计”。 |
| G-4.3 | `PLAN.md`：细任务、文件、要点、失败测试、依赖/并行 | 已完成并验证 | `PLAN.md` 已由 `writing-plans` 生成并在任务 1-4 记录实际 RED/GREEN、审查与提交。 |
| G-4.4 | `SPEC_PROCESS.md`：关键问题、至少三轮节选、采纳/拒绝、反思 | 已完成并验证 | `SPEC_PROCESS.md` 的五次迭代、四轮节选、采纳/拒绝与 brainstorming 反思。 |
| G-4.5 | 不同类型陌生 agent 的冷启动，且只给 SPEC+PLAN | 已完成并验证 | Claude Code `2.1.220` 非 `--resume` 启动，仅 Fetch `SPEC.md` 与 `PLAN.md` 两个 raw URL，发现四项规约缺口后暂停；原始转录、工具轨迹、修订前后 diff 见 `docs/evidence/cold-start-claude-code-task1.md`、`SPEC_PROCESS.md` 与 commit `ecbc418`。 |
| G-4.6-1 | 每个独立模块一个 worktree/PR | 部分完成（任务 1-14） | 任务 1-13 均有独立 worktree/draft PR；任务 14 已在独立 worktree 提交实现，待审查后 push/PR。 |
| G-4.6-2 | 每 task 一个新鲜 subagent | 部分完成（任务 1-14） | `AGENT_LOG.md` 记录任务 1-14 的 fresh implementer、reviewer、修复 agent 与输出；Task 14 implementer 为 `/root/t14_implementer`。 |
| G-4.6-3 | 红-绿-重构 | 部分完成（任务 1-14） | 任务 1-14 均记录真实 RED/GREEN；Task 14 初始 `7 failed`→`7 passed`，review fix 为 `4 failed, 5 passed`→`9 passed`。 |
| G-4.6-4 | 每 task 先 spec 合规审查，再代码质量审查 | 部分完成（任务 1-14） | 任务 1-13 已审查闭环；Task 14 初审 C/I/M=`0/3/3`，`1434a64` 后两项 scoped re-review 均通过；最终 review C/I/M=`0/0/1`，唯一文档状态 Minor 正由本次提交修正并待只读确认。 |
| G-4.6-5 | `finishing-a-development-branch` 决定分支去向 | 部分完成（任务 1-14） | 任务 1-13 已保留 branch/worktree 并建立 draft PR；Task 14 必须在两阶段审查通过后再执行该 skill。 |
| G-4.7-1 | 公开 GitHub、完整 commit/PR 历史、无凭据 | 部分完成（任务 1-14） | 公开仓库和任务 1-13 stacked draft PR（含 PR #13）已存在；Task 14 本地提交 `0f2b35f`/`1434a64` 待复审和 PR，最终历史扫描仍待交付前执行。 |
| G-4.7-2 | commit/PR 标注 subagent 和人工修改 | 部分完成（任务 1-14） | 任务 1-13 PR 与任务 1-14 日志均记录 subagent、人工调整及旧代码边界；Task 14 PR 尚未创建。 |
| G-4.7-3 | PLAN 持续标注完成与 commit hash | 部分完成（任务 1-14） | `PLAN.md` 已持续回填任务 1-14 的提交、RED/GREEN、审查 findings、修复与未完成外部状态。 |
| G-4.7-4 | 维护 `AGENT_LOG.md` | 部分完成（任务 1-14） | 日志已追加任务 1-14 的时间、agent、验证、审查、人工动作和教训；后续任务继续。 |
| G-4.8 | 一键测试、GitHub Actions push 测试、容器构建 | 部分完成（任务 14 本地） | `Makefile test` 使用仓库 venv；GitHub push/PR 测试+E2E+Docker job 已实现，GHCR publish 依赖成功的默认分支 push CI。本地 Docker loopback build/healthy 通过；外部 Actions 尚未运行。 |
| G-4.9 | AGENT_LOG 包含时间、task、skill、prompt、输出、人工干预、教训 | 部分完成（任务 1-14） | D0 及任务 1-14 日志包含上述字段；后续持续维护。 |
| G-4.10 | README 分发与 key 配置，CI 对应构建 | 部分完成（任务 14 本地） | README 与 Docker/GHCR workflow 已实现；本地 loopback build/run/API/WebUI/key 边界及无认证 gateway 前提已验证/记录。公开 GHCR pull/run 仍待外部发布和 package public 设置。 |
| G-4.11 | 服务端项目提供截止前可访问 WebUI、说明部署与 CI/CD | 已设计，尚未执行 | Render 或等效部署 URL、README 架构、部署验证。 |
| G-5-1 | 同一个 NJU Git 链接提交所有交付 | 外部阻断 | 等待用户提供 NJU Git 远程地址；推送后记录 URL/commit。 |
| G-5-2 | `.gitlab-ci.yml` 有名为 `unit-test` 的 job，最后 CI/CD 为 pass | 部分完成（任务 14 配置） | `.gitlab-ci.yml` 已有顶层精确 `unit-test`，运行 backend、demos、frontend unit/build；GitLab 外部 pipeline 尚未触发，最后一次 pass 证据仍待 Task 15。 |
| G-5-3 | `REFLECTION.md` 为学生本人 1500-2500 字 | 外部阻断 | 由学生独立写作；AI 仅可润色并记录边界。 |
| G-5-4 | 线上 WebUI URL | 已设计，尚未执行 | 已部署 URL 与可访问性检查。 |
| G-6 | 学术规范：个人手写核心处注释、第三方许可证、反思不可 AI 代写 | 已设计，尚未执行 | 源码中学生手写标注（如有）、README 许可证清单、学生本人反思。 |

## A 赛道要求

| 编号 | 正式要求 | 当前状态 | 目标证据与完成门槛 |
| --- | --- | --- | --- |
| A-1/A-2 | 交付 Coding Agent Harness：决策封装、工具、上下文/记忆、治理、反馈、配置 | 已完成并验证 | 任务 2-9 已实现动作/LLM 抽象、工具、上下文/有界脱敏记忆、规则/沙箱/命令护栏/HITL、确定性反馈、自实现 AgentLoop 与声明式 Planner 配置；任务 8/13 提供运行、审批和集成 API/时间线。 |
| A-3 | SPEC 说明动作、客观反馈、危险动作、记忆 | 已完成并验证 | `SPEC.md` 3、4。 |
| A-4-A | 自实现主循环、可注入 Mock LLM；不得使用高层 agent 编排框架 | 已完成并验证 | 任务 2 提供单次 `LLMClient`/`MockLLM` 与动作协议；任务 7 实现 context→单次 LLM→解析→治理/分派→结果回灌→停机/审批恢复的 `AgentLoop`，未引入高层 agent runner。 |
| A-4-B | 反馈与危险动作必须是确定性代码，而非提示词 | 已完成并验证 | 任务 3-4 的规则、路径沙箱、命令护栏/HITL 与任务 6 的反馈校验器均为确定性代码；任务 13 demos 在 Mock LLM 下复现危险阻断和失败反馈改变下一动作。 |
| A-4-C | 移除真实 LLM 后所有核心机制仍可单测 | 已完成并验证 | 动作、治理、工具、反馈、记忆、完整 loop、审批恢复、API 与三项机制 demo 均由 Mock/stub LLM 离线确定性测试覆盖；真实 Planner/key/网络不是测试前提。 |
| A-4-D | 六维最低实现，并选择一个深入维度 | 已完成并验证 | 六维最低实现均已落地：决策封装、动作/工具、上下文/记忆、治理/HITL/沙箱、反馈闭环、声明式配置；治理主贡献另有规则、路径/命令护栏、审批状态机和事件证据的深入实现。 |
| A-5 | SPEC 增加“领域与机制设计” | 已完成并验证 | `SPEC.md` 4。 |
| A-6-1 | Mock/stub LLM 的确定性核心机制单测 | 已完成并验证 | `backend/tests` 以 `MockLLM`/stub 覆盖 Harness 核心；三 demo 保持稳定 JSON。Task 14 fix 后完整 backend `168 passed, 1 warning`，CI 已定义相同离线测试，但外部 CI 成功状态不作为本地证据。 |
| A-6-2 | 三项机制演示：危险阻断、失败反馈改变动作、主贡献行为 | 已完成并验证 | 三份稳定 JSON demo 已审查通过：护栏阻断、MockLLM 反馈闭环改变动作、真实 `RunService` 的等待审批→批准→执行。真实 FastAPI/Vite/Chromium E2E `2 passed`；320x720 初始视口 RED（底边 `1327.4375 > 720`）由 `5ed4bd3` 的最小修复关闭，scoped 双阶段 re-review C/I/M `0/0/0`。上述均为本地证据；Task 14 CI 复现仍待执行。 |
| A-7 | 提交自实现 Harness 内核、Mock 单测、机制演示 | 部分完成 | 自实现 Harness、Mock 单测和三项 demo 已在 draft PR #13；Task 14 本地 `0f2b35f`/`1434a64` 增加并加固 CI/OCI 分发。当前 backend `168 passed, 1 warning`、frontend `48`、build/E2E `2 passed`，scoped re-review 已通过；Task 14 文档 Minor 确认/PR 与最终交付仍待完成。 |

## 实现前绝对门禁

1. 用户明确批准 `SPEC.md` 的本轮修订。
2. `writing-plans` 产生并提交符合 G-4.3 的 `PLAN.md`。
3. 使用不同类型的新 agent，仅凭 SPEC+PLAN 完成冷启动验证，并据结果修订 SPEC/PLAN。
4. 为所有实现模块建立 worktree/PR 与 task 编号。前三项任一缺失时，不得编写实现代码。

## 2026-08-10 PR #10/#11 集成追踪（已完成，历史记录）

G-4.6-1/2 当前事实：PR #10 已以 `696214d`、PR #11 已以 `622c472` 合并；两者均有完整回归、diff/marker/credential scan clean 和 fresh C/I/M=`0/0/0` 证据。Task12 仍待其自身复审和 GitHub 状态回读。

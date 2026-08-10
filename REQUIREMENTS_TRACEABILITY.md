# 要求追踪矩阵

本文件把《AI4SE 期末项目·通用要求》与《AI4SE 期末项目·A·Coding Agent Harness》逐项映射到仓库证据。状态只使用四种含义：`已完成并验证`、`部分完成`、`已设计，尚未执行`、`外部阻断`。没有对应的真实证据不得标记完成。

## 通用要求

| 编号 | 正式要求 | 当前状态 | 目标证据与完成门槛 |
| --- | --- | --- | --- |
| G-3.1-1 | key 不得硬编码、提交、写日志/history/明文配置 | 部分完成（任务 9、12、15 本地） | Credential Manager-only、掩码 API 和前端清空边界已验证。Task 15 对 110 个本地可见提交作高置信扫描：2 个候选均为脱敏/阻断测试的合成 fixture，排除后 tracked/history 未分类候选均为 0；最终合并/外部同步后仍须再扫描。 |
| G-3.1-2 | 至少一种安全存储；说明环境变量/`.env` 明文风险 | 部分完成（任务 9、14-15 本地） | Windows Credential Manager 适配器和非 Windows fail-closed 测试已完成；README 已说明容器进程内存、平台 secret 环境可见风险及禁止提交 `.env`/命令行明文。托管平台 secret 仍待真实部署核验。 |
| G-3.1-3 | 首次安全录入，支持查看状态、更新、清除，不回显 | 部分完成（任务 9、12、13 Task 1） | Task 9 API 支持掩码状态、更新、清除且无明文/异常链泄露；Task 12 有隐藏输入、初始加载、保存/清除、mutation pending 禁用和固定错误单测。Task 13 Task 1 已验证合并后真实 Planner API 返回固定四字段 DTO；Task 3 浏览器只覆盖审批，不把它误写成 Planner 凭据浏览器验证。 |
| G-3.1-4 | SPEC 有凭据威胁模型与对策 | 已完成并验证 | `SPEC.md` 8.1。 |
| G-3.2-1 | 选择分发形态；容器须单条 build/run 且推送公开 registry | 已完成并验证 | `0f2b35f` 提供单条 Docker build/run；main `c633003` CI 的 Docker build 已通过，成功后的 GHCR workflow `31389335469` 已发布。空 Docker 配置实际匿名拉取 SHA tag，digest `sha256:efebd5cc0277b73ddbfbecf00ad843af1c127b3ba31e0395f3de6b46825694d2`，并在 loopback 容器验证 `/`、`/api/runs` 都为 200。 |
| G-3.2-2 | README 写获取、运行、目标机安全 key 配置、限制 | 已完成并验证 | `9acb2ae`/`60528ae`：中文 README 包含源码获取、本地/OCI 运行、未来 GHCR pull/run、Windows Credential Manager、容器进程内存/平台 secret 风险、无认证与公网 authentication/TLS gateway 前提、目录和“已知限制”；未把 GHCR 外部结果写成已完成。 |
| G-3.3 | SPEC 说明技术栈、LLM 供应商与理由 | 已完成并验证 | `SPEC.md` 9；可选 Planner 明确为 OpenAI-compatible 单次动作提供方。 |
| G-3.4-1 | 真实、非玩具项目，至少三个职责清晰模块 | 已完成并验证 | Action/LLM、Governance、Tools、Feedback/Memory、AgentLoop、API/WebUI 均已有职责分离的实现与离线测试；任务 13 又以真实本地 API/浏览器串联运行与审批。 |
| G-3.4-2 | 一键测试；新机器验证凭据与分发 | 部分完成（任务 14-15 本地） | `Makefile test` 使用 README 安装的 `.venv/bin/python` 串联 backend/frontend；当前 Windows 无 GNU Make，未虚称运行，两个实际 target 为 backend `169 passed`、frontend `48 passed`。本地 OCI loopback build/healthy/API/WebUI 已验证；独立新机器和公开 pull 仍为外部阻断。 |
| G-3.5 | 个人负责 PM/架构/reviewer | 已完成并验证 | 用户作为最终决策者；PR 日志记录人工决策与修改。 |
| G-3.6-1 | 安装并使用 Superpowers | 已完成并验证 | 本会话实际使用 `brainstorming`；后续每一步在 `AGENT_LOG.md` 记录对应官方 skill。 |
| G-3.6-2 | 如实遵循七步流程；偏离须记录 | 部分完成（任务 1-15 本地实现） | Task 14 已以 draft PR #14 收尾。Task 15 fresh subagent 已完成本地 RED/GREEN、回归和两阶段审查；初审 C/I/M=`0/0/1`，`93f3415` 后限定复审 `0/0/0`。本机无 GNU Make、外部 CI/GHCR/部署/NJU、学生反思与分支收尾均如实保留为未完成。 |
| G-3.6-3 | TDD：红-绿-重构，不得先实现后补测 | 部分完成（任务 1-15 本地实现） | Task 15 发布文档契约为 `1 failed`→`1 passed`；完整回归发现 Task 14 README 安全契约 RED 后最小恢复。当前 backend `169 passed, 1 warning`、frontend `48 passed`、E2E `2 passed`。 |
| G-3.6-4 | 有 UI 时说明 Open Design 系统与 skill | 部分完成（任务 11、13 Task 3） | 任务 11 的 Open Design 安装历史仍不可复现且不猜测摘要；Task 13 Task 3 已用真实 Chromium 在 320x720 验证批准控件可见及 DOM 无横向溢出，未把静态 CSS 检查替代为浏览器证据。 |
| G-4.1 | brainstorming 分块确认后 writing-plans | 已完成并验证 | 本会话逐段确认、`SPEC_PROCESS.md` 四轮节选；用户批准 SPEC 后才可调用 `writing-plans`。 |
| G-4.2 | `SPEC.md` 的十类内容及 A 赛道附加节 | 已完成并验证 | `SPEC.md` 1-11，含“领域与机制设计”。 |
| G-4.3 | `PLAN.md`：细任务、文件、要点、失败测试、依赖/并行 | 已完成并验证 | `PLAN.md` 已由 `writing-plans` 生成并在任务 1-4 记录实际 RED/GREEN、审查与提交。 |
| G-4.4 | `SPEC_PROCESS.md`：关键问题、至少三轮节选、采纳/拒绝、反思 | 已完成并验证 | `SPEC_PROCESS.md` 的五次迭代、四轮节选、采纳/拒绝与 brainstorming 反思。 |
| G-4.5 | 不同类型陌生 agent 的冷启动，且只给 SPEC+PLAN | 已完成并验证 | Claude Code `2.1.220` 非 `--resume` 启动，仅 Fetch `SPEC.md` 与 `PLAN.md` 两个 raw URL，发现四项规约缺口后暂停；原始转录、工具轨迹、修订前后 diff 见 `docs/evidence/cold-start-claude-code-task1.md`、`SPEC_PROCESS.md` 与 commit `ecbc418`。 |
| G-4.6-1 | 每个独立模块一个 worktree/PR | 部分完成（任务 1-15 本地） | 任务 1-14 均有独立 worktree/stacked draft PR；任务 15 位于独立 worktree且已推送至 NJU Git，但尚未建 PR 或完成分支收尾。 |
| G-4.6-2 | 每 task 一个新鲜 subagent | 部分完成（任务 1-15 本地） | `AGENT_LOG.md` 记录任务 1-14 的 fresh implementer/reviewer/fix agent；Task 15 fresh implementer 为 `/root/t15_implementer`，独立两阶段审查及限定复审均已执行。 |
| G-4.6-3 | 红-绿-重构 | 部分完成（任务 1-15 本地） | 任务 1-14 的 RED/GREEN 已记录；Task 15 发布契约为 `1 failed`→`1 passed`，并用现有 Task 14 安全契约的回归 RED 驱动双语修复。 |
| G-4.6-4 | 每 task 先 spec 合规审查，再代码质量审查 | 已完成并验证（任务 1-15 本地阶段） | Task 15 两阶段初审总计 C/I/M=`0/0/1`，唯一 PLAN 历史 Minor 由 `93f3415` 修复，限定复审 `0/0/0`；没有未关闭本地 finding。 |
| G-4.6-5 | `finishing-a-development-branch` 决定分支去向 | 部分完成（任务 1-15 本地） | 任务 1-14 均按该 skill 保留 branch/worktree 并建立 draft PR；Task 15 两阶段审查已通过，但外部门槛和分支收尾仍未完成。 |
| G-4.7-1 | 公开 GitHub、完整 commit/PR 历史、无凭据 | 部分完成（任务 1-15 本地） | 公开仓库和任务 1-14 stacked draft PR（含 PR #14）已存在；Task 15 本地提交 `9acb2ae`/`60528ae`/`84a10b4`/`93f3415`/`1215581` 已推送到 NJU Git，110 commits 扫描排除两处合成 fixture 后未分类候选为 0；Task 15 GitHub push/PR、最终合并/外部同步后仍须复扫。 |
| G-4.7-2 | commit/PR 标注 subagent 和人工修改 | 部分完成（任务 1-15 本地） | 任务 1-14 PR 与任务 1-15 日志记录 subagent、人工调整及旧代码边界；Task 15 PR 尚未创建。 |
| G-4.7-3 | PLAN 持续标注完成与 commit hash | 部分完成（任务 1-15 本地） | `PLAN.md` 已回填任务 15 本地提交、RED/GREEN、回归、初审 `0/0/1`、`93f3415` 修复和限定复审 `0/0/0`；PR/外部 URL 后继续更新。 |
| G-4.7-4 | 维护 `AGENT_LOG.md` | 部分完成（任务 1-15 本地） | 日志已追加任务 1-15 的时间、agent、验证、审查、修复、人工动作和教训；Task 15 外部结果与收尾仍待追加。 |
| G-4.8 | 一键测试、GitHub Actions push 测试、容器构建 | 已完成并验证 | `Makefile test` 使用仓库 venv；GitHub push/PR 测试+E2E+Docker job 已实现。最新 main `c633003` 的 [run 31389169084](https://github.com/AlterGo-xzy/safe-code-harness-v2/actions/runs/31389169084) 成功执行 backend、demos、frontend、Chromium E2E 与 docker-build。 |
| G-4.9 | AGENT_LOG 包含时间、task、skill、prompt、输出、人工干预、教训 | 部分完成（任务 1-15 本地） | D0 及任务 1-15 本地日志包含上述字段和本地审查闭环；外部核验与分支收尾后继续更新。 |
| G-4.10 | README 分发与 key 配置，CI 对应构建 | 已完成并验证 | README、Docker/GHCR workflow 与 key 安全边界均已记录；最新 main CI 通过后 GHCR publish `31389335469` 成功，匿名 pull/run 已实际验证。Railway Mock 的无认证限制仍明确保留。 |
| G-4.11 | 服务端项目提供截止前可访问 WebUI、说明部署与 CI/CD | 部分完成（Mock 演示已验证） | 用户确认 Railway `https://safe-code-harness-v2-production.up.railway.app` 已部署，浏览器截图显示首页“暂无运行记录”，协调会话只读 HTTP 根请求返回 `200`；README 说明部署/CI/CD。该公共 HTTPS 站没有应用认证且未配置真实 Planner key，只能作为无敏感数据的 Mock 演示；认证/TLS 安全生产边界列为后续扩展。 |
| G-5-1 | 同一个 NJU Git 链接提交所有交付 | 部分完成 | 用户提供的 NJU Git `https://git.nju.edu.cn/xzy241276010/safe-code-harness-v2.git` 已可访问；2026-08-10 已推送 `codex/t15-release-evidence`（HEAD 当时为 `1215581`）并设上游。最终合并、Task 15 PR 与其余外部证据仍待。 |
| G-5-2 | `.gitlab-ci.yml` 有名为 `unit-test` 的 job，最后 CI/CD 为 pass | 已完成并验证 | `.gitlab-ci.yml` 有顶层精确 `unit-test`，运行 backend、demos、frontend unit/build。初始 job #610227（pipeline #319719）因 Bookworm Node 缺少全局 `File` 失败；TDD 修复 `749199a` 后，用户提供的 GitLab 页面确认 job #610231（pipeline #319723，`749199a`）及 job #610232（pipeline #319724，`87b432d`）均为通过。 |
| G-5-3 | `REFLECTION.md` 为学生本人 1500-2500 字 | 已完成并验证（中文汉字口径） | 用户提供的学生本人正文已原样写入，协调会话未代写或润色；中文汉字统计 `1583`，落在 1500–2500。若课程平台采取不同统计口径，学生提交前仍须本人确认。 |
| G-5-4 | 线上 WebUI URL | 已完成并验证（Mock 演示范围） | 用户确认 Railway URL `https://safe-code-harness-v2-production.up.railway.app`，并提供首页空状态截图。它满足可访问 WebUI URL 的演示证据；无认证、无真实 key、不得上传敏感工作区，安全生产部署是后续扩展。 |
| G-6 | 学术规范：个人手写核心处注释、第三方许可证、反思不可 AI 代写 | 部分完成 | `LICENSE`、`THIRD_PARTY_NOTICES.md` 和 README 许可证索引已完成；学生本人反思及最终人工学术规范复核仍未完成。 |

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
| A-6-1 | Mock/stub LLM 的确定性核心机制单测 | 已完成并验证 | `backend/tests` 以 `MockLLM`/stub 覆盖 Harness 核心；最新 main CI `31389169084` 实际成功运行 backend 与三份稳定 JSON demo。 |
| A-6-2 | 三项机制演示：危险阻断、失败反馈改变动作、主贡献行为 | 已完成并验证 | 三份稳定 JSON demo：护栏阻断、MockLLM 反馈闭环改变动作、真实 `RunService` 的等待审批→批准→执行；真实 FastAPI/Vite/Chromium E2E 已通过。最新 main CI `31389169084` 也实际复现 demos 为绿。 |
| A-7 | 提交自实现 Harness 内核、Mock 单测、机制演示 | 部分完成 | 自实现 Harness、Mock 单测和三项 demo 已在 draft PR #13，CI/OCI 已在 draft PR #14；Task 15 本地 release docs/evidence 为 `9acb2ae`/`60528ae`/`84a10b4`/`93f3415`，限定复审 `0/0/0`。当前 backend `169 passed, 1 warning`、frontend `48`、build/E2E `2 passed`；Task 15 PR、外部交付与学生反思仍待完成。 |

## 实现前绝对门禁

1. 用户明确批准 `SPEC.md` 的本轮修订。
2. `writing-plans` 产生并提交符合 G-4.3 的 `PLAN.md`。
3. 使用不同类型的新 agent，仅凭 SPEC+PLAN 完成冷启动验证，并据结果修订 SPEC/PLAN。
4. 为所有实现模块建立 worktree/PR 与 task 编号。前三项任一缺失时，不得编写实现代码。

## 2026-08-10 Task 15 发布依赖更新

G-4.10 的 GHCR 外部验证仍为部分完成：只读 GitHub 查询表明 PR #1-#14 尚未合并且 `publish-image.yml` 不在默认分支（workflow 查询 404）。这说明需要先完成 stacked 合并和默认分支 CI，之后才可声明 GHCR package public 或匿名 pull/run 的真实结果。

## 2026-08-10 Task 15 反思篇幅更新

G-5-3 更新为部分完成待人工字数口径确认：用户提供的正文已原样写入 `REFLECTION.md`，协调会话没有代写/润色。统计中文汉字 `1583`（1500–2500 范围内），全部非空白字符 `2852`；学生应依据课程平台的实际计数口径决定是否自行缩短。

## 2026-08-10 stacked PR 集成追踪修正（优先）

G-4.7-1/2 的当前外部状态：PR #1–#9 已由 GitHub API 回读为 merged；#4–#9 merge commits 依次为 `c9b1173`、`9568e9f`、`b14a6c8`、`ef9c0a7`、`8468dfe`、`a2abb83`。#9 的堆叠冲突仅涉及过程日志并已在完整 backend `114 passed, 1 warning`、diff/凭据检查和 fresh C/I/M=`0/0/0` 独立审查后合并。尚未完成的是 #10–#14、Task15 PR/收尾、Task14 workflow 抵达 main 后的 GHCR public/匿名 pull-run；本修正覆盖上方“#1–#14 均未合并”的历史快照。

G-4.7-1/2 当前更新：PR #10 也已由 GitHub 回读为 merged（`696214d`）。该合并以前述 Red/Green integration test、完整 backend `146 passed, 1 warning`、diff/marker/credential scan clean 和 fresh C/I/M=`0/0/0` 为前提；仍待 #11–#14、Task15 PR/收尾，以及 Task14 workflow 抵达 main 后 GHCR public/匿名 pull/run 的真实外部证据。

G-4.7-1/2 当前更新：PR #11 已由 GitHub 回读为 merged（`622c472`）；完整 backend `146 passed, 1 warning`、frontend 15 tests/build、diff/marker/credential scan clean、fresh C/I/M=`0/0/0`。仍待 #12–#14、Task15 PR/收尾，以及 Task14 workflow 抵达 main 后 GHCR public/匿名 pull/run。

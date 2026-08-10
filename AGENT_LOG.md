# AGENT_LOG

本日志只记录实际发生的过程，不补写或虚构历史证据。

## 2026-08-03 D0：规格阶段

- 触发技能：`using-superpowers`、`brainstorming`、GitHub 工作流指引。
- 关键上下文：用户要求以《AI4SE 期末项目·通用要求》和《AI4SE 期末项目·A·Coding Agent Harness》为唯一验收基准，建立全新仓库，严格遵循七步 Superpowers 流程。
- 用户决策：确认建立公开仓库 `AlterGo-xzy/safe-code-harness-v2`；确认保留 WebUI 与自实现 Harness 内核；确认旧项目仅可在先写失败测试后按模块参考；确认治理作为主要贡献；确认 Docker/GHCR/公开 WebUI 为分发形态；要求所有材料使用中文。
- 实际动作：创建公开 GitHub 仓库；仅提交 `SPEC.md`、`SPEC_PROCESS.md` 和设计记录，提交 `568499a docs: record approved v2 specification`。本次文档修订尚未包含任何生产实现代码。
- 人工干预：用户纠正了英文文档方向，要求仅按正式要求完成并使用中文；据此将规格和过程记录改为中文。
- 学到的教训：文档存在不等于流程发生。必须让每一项过程要求具有可核验的时间顺序、Git 证据、测试记录和独立审查证据。

## 2026-08-03 D0：过程证据完善

- 触发技能：`brainstorming` 的规格审阅阶段。
- 触发原因：用户询问是否真正执行过 brainstorming，并指出过程文件需要能够支撑课程要求。
- 实际动作：在 `SPEC_PROCESS.md` 增加四轮真实对话节选、智能体追问与对应处理决策；未添加或修改任何实现代码。
- 人工干预：用户要求所有叙述如实，并以通用要求和 A 赛道要求为唯一目标。
- 学到的教训：仅写“迭代 1、迭代 2”不足以证明共同设计过程；过程文档应保留可核验的关键问答和决策链。

## 2026-08-03 D0：双要求逐条审计

- 触发技能：`using-superpowers`、`brainstorming` 的规格审阅阶段。
- 关键 context：完整阅读通用要求与 A 赛道要求，逐项检查新仓库已提交规格及过程文档。
- 实际动作：新增 `REQUIREMENTS_TRACEABILITY.md`；补足凭据生命周期和威胁模型；将 Open Design 实际使用设为前端任务前门禁；把 NJU Git、不同类型冷启动 agent、公开镜像和公开部署明确标为外部阻断而非已完成。
- 人工干预：用户要求不再由其补充遗漏，要求智能体自行逐条对照两份正式要求。
- 学到的教训：每条要求都必须具有一个可观察的完成门槛；“已设计”与“已验证”不可混用。

## 2026-08-03 D1：writing-plans 实现计划阶段

- 触发技能：`superpowers:using-superpowers`、`superpowers:writing-plans`；补丁异常时按 `superpowers:systematic-debugging` 先读取错误和精确原文再继续。
- 关键 context：用户要求以通用要求和 A 项目要求为唯一验收依据，逐项满足，不将旧仓库历史包装成合规证据；因此新仓库在冷启动验证前不创建实现代码。
- 实际动作：创建根目录 `PLAN.md`，定义任务 0-15 的依赖、独立 worktree/PR 规则、fresh subagent、失败测试、预期红色、最小实现、绿色验证、两阶段审查及真实提交记录要求；创建 Superpowers 计划索引。
- 人工干预：无实现层人工修改。用户此前确认以中文编写，并授权严格推进流程；计划仍需在提交后接受其确认，并先完成不同类型 agent 的冷启动验证。
- 已知边界：尚未使用不同类型 agent，尚未执行任何任务的失败测试，尚未创建 `backend/` 或 `frontend/` 源码，尚无 task worktree、PR、CI、镜像或部署证据。
- 学到的教训：计划中的“完成记录”只能在任务真实结束时回填；把任务结构写得很细不等于完成了冷启动、TDD、subagent 或评审流程。

## 2026-08-03 D1：冷启动 agent 环境准备

- 触发技能：`superpowers:using-superpowers`；为满足任务 0 的“不同类型”约束而检查本机 agent 客户端。
- 实际证据：`Get-Command claude,gemini,aider,codex` 只发现当前主开发使用的 `codex.exe`；经用户授权安装 `@google/gemini-cli`，并由 `gemini.cmd --version` 确认版本 `0.53.1`。
- 异常与处理：PowerShell 执行策略阻止 `gemini.ps1`，错误明确指向该包装脚本；改用同安装包的 `gemini.cmd`。其首次清理尝试因受限执行环境不能创建 `C:\\Users\\Admin\\.gemini` 而报告 EPERM；这不被记作认证或冷启动成功。
- 当前状态：不同类型 agent 已安装但尚未由用户完成 Google 登录；尚未发送密封 prompt，尚未接收其输出，任务 0 仍未完成，生产代码门槛仍然关闭。
- 学到的教训：安装命令成功不是独立 agent 验证成功；认证、全新会话、输入隔离、暂停问题、原始输出与规约修订必须分别留下证据。

## 2026-08-04 D1：调整冷启动 agent 选择

- 用户决策：删除 Gemini CLI，改用用户安装的 Claude 作为不同类型的冷启动 agent。
- 实际动作：执行 `npm.cmd uninstall --global @google/gemini-cli`，输出为 `removed 5 packages`；随后 `Get-Command gemini.cmd` 确认为 `not found`。
- 环境核对：当前 PowerShell 未发现 `claude` 或 `claude.cmd`，Windows 开始菜单也没有返回 Claude/Anthropic 应用项。因此尚不能把本机已检测到的任何 Claude 客户端作为已验证的冷启动环境。
- 当前状态：改用 Claude 的决定已记录，但在用户指出其 Claude 的实际入口并完成独立新会话前，任务 0 仍未开始；没有实现代码、worktree 或子代理任务被创建。
- 学到的教训：更换 agent 类型也必须记录实际可执行入口，不能以口头安装声明替代可复核的类型和隔离证据。

## 2026-08-04 T0：Claude Code 冷启动规约审阅

- 触发技能：主开发 agent 使用 `superpowers:using-superpowers`、`executing-plans` 和 `receiving-code-review`；外部审阅 agent 为 Claude Code，未获得主会话历史。
- 密封 context：只提供 commit `fc9b754` 的 `SPEC.md` 与 `PLAN.md` raw URL；要求选择任务 1 或 2，说明失败测试和红色结果，遇到不明确之处即停止，禁止读其他文件或实现代码。
- Claude 输出：选择任务 1，正确列出版本导入测试及 `ModuleNotFoundError`，并暂停提出四个问题：pyproject 精确内容、src layout 导入路径、conftest 职责、Windows 一键测试与忽略规则。完整原文保存在 `docs/evidence/cold-start-claude-code-task1.md`。
- 人工处理：判定四项均为 SPEC/PLAN 的真实缺口；修订 SPEC 9.1、PLAN 任务 1 和任务 8，固定包名、版本、最小依赖、测试路径、PowerShell 入口、editable-install 验证以及依赖的延后引入。
- 当前状态：Claude 已按“遇到歧义停止”要求产出可用反馈，尚待学生确认该 Claude Code 会话为全新 session；确认与本轮文档提交前，任务 0 未标完成，生产代码门槛继续关闭。
- 学到的教训：把文件名和目标列入计划不足以让陌生 agent 独立执行；测试环境、导入策略、包边界和平台入口都必须写成可验证的约定。

## 2026-08-04 T0：冷启动隔离证据核验

- 触发技能：`superpowers:using-superpowers`、`executing-plans`、`verification-before-completion`。
- 新增客观证据：学生提供的 PowerShell 转录显示 Claude Code `2.1.220`；未登录会话未执行任何工具。实际审阅由普通 `claude` 新启动而非 `--resume`，仅 Fetch `SPEC.md` 和 `PLAN.md` 两个 raw URL（均 200），随后显示 `read 2 files`；无本地读取、shell、编辑或提交调用。
- 门禁结论：不同类型、输入隔离、暂停问题、原始输出和据此修订五项均已有仓库内证据。实现代码仍为零；任务 0 在本轮证据提交后才标记完成。
- 学到的教训：欢迎语“Welcome back”不是会话复用的证据；必须以启动命令、是否 `--resume`、工具轨迹和实际读取集合判断输入隔离。

## 2026-08-04 P0：任务 1 worktree 前置准备

- 触发技能：`superpowers:using-git-worktrees`；工作区检测显示当前是普通 `main` 检出（`git-dir` 与 `git-common-dir` 都为 `.git`），`.worktrees/` 不存在且 `git check-ignore` 返回未忽略。
- 实际动作：在创建任一 worktree 前，最小新增 `.gitignore` 的 `.worktrees/` 与 `.superpowers/` 两项，并调整 PLAN 任务 1：该任务在隔离 worktree 中扩展已有 `.gitignore`，而不是声称新建它。
- 边界：此提交不创建 `backend/`、`frontend/` 或任何 Harness 源码，不执行任务 1 的测试，也不替代该任务的 TDD 过程。
- 学到的教训：忽略 worktree 目录必须先于 `git worktree add`，否则隔离目录可能被误纳入版本控制；该基础操作也要在日志和计划中如实说明。

## 2026-08-04 T1：工程基座与离线测试入口

- worktree/分支：`D:\\safe-code-harness-v2\\.worktrees\\t01-foundation` / `codex/t01-foundation`，基线 `5dd5da3`。
- 实现 subagent：`Arendt`（新鲜 session）；读取任务简报并仅在该 worktree 工作。实际提交 `cc81e31 chore: establish offline test foundation`，创建后端包元数据、src layout、测试导入脚手架、版本契约测试、Windows `scripts/test.ps1`，并扩展忽略规则；没有使用旧仓库源码或高层 agent framework。
- TDD 证据：生产包不存在时，focused pytest 实际得到 `ModuleNotFoundError: safe_code_harness`；加入最小 `__version__` 后 focused pytest、editable install、独立导入和 `scripts/test.ps1` 均通过，当前完整 backend 测试为 `1 passed`。
- 两阶段审查：新鲜 reviewer `Mencius` 先作 spec 合规、再作代码质量审查，结论均为批准，无 Critical/Important/Minor；其只读审查基线 `5dd5da3..cc81e31`。主协调会话独立执行 `scripts/test.ps1`，输出 `1 passed in 0.01s`，并确认 `git diff --check` 无输出。
- 人工干预：协调会话仅回填 PLAN/AGENT_LOG 的实际证据，没有修改任务功能文件。
- 学到的教训：即使最小包基座也要同时验证 pytest 导入路径和独立 editable-install 导入，任一单独通过都不足以证明 src layout 可用。

## 2026-08-04 T1：PR 创建外部阻断

- 实际动作：分支 `codex/t01-foundation` 已成功推送至 `origin`。尝试通过 GitHub 连接器为 `AlterGo-xzy/safe-code-harness-v2` 创建 draft PR，返回 `403 Resource not accessible by integration`。
- 交叉核对：`gh auth status` 显示本机活动账户 `AlterGo-xzy` 的 token 无效，并要求执行 `gh auth login -h github.com`；Git push 的传输凭据不能替代该 token。
- 当前状态：TDD、代码审查和独立测试均完成，但课程要求的“每个 worktree 一个 PR”尚未满足。等待学生完成 GitHub CLI 重新认证或通过网页创建 PR；在真实 PR URL/编号回填前，不进入任务 2。
- 学到的教训：分支已 push 不等于 PR 已建立；Git 传输认证、GitHub CLI token 和连接器权限需分别验证。

## 2026-08-04 T1：认证复核与新对话 handoff

- 用户声明已完成登录后，协调会话在当前分支重新运行 `scripts/test.ps1`，结果为 `1 passed in 0.01s`；随后 `gh auth status` 仍返回 `AlterGo-xzy` token invalid。该声明未被写成认证通过。
- 用户决策：允许复用此前完成的代码以减少重复工作，并要求完成当前 task 后维护可供新对话直接读取的进度与目标文件，目标必须覆盖两份正式要求的每一项。
- 实际动作：新增 `PROJECT_PROGRESS.md`，记录真实分支/commit/PR 阻断、严格的旧代码迁入边界、通用要求和 A 赛道要求逐项目标，以及下一步顺序。
- 学到的教训：handoff 文档必须把“已验证”“外部阻断”“后续目标”分开写；用户口头状态与命令实际输出冲突时以可复跑输出为准。

## 2026-08-04 T1：GitHub CLI 认证成功与分支收尾

- 触发技能：`superpowers:verification-before-completion`、`superpowers:finishing-a-development-branch`。
- 关键 context：用户完成 GitHub CLI 登录后，主协调会话重新运行 `gh auth status`，得到账户 `AlterGo-xzy` 已登录，token scopes 包含 `repo` 与 `workflow`。用户此前明确选择收尾选项 2“推送并创建 PR”。
- 实际动作：创建前执行 `scripts/test.ps1`，结果为 `1 passed in 0.01s`；执行 `git diff --check origin/main...HEAD` 无输出；使用 `gh pr create --draft --base main --head codex/t01-foundation` 创建 [PR #1](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/1)。
- 分支决定：依照选项 2 保留 `codex/t01-foundation` 与 `.worktrees/t01-foundation`，用于处理 PR 审查反馈；不合并、不删除。此前 connector 403 与失效 token 的日志保留为历史事实，不再构成阻断。
- 人工干预：用户完成并授权 GitHub CLI 登录；主协调只回填真实 PR 与新鲜验证记录，未修改任务 1 功能代码。
- 学到的教训：GitHub connector、Git 传输和 `gh` 是独立认证面；PR URL、测试输出和分支收尾决定都应在同一流程节点即时写入过程文档。

## 2026-08-04 T2：动作协议、运行模型与离线 Mock LLM

- worktree/分支：`D:\\safe-code-harness-v2\\.worktrees\\t02-action-protocol` / `codex/t02-action-protocol`，以任务 1 分支为 stacked 基线；后续 PR 先指向 `codex/t01-foundation`，待 PR #1 合并后改回 `main`。
- 触发技能：`superpowers:using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`；`systematic-debugging` 用于确认一键脚本必须从仓库根目录调用。
- 实现 subagent：`/root/t02_implementer`（新鲜 session），提交 `ba3116a feat: add deterministic action protocol and mock llm`。用户明确授权直接复用旧项目；仅迁入 `D:\\2026_summer_project\\backend\\src\\safe_code_harness\\core\\action.py`、`llm\\base.py`、`llm\\mock.py` 的相关概念，人工最小适配为计划接口 `parse_action`、`LLMClient.next_action` 与字符串序列 `MockLLM(responses)`；未迁入任何工具、网络、凭据或旧版内建序列。
- TDD 与验证：RED 的 focused parser 测试预期报 `ModuleNotFoundError: safe_code_harness.core`；GREEN 的 parser/Mock 测试为 `6 passed in 0.02s`。协调会话新建本 worktree 忽略的 `.venv` 后，从其根目录运行 `scripts/test.ps1` 和 `python -m pytest backend/tests -q`，两者均为 `7 passed in 0.01s`；`git diff --check 9f5eab6..HEAD` 无输出，受跟踪源码 secret scan 为 clean。
- 两阶段审查：独立 reviewer `/root/t02_reviewer` 先给出 Spec Compliance PASS，再给出 Task quality APPROVE；无 Critical/Important。Minor 要求保留独立完整测试输出，已通过协调会话的新鲜 full-suite 输出满足。
- 分支收尾：依照用户已确认的 `finishing-a-development-branch` 选项 2，推送 `codex/t02-action-protocol` 并创建 [draft PR #2](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/2)，暂以 `codex/t01-foundation` 为目标；保留该分支/worktree 处理审查，待 PR #1 合并后改为 `main`。
- 人工干预：协调会话只创建隔离 worktree、调用审查与回填真实证据；未改动任务功能源码。一次从旧项目当前目录绝对调用 `scripts/test.ps1` 导致相对路径误收集旧项目测试；检查脚本后确认规范调用方式是先进入目标仓库根目录，按此方式重跑后通过。
- 过程记录修正：后续只读审计发现任务 2 完成记录被误插入任务 13 的同名占位符；已将该记录移回任务 2，并恢复任务 13 的未完成占位符。未修改任何任务功能代码，也未启动任务 3。
- 学到的教训：批准复用旧代码并不等于放弃新仓库接口、离线边界或 RED/GREEN 证据；堆叠 PR 需要明确目标分支，避免把任务 1 基座变成任务 2 的重复审查范围。

## 2026-08-04 T3：策略、规则与失败关闭路径沙箱

- worktree/分支：`D:\\safe-code-harness-v2\\.worktrees\\t03-governance` / `codex/t03-governance`，以任务 2 分支为 stacked 基线，后续 PR 先指向 `codex/t02-action-protocol`。
- 触发技能：`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`；初审发现安全问题后按 fix round 与 scoped re-review 处理。
- 实现 subagent：`/root/t03_implementer`，初始提交 `843e50e feat: add policy rules and path sandbox`，修复提交 `49efb0c fix: harden governance path and secret checks`。用户授权复用旧代码；仅迁入 `D:\\2026_summer_project\\backend\\src\\safe_code_harness\\guardrails\\path_sandbox.py` 与 `rules\\evaluator.py` 的相关逻辑。人工适配把旧版独立 `check()` 合并进新 `resolve()`，杜绝返回不安全路径；未迁入命令、审批、工具、循环和 API。
- TDD：初始 RED 为缺少 `safe_code_harness.governance`；初始 GREEN 为 focused `11 passed`、backend `18 passed`。审查修复先得到 8 个预期失败，再为 focused `19 passed`、backend `26 passed`；协调会话新鲜运行完整 backend 及从仓库根目录运行 `scripts/test.ps1`，均为 `26 passed`，使用本地 `--basetemp`/`TEMP` 避开环境的默认临时目录权限限制。
- 两阶段审查：`/root/t03_reviewer` 先判定 spec 不通过并报告 `.env.*` Critical、`sk-`/`sk-proj-` 与运行时 level Important；`/root/t03_implementer` 原地修复。`/root/t03_rereviewer` scoped 复审逐项判定全部 ADDRESSED，无新 Critical/Important/Minor。精确凭据形态扫描 clean；宽泛词扫描只命中安全检测函数名，不作为泄露。
- 分支收尾：依照用户已确认的 `finishing-a-development-branch` 选项 2，推送 `codex/t03-governance` 并创建 [draft PR #3](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/3)，暂以 `codex/t02-action-protocol` 为目标；保留该分支/worktree 处理审查，上游 PR 合并后依次改为 `main`。
- 人工干预：协调会话只创建 worktree、维护账本、调度审查、运行独立验证及回填真实证据；未编辑任务功能源码。
- 学到的教训：治理边界不能只测试精确字符串；`.env.*`、大小写、链接解析、真实供应商 token 形态及运行时类型约束都必须成为可重复的失败测试。

## 2026-08-08 T4：命令护栏与非执行审批状态机

- worktree/分支：`D:\\safe-code-harness-v2\\.worktrees\\t04-command-approval` / `codex/t04-command-approval`，以任务 3 分支为 stacked 基线；后续 PR 先指向 `codex/t03-governance`。
- 触发技能：`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`systematic-debugging`、`verification-before-completion`、`finishing-a-development-branch`；使用 SDD 账本保存实现和修复回合证据。
- 实现 subagent：`/root/t04_implementer`。初始提交 `4707e49 feat: add command guard and approval state`；仅在 GREEN 阶段参考旧项目 `D:\\2026_summer_project\\backend\\src\\safe_code_harness\\guardrails\\command_guard.py` 和 `guardrails\\approval.py` 的命令规范化与决策术语。人工适配为当前 `RuntimePolicy` 的可配置阻断可执行名、确定性 `shlex` argv 解析，另新建不可执行的内存 `ApprovalStore`；未迁入旧 AgentLoop、工具、API、反馈或记忆。
- TDD：初始两个 focused 测试在模块不存在时按预期 RED；初始 GREEN 为 focused `5 passed`、完整 backend `31 passed`。首次独立审查发现等效 `rm` flags/long options/`--` 绕过（Critical）、policy 未参与（Important）和非字符串异常（Minor）；implementer 先加入回归，RED 为 `9 failed, 4 passed`，提交 `b053032 fix: harden command guard parsing` 后 focused `13 passed`、backend `42 passed`。scoped re-review 又发现 `env`、`sudo`、`command` 包装器绕过（Critical）；第二轮先得到 `8 failed, 14 passed`，提交 `eea0e4d fix: block destructive command wrappers` 后 focused command+approval `25 passed`、完整 backend `51 passed`。
- 两阶段审查：`/root/t04_reviewer` 首审拒绝合并并报告命令等效绕过；`/root/t04_rereviewer` 验证初审发现已修复但报告 wrapper Critical；`/root/t04_rereviewer2` 对 wrapper、嵌套 wrapper、普通 `env VAR=value`、自定义 `wipe` policy 和 fail-closed 行为 scoped re-review 为 APPROVE，无新 Critical/Important/Minor。审批存储只保存状态转换，不含工具或进程调用。
- 协调验证与环境排障：新鲜完整 `pytest backend/tests -q --basetemp ...` 为 `51 passed in 0.07s`。首次调用 `scripts/test.ps1` 显示 task 4 worktree 缺少 `.venv`，且脚本未传播解释器不存在的退出码；检查脚本和 `.gitignore` 后确认是隔离环境缺失而非源码缺陷。仅在忽略的 `.venv/` 建立指向任务 3 已验证环境的本地 junction，并从 task 4 根目录重跑，`scripts/test.ps1` 为 `51 passed in 0.08s`。`git diff --check b9f72cf..HEAD` 无输出；精确凭据扫描唯一命中是既有 `test_rules.py` 的假 token fixture，不是泄露。
- 人工干预：协调会话未编辑任务 4 功能源码；只调度独立审查、维护记录、修复本地忽略测试环境并执行新鲜验证。
- 学到的教训：命令安全策略不能依赖字符串子串；必须对参数排列、长短选项、分隔符、包装器和无法解析输入定义确定性的 fail-closed 语义，并把每一个审查绕过固化为先失败的回归测试。

## 2026-08-08 T4：分支收尾与 PR

- 触发技能：`verification-before-completion`、`finishing-a-development-branch`、`github:yeet`。用户已在任务 1-3 建立并持续采用收尾选项 2；本任务沿用“推送并创建 draft PR、保留 worktree”。
- 收尾前新鲜验证：从 `codex/t04-command-approval` worktree 根目录运行 `scripts/test.ps1`，为 `51 passed in 0.07s`；`git diff --check b9f72cf..HEAD` 无输出，工作树干净。
- 实际动作：GitHub CLI 认证为 `AlterGo-xzy`，scopes 包含 `repo` 与 `workflow`；推送 `codex/t04-command-approval` 并创建目标为 `codex/t03-governance` 的 [draft PR #4](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/4)。API 回读确认 `OPEN`、`isDraft=true`、base/head 正确。
- 分支决定：保留 `codex/t04-command-approval` 与 `.worktrees/t04-command-approval` 用于处理审查；待 #1、#2、#3 合并后依次将 base 调整为 `main`。

## 2026-08-08 T5：受控工具与分派器

- worktree/分支：`D:\\safe-code-harness-v2\\.worktrees\\t05-tools` / `codex/t05-tools`，以任务 4 分支为 stacked 基线；后续 PR 先指向 `codex/t04-command-approval`。
- 触发技能：`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`；SDD 账本保存简报、报告和 deferred Minor。
- 实现 subagent：`/root/t05_implementer`，提交 `2795539 feat: add governed tool dispatcher`。旧代码只在 RED 后参考 `tools` 的四个相关模块与一个测试文件；人工适配为显式 handler 白名单、`ToolResult`、`PathSandbox`、`CommandGuard` 和可注入 runner/timeout，未迁入 loop/API/planner/凭据/反馈/旧 memory。
- TDD 与验证：三个 focused 测试先按预期 RED 为缺少 `safe_code_harness.tools`；GREEN 为 focused `7 passed in 0.03s`、完整 backend `58 passed in 0.09s`。协调会话新鲜运行 `scripts/test.ps1` 为 `58 passed in 0.10s`，`git diff --check 716d246..HEAD` 无输出；精确凭据扫描只有既有假 token fixture。
- 审查：`/root/t05_reviewer` 认为白名单、PathSandbox、guard-before-runner、argv/timeout 和无真实进程测试均符合要求，无 Critical/Important。它建议补强安全 shell 的 argv/timeout 和 requires_approval 短路回归，已如实登记为 deferred Minor，不影响当前任务合格。
- 人工干预：协调会话只建立 worktree/本地忽略环境、调度审查、回填证据和运行新鲜验证，未改动任务功能源码。
- 学到的教训：工具层的“没有执行”需要用注入 runner 的行为断言证明；白名单、路径解析和命令护栏必须构成不可绕过的先后顺序，而不是由调用者自觉遵守。

## 2026-08-08 T5：分支收尾与 PR

- 触发技能：`verification-before-completion`、`finishing-a-development-branch`、`github:yeet`；沿用既有选项 2，推送并创建 draft PR、保留 worktree。
- 收尾前新鲜验证：`scripts/test.ps1` 为 `58 passed in 0.10s`，`git diff --check 716d246..HEAD` 无输出，工作树干净。
- 实际动作：推送 `codex/t05-tools`，创建 [draft PR #5](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/5)，API 回读确认 `OPEN`、`isDraft=true`、base `codex/t04-command-approval`、head 正确。
- 分支决定：保留 `codex/t05-tools` 与 `.worktrees/t05-tools` 等待审查；上游 PR 合并后依次调整 base 为 `main`。

## 2026-08-08 T6：确定性反馈与有界运行记忆

- worktree/分支：`codex/t06-feedback-memory`；implementer `/root/t06_implementer` 提交 `cc5b974`，审查修复 `6b9676b`。RED 缺少模块；GREEN focused `12 passed`、backend `70 passed`。首审发现凭据脱敏和可变事件两项 Important；先以 `7 failed` 回归再修复为 focused `19 passed`、backend `77 passed`。scoped re-review APPROVED；协调一键测试 `77 passed in 0.11s`，diff check clean。
- 旧代码仅在 RED 后参考 `feedback/evaluator.py` 与 `memory/store.py` 概念；未迁入 loop/API/planner/凭据。自由文本前缀分类问题明确 deferred 至任务 7 的结构化 outcome。

## 2026-08-08 T6：分支收尾与 PR

- 沿用收尾选项 2；已推送 `codex/t06-feedback-memory` 并创建 [draft PR #6](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/6)。API 回读确认 `OPEN`、`isDraft=true`、base `codex/t05-tools`、head 正确；保留 worktree 等待审查。

## 2026-08-08 T7：自实现受治理 AgentLoop

- worktree/分支：`codex/t07-agent-loop`，基线 `124b7f6`；implementer `/root/t07_implementer` 提交 `2ceb6b1`，两轮安全修复 `e018822`、`328baaf`。
- RED 后仅参考旧项目 `core\agent_loop.py` 和直接相关测试的循环/事件概念；新实现使用本仓库 Action、Rules、ApprovalStore、ToolDispatcher、Feedback 和 Memory，未迁入高层 agent framework、API、planner 或凭据。
- 初审发现审批触发/恢复和工具失败可观察性缺口；第一次修复后 scoped re-review 又发现恢复配置漂移可绕过被拒审批。每轮均先有失败回归，最终 scoped re-review PASS。新鲜 unit 为 `88 passed`，根目录完整 backend/tests（含 integration）为 `89 passed in 0.12s`；未跟踪报告保留在 `task-7-report.md`。

## 2026-08-08 T8：FastAPI 运行与审批 API

- `/root/t08_implementer` 提交 `974d73b`、`7afa279`；API 只经 ApprovalStore 和 AgentLoop.resume 恢复，拒绝无工具分发，事件脱敏可序列化。
- 审查的 httpx2 依赖缺口经干净安装验证修复，scoped re-review PASS；full backend `96 passed`、一键 unit `88 passed`；上游 Starlette 弃用警告已如实记录。
- 任务 11 发现前端所需列表契约与实际 Task 8 不一致；用户确认不伪造数据、以 Task 8 修正补充真实只读 API。fresh implementer `/root/t08_runlist_implementer` 在 RED（405/缺 scenario）后提交 `afd42ae`；列表严格白名单四个摘要字段且稳定排序，详情补安全元数据。独立 reviewer `/root/t08_runlist_reviewer` PASS，无 C/I/M；协调完整 backend `99 passed`、脚本 `88 passed`，仅既有 TestClient warning。未使用旧代码、网络或真实凭据；已更新现有 draft PR #8。
- 任务 11 API 边界审查发现详情事件原文不可安全透传；用户确认以服务端固定 DTO 取代。fresh implementer `/root/t08_timeline_implementer` 在 RED 后提交 `6fd3237`，详情时间线仅含 `type`、`created_at`、`level`、`display_status`、`summary_code`，固定中文映射且未知事件 fail-closed。独立审查代码 PASS；缺少 SDD 报告的 Minor 已补齐并 scoped 确认。协调完整 backend `100 passed`、脚本 `88 passed`，仅既有 TestClient warning；更新现有 draft PR #8。

## 2026-08-08 T9：凭据存储与 OpenAI-compatible Planner

- worktree/分支：`D:\safe-code-harness-v2\.worktrees\t09-planner-credentials` / `codex/t09-planner-credentials`，基线 `2de48a2`。触发技能：`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`systematic-debugging`、`verification-before-completion`；SDD 简报明确禁止真实 key、网络调用和明文/磁盘回退。
- 用户决策与安全边界：用户选择暂不配置 OpenAI-compatible API key，之后再通过前端录入。协调会话仅做 presence 检查并得到 `OPENAI_API_KEY_STATUS=absent`，未读取或输出任何值；功能和测试只用 `fixture-secret-2026` 与 fake adapter/transport。
- 实现 subagent：`/root/t09_implementer` 提交 `3074085 feat: add secure optional planner configuration`。新增 Windows Credential Manager-only `SecretStore`、掩码 `GET/PUT/DELETE /api/config/planner` 和可注入 HTTP transport 的单次 Planner LLM。非 Windows 和适配器失败均 fail-closed，配置响应只含 `configured`、`masked_suffix`、`base_url`、`model`；未使用旧项目代码。
- TDD：模块缺失时 focused RED 是 `4 failed, 4 errors`；初始 GREEN focused `8 passed`、全量 `104 passed`。`/root/t09_reviewer` 的威胁模型审查发现 Important：`raise ... from exc` 会让潜在含 key 的底层错误存在于 traceback。implementer 先用会抛含 fixture key 的 fake adapter 得到修复 RED `4 failed, 10 passed`，随后在 SecretStore 和配置路由的六处异常转换使用 `from None`，提交 `51eb9c8 fix: prevent credential exception-chain leaks`；另补无 key 不调 fake transport和空白 key 422。修复 GREEN focused `14 passed`、full backend `110 passed`。
- 两阶段审查：首轮拒绝并报告上述 Important；scoped re-review 核对 set/get/clear 与 GET/PUT/DELETE 的 traceback/503 均不含 fixture key，且无 key 时传输调用为零，结论 PASS、无 C/I/M。协调会话独立运行完整 backend `110 passed, 1 warning`，运行 `scripts/test.ps1` unit `96 passed`；唯一 warning 为既有 Starlette/TestClient 对 httpx 的弃用提示。
- 人工干预与教训：协调会话未编辑功能源码，只调度审查、运行独立验证并回填证据。接口“不回显”不足以保证安全；异常 cause、traceback 和错误日志也必须被视为凭据数据流并有失败回归。
- 分支收尾：依照用户在前序任务持续采用的 `finishing-a-development-branch` 选项 2，推送 `codex/t09-planner-credentials` 并建立目标为 `codex/t08-api-runs` 的 [draft PR #9](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/9)。保留该 branch/worktree 等待审查；上游 stacked PR 合并后依次调整 base 为 `main`。

## 2026-08-09 T11：受治理运行工作台的复核与过程证据

- worktree/分支：`D:\safe-code-harness-v2\.worktrees\t11-workbench-ui` / `codex/t11-workbench-ui`；实现 subagent 分段为 `/root/t11_task1_implementer` 与 `/root/t11_task2_implementer`，过程复核为 `/root/t11_task3_implementer`。实现提交：`893f01a`、`63749f5`、`0dcdca9`；本条不创建 PR。
- Open Design 历史记录与当前证据边界：设计阶段记录称当时从 `nexu-io/open-design` Windows x64 Release 安装 `0.18.1` 并做过 SHA-256 校验，但本地未保留安装包、资产 URL 或精确摘要，当前不可复现，也不能作为已验证事实。本项目只采用该记录中的“技能/设计系统驱动、真实文件产出、可审计而非装饰性堆叠”原则，未引入运行时依赖；绝不猜测或补写摘要值。
- Task 1：先有 `runs` 模块不存在的 RED；首轮 GREEN 为 4/4。随后以任务 8 服务端安全 DTO 为唯一契约：列表白名单四字段，详情时间线白名单五字段。安全审查报告两个 Important：fetch/JSON 错误会露出原文，及旧字段 `summary`/`failure` 被读取；先有 3/6 RED，再在 `63749f5` 修复为 6/6，并将错误固定为中文消息。
- Task 2：先有 `App` 与 `RunTimeline` 不存在的 RED；绿色为 focused 6/6、全套 12/12。审查覆盖 API-only 渲染、无批准/配置/上传写路径、无 secret/localStorage、选中卡片仅以 `getRun` 返回事件、中文加载/空/错误状态；最终未发现 Critical/Important。质量复核确认原生 button 键盘焦点、`aria-pressed`、文本状态、语义列表、`44rem` 单列布局、`min-width: 0` 和 `overflow-wrap: anywhere`。没有浏览器 320px 实测，保留 Task 13 E2E，不把 CSS 静态检查写成视觉验证。
- 新鲜控制器验证：从 `frontend` 运行 `npm.cmd test`，Vitest 为 3 files/12 tests passed；`npm.cmd run build` 成功（Vite 5.4.21，337ms）；仓库根目录 `git diff --check 2de48a2..HEAD` 无输出。变更文件凭据模式扫描只报告汇总：无非测试代码匹配，未输出任何命中内容。
- 人工边界与教训：没有编辑功能源码、没有读取旧项目、没有联网或真实密钥；仅更新过程文档和本地 SDD 报告。完整 Release checksum 必须在将来有原始安装证据或获准联网时补入，不能由记忆或猜测替代。

## 2026-08-09 T11：最终审查修复波

- 执行者 `/root/t11_final_fix_implementer` 使用 `receiving-code-review`、`systematic-debugging`、`test-driven-development`、`verification-before-completion`；用户明确选择安全 DTO 优先，禁止恢复任何原始事件文本。实现与设计/详细计划修复提交为 `33b5ff0`，不创建 PR。
- 依赖 RED：原树没有 `package-lock.json`，`npm.cmd ci --ignore-scripts` 以 `EUSAGE`/exit 1 失败；`@testing-library/react`、`@testing-library/jest-dom`、`jsdom` 只是旧 `node_modules` 的 extraneous 包。GREEN：`package.json` 精确声明 16.3.2、6.9.1、25.0.1，新增 lockfile v3；`npm.cmd install` 生成依赖树，随后 lockfile 驱动的 `npm.cmd ci --ignore-scripts --no-audit --no-fund` 成功安装 176 packages。
- 行为 RED：focused 3 files/9 tests 中 3 个按预期失败，分别证明卡片 accessible name 缺场景以外的状态/更新时间、UTC 值未标注时区、`detail.id !== selectedRunId` 仍会渲染。另加真实乱序 promise 回归，证明晚到旧请求不能覆盖当前选择。GREEN：卡片名称现在包含场景/状态/UTC 更新时间，两个时间格式化器显式附加 `UTC`，App 只在详情 id 匹配当前选择时渲染；focused 3 files/9 tests 全绿。
- 文档修正：设计、详细计划与根计划只承诺列表四字段和时间线五字段安全 DTO，删除创建运行、最新事件摘要、工具输出/规则原文承诺。Open Design 只保留“当时记录称安装并校验、当前无安装包/资产 URL/精确摘要而不可复现”的历史陈述，绝不猜测摘要。任务 11 没有窄屏浏览器测试，320px 证据继续作为任务 13 未完成项。
- 新鲜验证：clean install 后 `npm.cmd test` 为 4 files/15 tests passed；`npm.cmd run build` 成功（Vite 5.4.21，327ms）；credential-like 扫描只报告 `credential_candidate_count=0`；staged diff check 无输出。网络仅用于获准的 npm 依赖安装/解析，没有应用 API、真实 LLM、真实凭据或其他联网操作。
- 独立 scoped re-review 对 `47986c1..779b4e0` 给出 Critical 0、Important 0、Minor 1：详细计划示例仍含旧事件文字及笼统安装证据措辞。随后以文档最小修正将断言改为固定 `summaryCode`，并明确安装记录不可复现；未改变运行时行为或安全边界。
- 收尾：用户选择 `finishing-a-development-branch` 选项 2；`codex/t11-workbench-ui` 已成功推送，并创建目标为 `codex/t08-api-runs` 的 [stacked draft PR #11](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/11)。保留 worktree 处理审查反馈；未合并、未删除分支。

## 2026-08-09 T12：治理控制面板与过程复核

- worktree/分支：`D:\safe-code-harness-v2\.worktrees\t12-settings-approval-ui` / `codex/t12-settings-approval-ui`。Task 1 提交 `1a9074b`，Task 2 提交 `0369c8f`，审查修复 `b22c56d`；本条不创建 PR 或推送。
- TDD：Task 1 在依赖安装后先得到 4 files failed、3 tests failed、5 passed 的预期 API RED，随后为 4 files/16 tests GREEN。Task 2 先因三个面板和 App 组合缺失得到 focused RED；另以 Planner 清除错误得到 focused RED，随后为 4 files/15 tests GREEN。Task 2 review 的两个 Important 均先有失败回归：晚到审批完成与选择切换、以及迟到初始 Planner GET 覆盖 mutation；修复后 focused 3 files/16 tests、完整 10 files/37 tests GREEN。
- 两阶段审查与复核：Task 1 的安全投影 review 记录为 clean（仅 2 个 deferred Minor）；Task 2 初审为 Critical 0、Important 2、Minor 1，fix round 后 review clean。Task 3 按先 spec/security、后质量/无障碍的顺序复核：只用任务 8-10 已有写路由，无 policy UI/route 或假成功；无 raw event、key JSX/state/error/URL、localStorage 和路径显示；labels、原生 keyboard buttons、pending disabled、固定错误/空状态、标题、审批刷新、ZIP accept、组件边界和 stale-detail guard 均符合范围。无 Critical/Important，因此不改产品代码。
- 旧项目/人工边界：Task 1/2 没有读取、复制或咨询旧项目源码。旧 `D:\2026_summer_project\frontend\src\components\ConfigPanel.tsx`、`WorkspaceUploadPanel.tsx`、`backend\src\safe_code_harness\api\routes_config.py` 仅登记为未来扩展调查入口，不是 Task 12 的实现指导；未迁入策略、localStorage、服务器路径或 workspace 切换。用户批准策略扩展延后，Task 12 未实现策略 API/UI。
- 新鲜控制器验证：`frontend` 中 `npm.cmd ci --ignore-scripts` 成功（176 packages；npm audit 提示 3 moderate、1 high、1 critical，未改依赖）；`npm.cmd test` 为 10 files/37 tests passed；`npm.cmd run build` 成功；`git diff --check codex/t11-workbench-ui..HEAD` 无输出。高置信凭据模式扫描只报告 `credential_like_match_count=0`，不输出内容。
- 后续：任务 13 的真实合并后 API、浏览器和 320px E2E 尚未执行；本 Task 不虚构 PR、浏览器验证或策略持久化。

## 2026-08-09 T12：最终审查修复波

- 执行者 `/root/t12_final_fix_implementer` 使用 `receiving-code-review`、`systematic-debugging`、`test-driven-development` 和 `verification-before-completion`；只处理最终审查的 Critical 0、Important 0、Minor 6，不创建 PR 或推送。
- 根因与 RED：运行时唯一缺口是 `PlannerSettings` 未表达初始 GET pending；其余五项是边界覆盖或文档事实不一致。新增全部回归后，focused `npm.cmd test -- --run src/api/runs.test.ts src/api/planner.test.ts src/components/PlannerSettings.test.tsx src/components/WorkspaceUpload.test.tsx` 为 1 failed、28 passed，失败断言精确指出缺少 `正在加载 Planner 配置…`。非字符串 `approval_id`、Planner GET/PUT/DELETE non-OK/网络错误固定消息、Planner save/clear pending 和 ZIP upload pending 回归均直接通过，证明现有实现已保持这些行为。
- 最小 GREEN：Planner 面板增加只覆盖初始 GET 生命周期的本地 loading state 和固定中文提示；`App` 仍只拥有当前选择详情/审批刷新，三个面板各自拥有瞬时请求状态。focused 复跑为 4 files/29 tests passed；完整前端为 10 files/48 tests passed，build 成功。
- 六项 Minor 均关闭：补齐非字符串审批 ID；三种 Planner 方法的 HTTP/网络脱敏；将 `PROJECT_PROGRESS.md` 日期改为 2026-08-09；统一 Task 1/2 未读取、复制或咨询旧代码且三个路径仅为未来扩展入口；修正 App/面板状态归属并加入 Planner 加载反馈；补齐 Planner 与上传 pending 禁用回归。设计、详细计划和四份过程文档均按实际事实修正。
- 边界未扩张：无 policy API/UI/backend、localStorage、raw fields、server paths 或 Planner key state/error echo。策略扩展仍按用户决定延后；任务 13 的真实 API、浏览器和 320px E2E 仍未执行。
- 分支收尾：用户要求按要求文件操作，故采用 `finishing-a-development-branch` 选项 2；已推送 `codex/t12-settings-approval-ui` 并创建目标为 `codex/t11-workbench-ui` 的 [stacked draft PR #12](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/12)。保留 worktree 处理审查反馈；未合并或删除分支。

## 2026-08-08 T10：安全 ZIP 上传与隔离工作区

- 分支/worktree：`codex/t10-workspace-upload` / `D:\\safe-code-harness-v2\\.worktrees\\t10-workspace-upload`，基线 `2de48a2`。实现 `/root/t10_implementer` 先 RED，后仅参考旧 `routes_workspace.py:75-118` 的 ZipInfo/symlink 概念，未复制旧跳过敏感文件或异常回显行为。
- 提交 `698e4dc`、`b546c89`、`d15a4fd`：全量预校验并拒绝 ZIP Slip、ADS、NUL、UNC、Windows 设备名、重复条目、symlink、敏感/缓存目录、成员与大小上限；仅当前上传创建的目录可被清理，UUID 碰撞保留旧工作区；API 固定 path-free 400。
- 审查：首审 1 Critical/3 Important、scoped review 1 Important，均先有失败回归后修复；最终 PASS，无 C/I/M。协调验证完整 backend `127 passed`、脚本 unit `113 passed`，各有既有 TestClient 弃用 warning。下一步按收尾 skill 建立独立 draft PR。
- 分支收尾：沿用 `finishing-a-development-branch` 选项 2，推送 `codex/t10-workspace-upload` 并建立目标为 `codex/t08-api-runs` 的 [draft PR #10](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/10)。保留 branch/worktree 等待审查；上游 stacked PR 合并后依次调整 base 为 `main`。

## 2026-08-09 T13 Task 1：真实 Task 8/9/10 API 集成

- worktree/分支：`D:\safe-code-harness-v2\.worktrees\t13-demos-e2e` / `codex/t13-demos-e2e`；fresh implementer `/root/t13_task1_implementer` 使用 `executing-plans`、`using-git-worktrees`、`test-driven-development` 与 `verification-before-completion`，严格限定为后端 API 集成，不做 frontend、E2E、demo 或 policy。
- 环境与基线：brief 中的 `..\.venv\Scripts\python.exe` 不存在；改用本 worktree 内被 `.gitignore` 排除的 `.venv` 并 editable install `backend[dev]`，避免误加载其他 worktree 的 editable source。合并前完整 backend 为 `100 passed`，只有既有 Starlette/TestClient 对 httpx 的弃用 warning。
- TDD RED：先新增 `backend/tests/integration/test_integrated_api_surface.py`，fixture 以 `FakeSecretStore` 调用 `create_app(secret_store=...)`，且断言 runs、Planner 四字段 DTO 与非法非 ZIP 上传。任何 merge 前 focused 命令 exit 1，预期错误为 `TypeError: create_app() got an unexpected keyword argument 'secret_store'`。
- 合并与冲突：Task 9 以 `ec613df` 合入，冲突仅 `AGENT_LOG.md`、`PROJECT_PROGRESS.md`、`REQUIREMENTS_TRACEABILITY.md`，保留 T9 reviewed 记录与更新的 T11/T12 记录；Task 10 以 `1664aa2` 合入，冲突为 `AGENT_LOG.md`、`PROJECT_PROGRESS.md` 与 `api/main.py`。factory 按 brief 统一三个 state 和三个 router；Task 9/10 安全源文件与测试相对各自 reviewed branch 的 scoped diff 均无输出。
- GREEN：focused integration `1 passed, 1 warning`；完整 `backend/tests` 为 `146 passed, 1 warning`。warning 仍为既有 TestClient 弃用提示，不是本集成引入的失败。未使用真实 key、应用网络调用或旧项目源码。
- 提交：Task 9/10 merge commits 分别为 `ec613df`、`1664aa2`；集成测试与四份过程文档提交为 `fd38e6a feat: integrate planner and workspace APIs`。
- 剩余范围：Task 13 的三个确定性 demo、Playwright 真实浏览器流程与 320px 验证仍未执行；策略扩展仍按用户决定延后。完整命令和证据见 `.superpowers/sdd/2026-08-09-demos-e2e/task-1-report.md`。

## 2026-08-09 T13 Task 2：离线确定性机制演示（审查待执行）

- worktree/分支：`D:\safe-code-harness-v2\.worktrees\t13-demos-e2e` / `codex/t13-demos-e2e`；fresh implementer `/root/t13_task2_implementer` 按 `subagent-driven-development` brief 使用 `test-driven-development`。范围严格限于三份离线 demo、其集成测试、跨平台入口与 README 说明；未开始 Playwright、policy 扩展、CI、容器或部署，也未读取或迁入旧项目代码。
- TDD RED：新增 `backend/tests/integration/test_demos.py` 后运行 `.\.venv\Scripts\python.exe -m pytest backend\tests\integration\test_demos.py --basetemp .pytest-tmp\task13-demos-red -q`，预期在收集期以 `ModuleNotFoundError: No module named 'scripts.run_approval_demo'` 失败。测试验证实际 CLI JSON 行为，而非源文本；同时拒绝 `C:`、`D:` 和 `secret` 输出。
- 最小实现与边界：guardrail 直接调用现有 `CommandGuard(RuntimePolicy())`；反馈 demo 用固定响应的 `MockLLM` 子类，第二次动作前确认失败测试反馈已进入真实 `AgentLoop` context，并用临时目录内的有界工具 double 后在 `finally` 清理。首次版本的 approval demo 虽调用真实 `RunService.start/decide`，但返回值是固定字面量，不能构成“实际投影”证据；该不准确表述已在修复记录中更正。三份 CLI 仅输出稳定 JSON；没有网络、真实 LLM、key、项目工作区 mutation 或绝对路径输出。
- GREEN：同测试为 `6 passed in 0.23s`；`.\scripts\run_demos.ps1` 成功连续输出阻止、反馈修复、批准后执行三份 JSON。完整 backend 回归为 `152 passed, 1 warning`，warning 是既有 Starlette/TestClient 对 httpx 的弃用提示；`git diff --check` 无输出，高置信凭据候选只报告计数 `0`。`Makefile` 为 Unix-like 环境提供 `demos` target；当前 Windows 没有 GNU make，未运行且未宣称其成功。README 仅说明离线 demos，明确不把它们写成 E2E/CI/部署证据。
- 提交与后续：源代码及首次证据提交为 `26f9855 test: add deterministic mechanism demos`。Task 2 尚待独立 spec/security 审查与代码质量审查；之后才可进入 Task 3 的真实 API/browser/320px 工作。完整执行报告将写入 `.superpowers/sdd/2026-08-09-demos-e2e/task-2-report.md`（忽略文件）。

## 2026-08-09 T13 Task 2：首次审查修复（复审待执行）

- 反馈验证：首次审查的三项发现均可由当前代码复现，且不改变 Task 2 范围。approval demo 的根因是它没有读取 snapshots；进一步诊断确认现有安全 DTO 在 completed snapshot 中会把两条 approval event 都映射为 `approval_approved`，因此修复使用真正执行前的最后一个批准事件，而不改动 Task 8 的安全投影。PowerShell 根因是外部命令的 `$LASTEXITCODE` 不会在无检查时令脚本失败；cleanup 根因是 `ignore_errors=True`。
- TDD：先对缺少 `_project_approval_transcript` 得到 import RED；其后事件顺序回归以不匹配固定错误 RED，确认重复 approval 投影需要精确定位。另有 PowerShell 临时 `SystemExit(7)` child 的 RED（entrypoint returncode 为 0），以及缺少 `_remove_demo_workspace` 的 import RED。修复后 approval 子集 `4 passed`、PowerShell 子集 `1 passed`、cleanup 子集 `1 passed`，完整 `test_demos.py` 为 `10 passed in 0.47s`；正常 `.\scripts\run_demos.ps1` 连续输出三份稳定 JSON。完整 backend 为 `156 passed, 1 warning`（既有 TestClient 弃用），`git diff --check` 无输出，凭据候选计数为 0。

- 修复：approval transcript 只从真实 pending/completed snapshots 生成，拒绝等待 snapshot 已含 `tool_succeeded`、缺少证据或最后一次批准不早于唯一执行；PowerShell 新增受测的可选 Python/script 参数但默认行为不变，每次 child 后检查 `$LASTEXITCODE` 并抛固定 path-safe 错误；清理将 `OSError` 变为固定 `RuntimeError`，不再吞掉失败。未改 UI、E2E、policy、旧项目复用、CI 或部署。
- 提交与后续：修复提交为 `7243dfc fix: harden deterministic demo evidence`。此修复待独立复审，随后才可更新 Task 2 完成状态并开始 Task 3。完整修复报告将写入 `.superpowers/sdd/2026-08-09-demos-e2e/task-2-fix-report.md`（忽略文件）。

### 2026-08-09 — Task 13 Task 2：第二次独立复审与冻结交接

- 审查：fresh read-only reviewer `/root/t13_task2_fix_reviewer` 未运行测试、未修改文件，结论为 Critical 0、Important 1、Minor 2。Important：审批演示仍只将 `tool_succeeded` 认作等待/批准前执行，未拒绝 `tool_failed`；必须先写失败回归并拒绝任意工具结果。Minor：PowerShell 测试只有单一失败 child，必须证明 first child 失败时 later child 不运行；`PROJECT_PROGRESS.md` 与 `REQUIREMENTS_TRACEABILITY.md` 有 focused `6 passed`/完整回归未执行的过期陈述。
- 人工决定：用户要求先保存现有成果并停止继续实现，故不在此复审结论后修改代码、不启动 Task 3/Playwright/策略扩展。`7243dfc`、`7bf3d04` 已保存全部已完成实现/文档；当前 worktree 的 `git status --short` 无输出。
- 交接：新增 `HANDOFF_TO_NEXT_MODEL.md`，含分支/HEAD、可如实引用的 RED/GREEN、三个未闭环问题、环境差异、下一步 TDD 命令和不变量。后续模型必须先关闭该 Important 和两个 Minor、完整验证、再次独立审查，才可进入 Task 13 Task 3。

### 2026-08-10 — Task 13 Task 2：三轮 review/fix 后完成

- 范围与来源：fresh implementer `/root/t13_task2_fix2_implementer` 只处理第二次复审的 1 Important/2 Minor；未读、复制或咨询旧项目，未开始 Task 3/Playwright、策略扩展、CI、分发或部署。
- TDD：先将 waiting 回归参数化为 `tool_succeeded`/`tool_failed`，并新增 completed snapshot 在最后 `approval_approved` 前出现 `tool_failed` 的回归；RED focused 为 `2 failed, 2 passed`，两处均因未抛 `RuntimeError`。另将 PowerShell 回归改为 failing first child 加写 marker 的 later child；现有逐 child `$LASTEXITCODE` 检查已使该行为通过，故不改生产脚本。最小源码修复为 approval 投影在 waiting 或最后批准前拒绝 `tool_succeeded`、`tool_failed`；focused GREEN 为 `4 passed, 8 deselected in 0.26s`。
- 验证：完整 demo 为 `12 passed in 0.46s`，正常 `.\scripts\run_demos.ps1` 输出三份稳定、安全 JSON；完整 backend 为 `158 passed, 1 warning`，warning 是既有 TestClient 弃用提示；`git diff --check` 无输出，已变更 diff 的高置信凭据候选计数为 0。
- 第三次审查与状态：此前 focused `10 passed`、完整 backend `156 passed, 1 warning` 是历史证据；本轮源码/测试已提交 `7bdd85d`，第二次复审的 `tool_failed` 与 later-child 行为发现已修复并验证。第三次独立审查仅指出交接/过程文档仍未同步；`5bf57a3` 文档修正后的 scoped re-review 已 PASS（Critical/Important/Minor 均为 0）。Task 2 已完成，可进入 Task 3。

### 2026-08-10 — Task 13 Task 3：真实 API/浏览器 E2E 实现（实现阶段记录；后续审查见 Task 4）

- 执行者与范围：fresh implementer `/root/t13_task3_implementer` 使用 `test-driven-development`、`systematic-debugging` 和 `verification-before-completion`；只实现 Playwright 真实批准闭环与 320px 证据，未开始 Task 4、任务 14/15、策略扩展或 PR/push，也未读取/迁入旧项目代码。
- TDD RED：先新增 E2E spec、最小 config 与 `test:e2e`，运行 `npm.cmd run test:e2e` exit 1，精确报错为系统找不到 `playwright`。安装 `@playwright/test` 后，真实双服务首次启动 exit 1，报 t13 `.venv` 缺 `uvicorn`；根因是 `backend[dev]` 只声明 pytest，而批准计划的启动命令直接调用 uvicorn。最小声明 `uvicorn>=0.35,<1` 并 editable 重装。完整前端首次回归又因 Vitest 默认收集 `e2e/workbench.spec.ts` 得到 1 failed suite/48 passed tests；将 Vitest include 限定在 `src/**/*.test.{ts,tsx}` 后关闭。
- 依赖与真实边界：`npm.cmd install --save-dev @playwright/test` 成功并固定 1.62.1；npm audit 报 3 moderate、1 high、1 critical，未运行破坏性的 force fix。`npx.cmd playwright install chromium` exit 0，`install --list` 确认 1.62.1 的 Chromium、headless shell、ffmpeg 与 winldd。Playwright 以 `reuseExistingServer: false` 启动真实 FastAPI/Vite，Vite `/api` 代理到 127.0.0.1:8000；没有应用 API interception、真实 key/Planner call、raw fields、localStorage、sleep 或 create-run UI。
- GREEN 与验证：E2E 2/2 passed，浏览器实际点击中文“批准”；直连 API 在点击前证明 `waiting_approval` 与字符串 approval id，点击后证明 `completed` 且事件含 `approval_approved`、`tool_succeeded`、`run_finished`。320x720 中批准按钮可见，HTML/body `scrollWidth <= window.innerWidth`；未发现真实 CSS 缺口，故未改样式。`npm.cmd test` 为 10 files/48 tests，`npm.cmd run build` 成功；完整 backend 为 `158 passed, 1 warning`，warning 是既有 Starlette/TestClient 弃用提示。`git diff --check` 无输出，高置信 staged 凭据候选计数 0。
- 提交与当时状态：实现提交 `e18422e test: add real workbench e2e coverage`。当时下一步是 fresh read-only spec/security reviewer 与质量 reviewer；该审查及 320px Important 的 RED→修复→复审实际结果记录在下一节。本条保留的是实现提交当时状态，不代表当前仍待首次审查。

### 2026-08-10 — Task 13 Task 4：最终验证与视口审查闭环（本地完成，未收尾分支）

- 审查与 TDD：Task 4 的初始 read-only spec/security review 为 C/I/M `0/0/0`；quality review 为 `0/1/0`，指出 320px E2E 的 `toBeVisible()` 未证明实际视口可达。fresh implementer `/root/t13_task3_viewport_fixer` 只处理该项：先以真实元素 bounding-box 交集断言 RED，Chromium 实测底边 `1327.4375 > 720`；最小实现提交 `5ed4bd3 fix: keep mobile approval action in viewport`，仅把既有 `ApprovalPanel` 移至时间线之前。随后 scoped spec/security 与质量 re-review 均 PASS（C/I/M `0/0/0`）。未改 API、CSS、policy、旧项目代码、安全 DTO、凭据或 create-run UI。
- 协调最终控制验证：使用本 worktree 忽略的 `.venv`，`pytest backend/tests --basetemp .pytest-tmp\\task13-final -q` 为 `158 passed, 1 warning`（既有 Starlette/TestClient 弃用警告）；`scripts/run_demos.ps1` 输出三段稳定 JSON。clean `npm.cmd ci --ignore-scripts` 后，unit 为 `10 files/48 tests`、`npm.cmd run build` 成功、真实 Chromium `npm.cmd run test:e2e` 为 `2 passed`。install 报 5 个上游审计风险（3 moderate、1 high、1 critical），未运行 `npm audit fix --force`。
- 过程/安全核验：`git diff --check codex/t12-settings-approval-ui..HEAD` 无输出；变更非文档源码的高置信凭据形态候选计数 0。Task 9 的 config/LLM/secret-store/route 专属源和测试相对 `codex/t09-planner-credentials` 无 diff；Task 10 的 workspace/upload/route 专属源和测试相对 `codex/t10-workspace-upload` 无 diff。共享 `main.py`、runs API 和 run service 的差异属于已记录的 Task 1/Task 11 集成，未误写为 T9/T10 安全模块变更。
- 人工干预与当时边界：协调会话只执行当轮复验、准确回填过程文档和保存 ignored rerun report，未改产品代码、未 push、未创建 PR #13、未运行 `finishing-a-development-branch`。该轮原拟下一步进入分支处置，但随后最终全分支审查发现下节所述问题；其最终 scoped re-review 结果见下节。Task 14（CI/容器）、Task 15（部署/最终交付）及延后策略扩展仍未开始。

### 2026-08-10 — Task 13 最终全分支审查修复波（scoped re-review：C/I/M 0/0/2，文档 Minor 已修正）

- 执行者与技能：fresh fix agent `/root/t13_final_fix` 使用 `systematic-debugging`、`test-driven-development` 与 `verification-before-completion`；范围只包含最终 reviewer 的 E2E 凭据隔离 Important 和文档一致性 findings，不 push、不建 PR、不进入 Task 14/15/policy。
- 根因证据：Playwright 原命令启动 `safe_code_harness.api.main:app`；前端 Planner 初始 GET 经 `get_planner` → `PlannerConfiguration.snapshot()` → `SecretStore.get()` → `_require_adapter()` 构造 Windows Credential Manager。非破坏性运行时 probe 替换该构造器后，GET 返回固定 503 且 `credential_manager_probe_calls` 为 1，证明问题来自 E2E 入口而非 Planner DTO 或浏览器拦截。
- TDD RED/GREEN：新增 `backend/tests/integration/test_e2e_app.py`，禁止构造 Windows Credential Manager并请求精确 E2E app 的 Planner DTO；首次 focused 为 `1 failed, 1 warning`，预期失败是 `ModuleNotFoundError: safe_code_harness.api.e2e_app`。最小实现新增 E2E-only `create_e2e_app()`，向既有 `create_app()` 注入初始为空的进程内 SecretStore，并将 Playwright uvicorn 命令切至 `safe_code_harness.api.e2e_app:app`；生产 `main:app` 未改。focused GREEN `1 passed, 1 warning`，提交 `7d66d98 fix: isolate browser e2e credentials`。
- 文档修正：`PROJECT_PROGRESS.md`、`PLAN.md`、本日志与 handoff 统一 Task 3 已经初始审查、Task 4 视口修复已复审；追踪矩阵不再把已实现的 AgentLoop、反馈/记忆、六维与 API 集成写成待开发，并修复 A 表 separator 列数；设计删除 guardrail demo 创建临时工作区的虚假声明；README 增加本地 E2E 命令及内存凭据/无外部 Planner 边界。最终 scoped re-review 为 Critical 0、Important 0、Minor 2；两个 Minor 为测试数值的历史/当前措辞和追踪矩阵的状态词，已以本次纯文档修正关闭。
- 修复后控制证据：完整 backend `159 passed, 1 warning`，warning 仍为既有 Starlette/TestClient 弃用；`scripts/run_demos.ps1` 输出三份稳定 JSON；clean `npm.cmd ci --ignore-scripts` 安装 179 packages 后仍报告 5 个既有上游审计风险（3 moderate、1 high、1 critical），未 force fix；前端 unit `10 files/48 tests`、build 成功、真实 Chromium E2E `2 passed`。最终 diff/凭据扫描及本次文档的只读复核仍是进入分支收尾前的门槛。
### 2026-08-10 — Task 13：分支收尾

- 最终验证在 `e4599d2` 后重新运行：backend `159 passed, 1 warning`、三份稳定 JSON demo、前端 10 files/48 tests、build 和真实 Chromium E2E `2 passed`，均成功；warning 为既有 TestClient 弃用。
- 收尾决定：按课程“每个独立模块一个 PR”和 stacked 分支规则，用户选择 `finishing-a-development-branch` 选项 2。已推送 `codex/t13-demos-e2e` 并创建目标为 `codex/t12-settings-approval-ui` 的 [draft PR #13](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/13)；保留 worktree 等待审查反馈。Task 14/15、策略扩展仍未开始。

### 2026-08-10 — Task 14：CI 与 OCI 分发实现（待两阶段审查）

- 执行者、技能与范围：fresh implementer `/root/t14_implementer` 在独立 `codex/t14-ci-distribution` worktree 使用 `executing-plans`、`using-git-worktrees`、`test-driven-development`、`systematic-debugging` 与 `verification-before-completion`。prompt 绑定只做 GitHub/GitLab CI、Docker/GHCR 分发和四份过程记录；未开始 Task 15/部署/策略扩展，未读取或复用旧项目代码，未使用真实 key，未 push/建 PR。
- TDD RED：先只新增计划绑定测试，focused exit 1，精确为 `.github/workflows/publish-image.yml` 不存在的 `FileNotFoundError`；再在任何分发配置前扩展 push CI、默认分支/packages 权限、精确 `unit-test`、`make test` 双端核心测试、多阶段 FastAPI 静态服务、Compose 健康和无烘焙 key 契约，得到 `7 failed`。初次 GREEN 的唯一失败是测试把合法 `os.environ` 误判为 `.env` 文件；收窄为禁止 COPY/加载 `.env` 后 focused `7 passed`。
- 实现：新增 `.github/workflows/ci.yml`（每次 push/PR 的 Windows 后端、demo、前端、Chromium E2E，并在 Ubuntu 构建 Docker）、`publish-image.yml`（仅默认分支、`packages: write`、`GITHUB_TOKEN`、GHCR）、`.gitlab-ci.yml`（顶层精确 `unit-test`）、多阶段 `Dockerfile`、加固的 Compose 与 `.dockerignore`。镜像以非 root 用户运行、健康检查 `/api/runs`、FastAPI 挂载 WebUI；Linux 容器 Planner secret 只在进程内存，可由托管平台 secret 环境初始注入，不进入构建参数、层、Compose 或 `.env`。README 明确 Windows Credential Manager、容器环境风险、公开 package 需外部设置且未验证。
- 验证与调试：本机 Python 3.14.5 满足 `>=3.12`；baseline backend `159 passed, 1 warning`、frontend `48 passed`、build/E2E `2 passed`。最终 backend `166 passed, 1 warning`（同一既有 Starlette/TestClient 弃用），frontend `48 passed`、三份稳定 JSON demo、build、E2E `2 passed`，Compose config 成功。首次 Docker 因 daemon 未启动失败；后续 Compose 等 Docker Desktop 启动后实际构建成功并 healthy。预提交 E2E 的 8000 冲突经只读进程证据定位为本任务 Compose 容器而非 Playwright 遗留；使用 `compose --wait` 后 `/api/runs` 可访问、Planner JSON 为 `configured:false`、根页 200/含 WebUI，镜像配置 baked key 计数 0，随后只清理本任务容器/网络。GNU Make 不存在，故 `make test` 未运行；其两个子命令均实际通过。`npm ci` 仍报告既有 5 个审计风险（3 moderate、1 high、1 critical），未执行 force fix。
- 提交与外部边界：源码提交 `0f2b35f build: add ci and container distribution`；提交前 `git diff --cached --check` 无输出，高置信凭据候选计数 0。外部 GitHub Actions、GitLab pipeline、GHCR push/public pull、package visibility 未运行/未验证；下一步必须先做独立 spec/security 审查，再做代码质量审查，修复 findings 后才可进入 `finishing-a-development-branch`。

### 2026-08-10 — Task 14：初审修复 round 1（待 scoped re-review）

- 审查与根因：独立 reviewer `/root/t14_reviewer` 给出 C/I/M=`0/3/3`。逐项检查确认：Makefile 默认 `python3` 与 README 的 `.venv` 安装路径断裂；Compose/README `8000:8000` 会把没有认证的审批、配置和上传 API 暴露到所有网卡；`.dockerignore` 虽有根 dotenv 规则，但测试既不读取它也不固定嵌套 frontend 变体；独立 publish push workflow 不依赖 CI 成功。追踪矩阵 G-4.7-1/2 仍误写 Task 13 无 PR，README Windows 反斜杠与 API 解释器也不准确。
- TDD：在修配置前扩展 `test_distribution_config.py`。RED 为 `4 failed, 5 passed`：分别缺 `workflow_run` 成功/default push/被测 SHA，缺 `.venv/bin/python`，缺 `127.0.0.1`/无认证 gateway 文档，缺 `**/.env` 与 `**/.env.*`。最小实现后 focused `9 passed`；删除任一门禁、loopback 或 dotenv 规则会再次失败。
- 修复：`1434a64 fix: harden ci distribution boundaries`。Make 默认实际仓库 venv；GHCR 只在名称为 CI 的 workflow 对默认分支 push 成功后触发，并 checkout `workflow_run.head_sha`；Compose 和两条 Docker run 示例仅绑定 loopback；README 明确应用无认证，公网必须有认证与 TLS gateway；`.dockerignore` 同时保护根和任意嵌套 dotenv；Windows/Unix venv 与 uvicorn 命令已分开纠正。未改 Harness/API、未进入 Task 15、未读旧项目、未用真实 key。
- 验证：backend `168 passed, 1 warning`（既有 TestClient 弃用），frontend `48 passed`，三 demo、production build、真实 Chromium E2E `2 passed`；Docker build 和 Compose config 通过，Compose healthy 后 `docker port` 精确为 `127.0.0.1:8000`，runs API 返回 200/`[]`，WebUI 根页 200，随后只清理本任务容器/网络。GNU Make 在此 Windows 主机仍不存在，故未虚称执行；其 backend/frontend target 命令均通过。提交前凭据候选计数 0。
- 状态：Task 13 draft PR #13 的追踪陈旧项已纠正。外部 GitHub/GitLab CI、GHCR push/public pull/package visibility 仍未验证；本轮待 scoped re-review，未 push/PR/finish。

### 2026-08-10 — Task 14：scoped re-review 与最终文档 Minor

- 审查结论：`1434a64` 后 scoped spec/security 与代码质量 re-review 均通过。最终全分支 reviewer 给出 C/I/M=`0/0/1`；唯一 Minor 是 PLAN 的 Task 13/14 状态、交接/追踪矩阵的复审状态以及 README E2E 环境仍带 Task 13 专属措辞，未发现新的产品、CI、Docker、凭据或测试问题。
- 本次范围：仅修正文档事实，明确 Task 13 已推送并有 draft PR #13、Task 14 CI/容器已经实现且 scoped reviews 通过、最终 Minor 正在关闭，并将 E2E 环境改称 repository/worktree-local `.venv`。未改产品/config/tests，未进入 Task 15，未 push/PR/finish；外部 CI/GHCR 仍未验证。
### 2026-08-10 — Task 14：分支收尾

- 按课程“每个独立模块一个 PR”和 `finishing-a-development-branch` 选项 2，已推送 `codex/t14-ci-distribution` 并创建目标为 `codex/t13-demos-e2e` 的 [draft PR #14](https://github.com/AlterGo-xzy/safe-code-harness-v2/pull/14)。保留 worktree 等待审查；外部 CI/GHCR/匿名拉取和任务 15 仍未完成。

### 2026-08-10 — Task 15：本地发布资料与证据实现（实施阶段记录）

- 执行者与范围：fresh implementer `/root/t15_implementer` 在隔离的 `codex/t15-release-evidence` worktree 使用 `executing-plans`、`using-git-worktrees`、`test-driven-development` 与 `systematic-debugging`。只实现任务 15 的本地发布资料/测试/记录；未读取或复用旧项目代码，未改 Harness、Task 14 CI/Docker 配置或延后策略功能，未使用真实 key，未 push/建 PR/finish。
- TDD RED/GREEN：先新增 `backend/tests/unit/test_release_docs.py`，再运行 `.\.venv\Scripts\python.exe -m pytest backend\tests\unit\test_release_docs.py -q`；RED 为 `1 failed`，前两项 `docker pull`/`Credential Manager` 已满足，精确缺少“已知限制”。随后中文重写 README 并新增 MIT `LICENSE`、`THIRD_PARTY_NOTICES.md`、PR 模板、只含学生本人写作门禁/提纲的 `REFLECTION.md` 占位；focused GREEN `1 passed`，提交 `9acb2ae docs: add reproducible release documentation`。
- 回归调试：首次完整 backend 为 `1 failed, 168 passed, 1 warning`，现有 Task 14 测试证明中文重写遗漏精确英文安全契约 `does not implement authentication` / `authentication and TLS gateway`。先复现 focused RED 并对比最近 README diff；第一次只恢复首个短语后相邻断言仍 RED，随后完整读取测试函数，以单一双语句恢复两个固定契约。focused `2 passed`、完整 backend 恢复 GREEN；提交 `60528ae docs: preserve distribution security contract`。这两句保留的是无认证/公网网关安全边界，不是翻译装饰。
- 完整本地验证：新 worktree 自建被忽略 `.venv` 并安装 `backend[dev]`；clean `npm.cmd ci --ignore-scripts` 安装 179 packages，仍报告 5 个既有上游风险（3 moderate、1 high、1 critical）和 `whatwg-encoding` deprecation，未运行 `--force`。最终 backend `169 passed, 1 warning`（既有 Starlette/TestClient 弃用）、三份稳定 JSON demo、frontend `10 files/48 tests`、production build、真实 Chromium E2E `2 passed`；E2E 前后 8000 listener 均为 0。本机无 GNU Make，未虚称执行 `make test`，其 backend/frontend 实际 target 均通过。
- 凭据与许可证证据：对已跟踪文件和 `git log -p --all` 的 110 个本地可见提交扫描高置信 OpenAI/GitHub/私钥形态；2 个候选只位于 `test_memory.py` 和 `test_rules.py`，脱敏上下文证明它们是验证脱敏/阻断的固定合成 fixture。排除这两处后 tracked/history 未分类候选均为 0；没有输出候选值。第三方直接依赖许可证来自本地 Python distribution metadata 与已提交 npm lockfile；任务 15 本地源码采用 MIT。
- 外部阻断与下一步：没有 NJU Git 远程地址、托管平台/认证 TLS gateway、GHCR public 设置或学生反思正文；stacked PR 尚未合并，GitHub/GitLab 最终 CI、GHCR 未登录 pull/run、公开 HTTPS URL 均没有真实结果，故不尝试也不宣称。下一步必须 fresh read-only reviewer 先做 SPEC/课程 traceability 审查，再做文档/质量审查；修复所有 Critical 后才可由协调会话继续外部核验或分支收尾。

### 2026-08-10 — Task 15：本地两阶段审查闭环

- 审查结论：独立 spec/traceability 与文档/质量审查的初审汇总为 C/I/M=`0/0/1`。唯一 Minor 是根 `PLAN.md` 的 Task 14 Step 5、完成记录和修复记录仍保留 PR #14 建立前的陈旧状态；没有产品、测试、凭据、许可证或安全边界 finding。
- 修复与复审：只用 `apply_patch` 修改 `PLAN.md`，记录 Task 14 审查/修复已通过、branch 已推送、stacked draft PR #14 已创建且 branch/worktree 保留；外部 GitHub/GitLab CI 和 GHCR public/匿名 pull-run仍未验证。`git diff --check` 无输出，提交 `93f3415 docs: align task 14 completion history`；限定复审 C/I/M=`0/0/0`。
- 当前边界：Task 15 本地实现和审查已闭环，提交链为 `9acb2ae`、`60528ae`、`84a10b4`、`93f3415`。没有 push、Task 15 PR 或 `finishing-a-development-branch`；NJU remote、认证/TLS 公网 URL、GitHub/GitLab 最终实跑、GHCR public/匿名 pull-run 和学生本人反思仍未完成，因此 Task 15 整体状态保持未完成。

### 2026-08-10 — Task 15：NJU Git 推送与流水线读取尝试

- 人工授权与推送前验证：用户提供并授权使用 `https://git.nju.edu.cn/xzy241276010/safe-code-harness-v2.git`。协调会话确认当前 worktree 干净、`git diff --check HEAD` 无输出，并重新运行 backend `169 passed, 1 warning`、三份稳定 JSON demo、frontend `10 files/48 tests`、production build 与真实 Chromium E2E `2 passed`。
- 外部动作与结果：本地新增 `nju` remote 后执行非强制 `git push --set-upstream nju codex/t15-release-evidence`；远程创建同名分支并设为上游，未覆盖已有分支。Git 输出提供了新建 merge request 的 URL，但没有创建 MR。
- 外部阻断：对 GitLab REST pipeline endpoint 的匿名只读请求返回 Anubis “Making sure you're not a bot” 人机验证页面，而非 pipeline JSON，故没有可复核的 GitLab CI 结果。没有尝试绕过该保护，也未宣称 pipeline 成功。GitHub CI、GHCR public/匿名 pull-run、认证 TLS 公网部署、学生反思正文、Task 15 PR 和分支收尾仍待完成。

### 2026-08-10 — Task 15：GitLab `File` CI 失败修复

- 外部失败证据与根因：用户提供 GitLab `unit-test` 日志，`src/api/workspaces.test.ts` 三项均在 `new File(...)` 处以 `ReferenceError: File is not defined` 失败。配置核对显示 Vitest 强制 `environment: node`，而 GitLab `python:3.12-bookworm` 通过 apt 安装系统 Node；本机 Node 24 有 `File`，因此不能把本地绿误写为 CI 兼容。
- TDD：先新增 `frontend/src/test/file-polyfill.test.ts`，在 File-free target 导入缺失模块得到预期 RED；最小实现 `file-polyfill.ts` 仅在 `File` 缺失时从 Node `node:buffer` 安装构造器，并由 setup 调用。focused GREEN `1 passed`。首次 build RED 为缺少 `node:buffer` 类型声明；检查 `npm ls @types/node --all` 为 empty 后，仅新增精确 dev dependency `@types/node@20.17.57`，build 随后 GREEN。
- 完整本地验证：backend `169 passed, 1 warning`（既有弃用 warning）、三 demo、frontend `11 files/49 tests`、build、Chromium E2E `2 passed`。下一步是提交并推送这项最小修复，获取 GitLab 的真实复跑状态；未改 Harness/上传业务或凭据边界。
- 推送：提交 `749199a fix: support GitLab Node File tests` 已推送至 `nju/codex/t15-release-evidence`，GitLab 已接收更新并给出 merge request 创建 URL。`glab` 未安装，匿名 REST API 仍被 Anubis 拦截；等待用户网页登录 GitLab 查看并提供该复跑的真实 pipeline 状态。
- 外部结果：用户提供 GitLab pipeline 页面截图，记录初始失败 job #610227 / pipeline #319719（`1215581`），以及修复后的通过 job #610231 / pipeline #319723（`749199a`）和 job #610232 / pipeline #319724（`87b432d`）。这满足 GitLab `unit-test` 的最后通过记录；不因此推断 GitHub CI、GHCR 或部署已完成。
- GitHub 外部结果：协调会话使用已认证 `gh` 查询 [Actions run 31373926124](https://github.com/AlterGo-xzy/safe-code-harness-v2/actions/runs/31373926124)，结论 `success`；test job 成功执行 backend tests、demos、frontend tests、build、Playwright Chromium E2E，docker-build job 也成功。该 run 的 head 为 `87b432d`；不因此推断 GHCR 发布或公开性已完成。

### 2026-08-10 — Task 15：Railway Mock 演示站范围确认

- 人工决策：用户确认保留 Railway URL `https://safe-code-harness-v2-production.up.railway.app`，但不购买域名、不配置认证网关；后续认证生产部署作为扩展。
- 外部证据与边界：用户提供的浏览器截图显示工作台首页“暂无运行记录”。该状态符合空的运行列表；它不是实际 Harness 操作或真实 key 的证据。应用没有内建认证，故演示站必须保持 Mock LLM、无真实 Planner key、无敏感工作区上传；不得把 URL 写成安全生产部署完成。
- 文档动作：同步 README、进度、计划、追踪表和 handoff；将“可访问 WebUI URL”标为 Mock 演示范围已验证，而认证/TLS 安全边界保留为后续扩展。未修改 Harness、CI、Docker 或部署配置，未读取/输出/配置任何凭据。

### 2026-08-10 — Task 15：Railway/GitHub/GHCR 外部只读核验

- 推送：用户授权后，`6aa5274 docs: scope Railway as mock demonstration` 已推送到 GitHub `origin/codex/t15-release-evidence` 和 NJU `nju/codex/t15-release-evidence`；未创建 PR、未合并。
- Railway：对 `https://safe-code-harness-v2-production.up.railway.app` 的只读 HTTP 根请求得到 `200`。响应为 SPA 静态文档，未包含运行时中文空状态文字；空状态仍仅以用户浏览器截图作为证据。
- GitHub/GHCR：GitHub Actions run `31379732809`（head `6aa5274`）在观察时为 `in_progress`；`gh run watch` 在 55 秒窗口超时，未取得结论。`gh api /users/AlterGo-xzy/packages?package_type=container` 返回 403，明确要求 `read:packages` scope；未尝试改变 token scope、查询私有值、登录/登出 Docker，不能由此推断 GHCR 是否存在或公开。
- 后续同轮结果：用 `gh run view` 读取同一 run 的最终 JSON，结论为 `success`；`test` job 的 backend tests、demos、frontend tests、build、Playwright Chromium E2E 均成功，`docker-build` job 也成功。该结果证明 push CI 与容器构建，不证明 GHCR 已发布或允许匿名拉取。

### 2026-08-10 — Task 15：发布前置依赖只读盘点

- 只读结果：`gh pr list` 显示 PR #1-#14 全部为 draft，形成从 #1 的 `main` 到 #14 的 stacked 链；Task 15 没有 PR。按 `.github/workflows/publish-image.yml` 查询 GitHub 默认分支返回 HTTP 404，证明该工作流尚未到达默认分支。
- 结论：当前没有可运行的默认分支 GHCR 发布工作流，不能尝试/宣称 GHCR push、package public 或匿名 pull。下一步是学生审查并明确授权如何顺序合并 stacked PR；Task 14 合并后还需等待默认分支 CI 成功。该结论是流程依赖，不是代码或容器失败。

### 2026-08-10 — Task 15：用户提供反思正文

- 人工输入：用户在对话中提供完整 `REFLECTION.md` 正文；协调会话使用 `apply_patch` 原样写入，未代写、扩写或润色。
- 客观核验：中文汉字计数 `1583`，全部非空白字符计数 `2852`；`backend/tests/unit/test_release_docs.py` 为 `1 passed`，`git diff --check` 无输出。中文“字”口径下符合 1500–2500；若课程平台按非空白字符计数，学生须自行判断和修改。

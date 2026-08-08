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
- 后续：此修复待独立复审，随后才可更新 Task 2 完成状态并开始 Task 3。完整修复报告将写入 `.superpowers/sdd/2026-08-09-demos-e2e/task-2-fix-report.md`（忽略文件）。

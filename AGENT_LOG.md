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

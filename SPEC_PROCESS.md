# 规约生成过程

## 过程边界

本仓库是全新重建。旧 `safe-code-harness` 仓库只能作为只读技术参考，不能作为新仓库的实现历史。`SPEC.md`、`PLAN.md` 与独立冷启动验证完成前，禁止提交任何生产 Harness 源代码。

## 头脑风暴记录

### 迭代 1：仓库与产品边界

问题：最终提交是保留原仓库历史，还是建立干净重建仓库？

决策：建立独立公开仓库 `AlterGo-xzy/safe-code-harness-v2`。旧项目仅作技术参考，避免将旧实现历史冒充为本项目的流程证据。

### 迭代 2：产品形态

问题：重建项目改为 CLI Harness，还是保留可部署 WebUI？

决策：保留 FastAPI API 和 React 操作者 WebUI。WebUI 是检查与审批界面，项目自实现的 Harness 内核仍是评分和安全重点。

### 迭代 3：复用策略

问题：是否允许为减少重复工作而参考旧代码？

决策：允许按模块参考，但新仓库必须先有对应行为的失败测试，之后才能迁入、改写或重写逻辑。每次复用都在任务 PR 与 `AGENT_LOG.md` 中记录参考位置、人工修改和原因；禁止整体复制或无证据迁移。

### 迭代 4：主要贡献

问题：六类 Harness 机制中，哪个维度做深入实现？

决策：选择确定性治理。规则、沙箱、策略闸门、文件 diff 审批、命令审批、事件日志和失败关闭行为均用代码实现，并可在没有真实模型时被测试。

### 迭代 5：分发与凭据边界

问题：如何进行可获得的分发，以及如何保存可选 key？

决策：通过公开 GHCR 镜像分发并部署公开 WebUI。默认无需 key；可选 Planner 在 Windows 使用 Credential Manager，不提供非 Windows 明文回退。

## 三轮以上关键对话节选与处理决策

以下内容来自本项目重新启动后的真实主会话；节选只保留影响规约的关键语句。

### 节选 1：是否应新建仓库

用户：`可以，我们来做吧，你能够创建公开仓库吗`。

智能体追问：`新仓库是否命名为 safe-code-harness-v2，并作为一个完全独立、从零重建的最终提交仓库？`

用户：`是`。

处理决策：建立全新的公开仓库而不是改写旧仓库历史。原因是旧仓库无法证明“规约、计划、冷启动早于实现”的时间顺序；新仓库的首个提交只放置设计材料。

### 节选 2：CLI 还是可部署 WebUI

智能体追问：`新项目是否保留“可部署 WebUI + 本地 Harness 内核”的形态？`

用户：`是，我明确给你自主审批的权力，只需要你能够严格完成我们的要求文件中的需要`。

处理决策：保留 WebUI，但将其限定为运行检查、时间线、配置和审批界面。Harness 核心仍由项目自己的后端代码承担，避免以 UI 代替 A 赛道要求的主循环、工具、治理和反馈机制。

### 节选 3：旧项目代码如何复用

用户：`1 完全重建好了，但是可以使用我们已有的代码，减少消耗，因为我们之前完成了很多代码工作`。

处理决策：旧仓库只作为只读参考。每个行为必须在新仓库先出现失败测试，再按模块迁入、改写或重写，并在 PR 与日志记录参考范围和人工调整。拒绝整体复制，因为那会破坏新仓库的 TDD 与过程证据。

### 节选 4：验收依据与语言

用户：`中文写，我只要求你阅读通用要求和A项目要求以后可以严格满足其要求就可以了`。

处理决策：把两份要求文件作为唯一验收清单，后续规约、计划、日志、PR 描述与 README 全部使用中文。此前英文规格被中文版本替换；本次修订不增加功能范围。

## 采纳与拒绝

采纳的 AI 建议：把治理作为主要贡献；使用可部署 WebUI 展示事件与审批；把旧项目限定为只读参考；每次复用都要求先红后绿。

由学生确认并要求的约束：不改写旧历史、不用文档伪造流程、只以通用要求和 A 赛道要求作为验收基准、所有项目材料使用中文。

拒绝的方向：整体迁移旧代码，因为它无法提供“规约、计划、冷启动在实现之前”的真实证据；将同类型 subagent 称作不同类型冷启动 agent，因为这会违反要求。

## 对 brainstorming 的反思

做得好的地方：分段确认迫使项目先回答“为什么是 Harness”“谁使用它”“哪一项机制做深”，从而避免把旧项目的 UI 和功能清单不加选择地搬入新仓库。围绕旧代码复用的追问也把“节省工作量”变成了可审计的先测后迁入规则。

不满意的地方：单靠迭代摘要很容易看起来像过程证据，但不能让评阅者判断真实问题、用户决定和规格变更之间的关系。因此本项目额外保留了关键对话节选，并用要求追踪矩阵把每个承诺转成可观察的完成门槛。另一个局限是不同类型冷启动 agent 不能由同一种 Codex 子 agent 替代，这一外部能力必须在实现前真实解决。

## Superpowers 安装与使用证据

主开发环境为 Codex Desktop，已安装官方插件 `superpowers@openai-curated-remote`，版本 `6.2.0`，本地路径为 `C:\Users\Admin\.codex\plugins\cache\openai-curated-remote\superpowers\6.2.0`。规格阶段实际调用 `using-superpowers` 与 `brainstorming`；后续将按任务真实调用 `writing-plans`、`using-git-worktrees`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`finishing-a-development-branch`，并即时写入 `AGENT_LOG.md`。

## 冷启动验证：Claude Code 对任务 1 的审阅

### 执行记录与输入隔离

2026-08-04，学生使用与主开发 Codex Desktop 不同类型的 Claude Code `2.1.220` 运行冷启动审阅。密封 prompt 只给出了本仓库 commit `fc9b754` 中 `SPEC.md` 和 `PLAN.md` 的两个 raw URL，并明确禁止读取其他仓库文件、主会话历史或实现代码；完整 prompt、PowerShell 启动记录、Fetch 工具轨迹与 Claude 的原始输出见 [`docs/evidence/cold-start-claude-code-task1.md`](docs/evidence/cold-start-claude-code-task1.md)。

第一次未登录会话在调用任何工具前终止。实际审阅由重新执行 `claude`（没有 `--resume`）启动；其工具轨迹只显示两次对上述 raw URL 的 `Fetch`，随后显示 `read 2 files`，没有本地读取、shell、编辑或提交调用。该 agent 选择任务 1，说明了失败测试和预期红色结果，然后在发现四项不确定性后停止提问。它没有提交或建议任何实现代码。这构成“不同类型、全新启动、仅凭 SPEC+PLAN、遇歧义暂停”的冷启动验证证据。

### Claude 暂停的位置与判断

| 问题 | 判断 | 处理决定 |
| --- | --- | --- |
| `pyproject.toml` 的包名、Python 版本、依赖、src layout 与 pytest 配置缺失 | 规约缺失，不是 Claude 误读 | 在 SPEC 9.1 与 PLAN 任务 1 固定发布名、导入名、Python 版本、setuptools 配置、依赖引入时机和 pytest 配置。 |
| 根目录 pytest 命令不能自然找到 `backend/src` | 规约缺失；原 PLAN 的“红色结果”无法稳定复现 | 选择测试进程内 `conftest.py` 显式添加 src 路径；绿色后用独立 `python -c` 验证 editable install，避免 conftest 掩盖打包错误。 |
| `conftest.py` 职责未定义 | 规约缺失 | 任务 1 仅允许其负责路径注入，不预建无用途 fixture 或业务代码。 |
| Windows 下 `Makefile` 与一键测试范围未定义 | 规约缺失 | 以 `scripts/test.ps1` 作为任务 1 的规范入口，仅跑已存在的 backend unit 测试；`Makefile` 延后至任务 14 的 CI/容器阶段。 |

### 关键修订前后 diff

| 修订前 | 修订后 |
| --- | --- |
| 任务 1 只列文件名，使用模糊的 `python -m pytest ...`，没有定义打包、导入或 Windows 测试约定。 | SPEC 9.1 固定 `safe-code-harness` / `safe_code_harness`、`>=3.12`、src layout、最小依赖和 PowerShell 入口。 |
| `conftest.py`、`Makefile` 均被列为创建项，但没有职责和运行范围。 | `conftest.py` 只做 src 路径注入；`scripts/test.ps1` 为一键入口；`Makefile` 明确延后到任务 14。 |
| 红色阶段与 editable package 安装的关系未定义。 | 红色阶段用测试路径注入得到确定的 `ModuleNotFoundError`；绿色阶段再执行 editable install 和无 conftest 的独立导入验证。 |

### 差距与结论

Claude 的产出没有误解领域目标；它暴露的是工程基线没有被写成可独立执行的约定。修订后，任务 1 已具备明确文件、顺序、命令、红色期望、绿色期望和 Windows 入口。转录提供了 Claude 版本、非 resume 启动、只 Fetch 两份文档和暂停提问的客观证据；本轮修订已在实现前提交。任务 0 的冷启动门槛通过，后续任务仍必须在独立 worktree、fresh subagent、TDD 和两阶段审查下执行。

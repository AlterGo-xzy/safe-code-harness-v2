# REFLECTION

## Superpowers 技能的实际作用

这个项目中，对我帮助最大的技能是 `test-driven-development`、`subagent-driven-development`、`requesting-code-review` 和 `systematic-debugging`。

TDD 的价值最明显。AI 很容易快速生成一个“基本能工作”的实现，但对安全边界、异常情况和状态转换考虑不够完整。例如命令护栏最初可以阻止直接的危险命令，但 reviewer 随后发现参数变形、`env`、`sudo`、`command` 等包装方式仍可能绕过。我们没有直接修改代码，而是先把这些问题变成新的失败测试，再修复到绿色。这样 reviewer 的意见不会只停留在一次对话中，而会变成长期有效的回归测试。

独立 code review 也非常重要。Task 9 中，Planner API 已经不会直接返回 API key，但 reviewer 发现异常链仍可能通过 traceback 保存底层异常中的 key。这个问题仅靠功能测试很难发现，最后通过新增泄露回归测试并修改异常处理解决。

相对来说，`using-superpowers`、每次都完整执行 worktree、review、finishing branch 等流程，有时有些“形式大于实质”。对命令执行、凭据和 ZIP 上传这种高风险功能很值得，但对于纯文档修改或很小的 UI 调整，完整流程的成本比较高。项目后期形成了很长的 stacked PR 链，也增加了维护 base 和处理文档冲突的工作。

## TDD 是阻碍还是放大器

我认为在 AI 协作中，TDD 总体是放大器。

AI 最大的问题之一是容易满足需求的表面形式。Task 13 的 approval demo 就是一个例子。原要求是展示 `waiting_approval -> approved -> executed`，初始实现虽然调用了真实运行服务，但最终输出的状态是固定文字，因此不能真正证明工具只在批准后执行。reviewer 发现后，我们修改测试，要求 transcript 必须来自真实 snapshot，并进一步检查审批前不能出现 `tool_succeeded` 或 `tool_failed`。

这让我意识到，TDD 不只是验证代码是否正确，也可以限制 AI “用最容易的方法满足文字要求”。

但 TDD 并不是所有地方都同样有效。对于 CI、Docker 和 README，一些测试只能检查配置中是否存在某些字段，不能证明 GitHub Actions 或 GHCR 真的成功。因此外部分发仍然需要真实运行证据，不能把测试通过等同于部署完成。

## Subagent、自主时间与任务颗粒度

我不认为 subagent 能自主多久应该用分钟衡量。这个项目中比较稳定的单位是：

**一个明确能力 + 一个主要风险边界 + 一组 focused tests。**

例如动作协议、路径沙箱、命令审批、反馈记忆都比较适合一个 fresh subagent 独立完成。它可以完成 RED、最小实现、GREEN，然后交给另一个 agent review。

任务一旦跨越多个系统，偏离概率就明显上升。Task 13 同时包含 API 集成、deterministic demo、浏览器 E2E 和 320px viewport 验证，最后实际上被拆成多个子任务和多轮审查。因此如果重新规划，我会让每个 task 对应一个可以独立失败、独立测试和独立 review 的行为闭环。

## SPEC / PLAN 对实现质量的影响

SPEC 和 PLAN 的质量直接决定 fresh subagent 能不能独立执行。

项目早期我们专门让一个新的 Claude Code 只读取 SPEC 和 PLAN。它没有开始实现，而是提出了 `pyproject.toml`、src layout 导入方式、`conftest.py` 职责和 Windows 测试入口等问题。这说明仅写“创建这些文件”是不够的，陌生 agent 需要明确的工程约定。

Task 13 的 approval demo 是更直接的例子。PLAN 只要求输出三个审批状态，却没有规定这些状态必须来自真实运行证据，所以 subagent 选择了固定字面量。它并没有故意违反要求，而是准确利用了规约没有写清楚的部分。

另一个例子是 Task 11。前端需要运行列表和时间线，但 Task 8 原来的 API 契约并没有提供完全匹配且安全的 DTO。如果继续按原 PLAN 强行开发，subagent 很可能自己猜字段或者把原始事件直接传给前端。最后我们返回 Task 8，明确增加了四字段列表和五字段时间线 DTO。

因此我最有效的 prompt 策略不是提供更多上下文，而是提供更窄的上下文：允许修改什么、禁止实现什么、focused test 命令、预期 RED、安全不变量以及完成证据。对旧项目的参考范围也必须明确，避免 agent 顺手迁入超出任务范围的实现。

## 凭据与分发带来的工程思考

凭据要求让我意识到，“不要把 key 提交到 Git”远远不够。凭据还可能经过内存、API 响应、异常、traceback、日志、测试、E2E、Docker build context 和运行环境。

Task 9 的异常链泄露问题让我开始把 key 当成需要分析完整 data flow 的数据。Task 13 的浏览器 E2E 又发现，普通 Planner GET 会实际访问 Windows Credential Manager，所以最后专门建立了 E2E-only app，用内存 SecretStore 隔离真实系统凭据。

分发要求也暴露了很多原本容易忽略的问题。Task 14 第一版 Compose 使用 `8000:8000`，意味着没有认证的审批、配置和上传 API 可能暴露到局域网甚至公网。后来默认改成只绑定 loopback，并明确公网部署必须经过带认证和 TLS 的 gateway。GHCR workflow 也从“可以独立发布”修改成“只有默认分支 CI 成功后，发布经过测试的 SHA”。

这些问题让我认识到，Docker 能运行并不代表软件已经安全可分发。

## 如果重新做，以及对 Superpowers 的评价

如果重新做一次，我会更早冻结跨模块 API contract，把 Task 13 这种大任务提前拆小，并降低低风险文档任务的流程强度。我也会更早合并稳定的上游 PR，避免形成过长的 stacked PR 链。

我认为 Superpowers 隐含了几个假设：任务可以提前切得很清楚、fresh subagent 能靠 SPEC 独立工作、worktree 可以隔离开发环境、测试可以代表任务完成。这些假设在本项目中都只部分成立。worktree 能隔离 Git 文件，却不能隔离 venv、端口、Docker 和系统凭据；测试能证明确定性代码，却不能证明真实 CI 和公网部署。

因此我认为 Superpowers 最有价值的地方并不是固定流程本身，而是它强迫 AI 开发过程留下可验证的 RED/GREEN、review、Git 和外部证据。代价是更多流程成本。在 SafeCodeHarness v2 这种强调治理、安全和可审计性的项目中，这个代价总体是值得的。

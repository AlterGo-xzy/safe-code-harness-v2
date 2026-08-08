# 确定性机制演示与真实端到端验证设计

## 范围与目标

任务 13 为自实现 Harness 交付三份离线、稳定 JSON 的机制演示，并验证真实本地 FastAPI 与真实浏览器工作台的闭环。它证明的是可重复的机制行为，不是页面文案，也不调用真实 LLM、外部网络或真实凭据。

三份演示分别证明：

- 护栏对危险命令或路径确定性阻断，输出 `blocked: true`。
- Mock LLM 的第一次 `run_tests` 失败被反馈回灌，下一动作确定性变为 `write_file`。
- 审批状态依次走过 `waiting_approval`、`approved`、`executed`，且批准前不执行待处理写入。

## 集成基线

任务 13 从任务 12 工作台分支开始。由于任务 9 的 Planner 路由和任务 10 的工作区上传路由尚在独立已审查分支，任务 13 在任何真实浏览器验证前合并 `codex/t09-planner-credentials` 与 `codex/t10-workspace-upload` 的已验证代码。合并只解决必要冲突并保持已有测试与安全语义；不把它当作新增功能开发。这样运行中的真实本地 API 才能同时服务工作台读取、审批、Planner 和上传端点。

## 演示设计

- `scripts/run_guardrail_demo.py` 创建临时工作区并调用现有确定性 Rule/CommandGuard 边界；输出包含稳定场景名、`blocked` 布尔值和固定安全原因码。临时目录在 finally 清理，输出不包含绝对路径或敏感内容。
- `scripts/run_feedback_demo.py` 使用受控 MockLLM 序列和最小工具 stub。JSON transcript 至少含两项：第一次 `run_tests` 的 `ok: false`，随后 `write_file`；演示不修改真实项目文件。
- `scripts/run_approval_demo.py` 使用 RunService 或 AgentLoop 的内存审批状态机，先确认写动作停在 `waiting_approval`，随后批准并恢复，输出显式三阶段序列及执行布尔值。
- `backend/tests/integration/test_demos.py` 直接导入演示函数并断言结构，而非只匹配 stdout。
- `Makefile` 的 `demos` 目标顺序运行三份脚本；README 只记录确定性离线运行方式与结果含义。

## 真实 API 与浏览器 E2E

- Playwright 启动本地 FastAPI 和 Vite 前端。测试设置通过真实 `POST /api/runs` 创建 `pending_write`，这是初始化 API 数据，不是新 UI 功能。
- 测试先以 HTTP request 读取该运行，断言后端真实状态为 `waiting_approval` 和存在审批 ID；随后打开浏览器，验证页面显示同一运行的安全时间线与审批控件。
- 用户操作浏览器内的“批准”按钮；测试随后通过真实 API 读取状态，断言已不再待审批且审批后的执行结果可观察。页面选择/审批交互与 API 断言相互补充，不能以单一页面文字代替后端状态断言。
- E2E 还在 320px viewport 验证工作台为单列、主要控件可见且文本没有横向溢出，填补任务 11 明确留给任务 13 的证据。

## 边界与风险

- 不新增创建运行 UI、策略 API/UI、真实 Planner 调用、凭据或浏览器持久化；Planner 和上传在 E2E 仅验证真实路由可被本地应用加载，不录入密钥或上传真实用户项目。
- 不展示原始事件、工具输出、服务器路径或密钥；前端仍严格使用任务 11/12 的安全 DTO。
- 服务启动/停止、临时目录和 Playwright 端口必须由测试 fixture 控制并 finally 清理；所有等待以后端状态或明确 DOM 条件为准，禁止固定 sleep。
- Windows 环境如果 Playwright 浏览器未安装，安装是受控开发依赖操作；若仍无法满足真实浏览器前置条件，记录实际阻断而不伪造 E2E 通过。

## 验证与自查

- 每份演示和 E2E 均先有失败测试，再最小实现。
- 控制器运行 `make demos`、`pytest backend/tests/integration/test_demos.py`、前端完整测试/构建和真实 `npm.cmd run test:e2e`。
- 两阶段独立审查先检查 A 项机制证明与真实 API 边界，再检查清理、等待、端口、可访问性、320px 证据和凭据泄露。
- 任务 14 的 CI/容器、最终策略扩展和任务 15 部署/README 总交付仍不在本任务范围。

# 治理操作区设计

## 范围与目标

任务 12 在任务 11 的中文只读运行工作台中加入单页治理操作区。核心范围严格限于已有后端契约的三项操作：对 `waiting_approval` 运行作出批准或拒绝决定、读取/更新/清除可选 Planner 配置、上传安全 ZIP 并显示返回的工作区元数据。

策略读取与编辑是最后的扩展功能，不属于任务 12。本仓库当前没有策略 API；即使旧项目有相近实现，也不得制作假保存界面或提前迁入后端策略代码。

## 架构与数据边界

- `frontend/src/api/approvals.ts` 只调用 `POST /api/runs/{run_id}/approvals/{approval_id}/approve|reject`。只有详情状态为 `waiting_approval` 且存在 `approval_id` 时才显示可用决策；冲突和 404 映射为固定中文错误，不回显响应体。
- `frontend/src/api/planner.ts` 消费任务 9 的 `GET`、`PUT`、`DELETE /api/config/planner`。读取响应只包含 `configured`、`masked_suffix`、`base_url`、`model`；API key 只从密码输入框提交，随后立即清空，不进入 React state、日志、URL 或 localStorage。
- `frontend/src/api/workspaces.ts` 调用任务 10 的 `POST /api/workspaces/upload-zip`。只展示返回的 `id` 和 `file_count`；不显示服务器路径、不保存 workspace id 到 localStorage，也不假定上传会切换运行服务的当前工作区。
- `ApprovalPanel`、`PlannerSettings`、`WorkspaceUpload` 各自只接收类型化 DTO 与回调。`App` 负责刷新当前运行详情及三块面板的加载/错误状态。

任务 12 在 `codex/t12-settings-approval-ui` 工作树上以任务 11 前端为基础开发。任务 9、10 的后端分支尚未并入该基线，因此单元测试使用严格的 HTTP mock 验证契约；任务 13 负责在合并后的本地服务上进行真实浏览器端到端验证。

## 交互与安全

- 页面保持任务 11 的卡片总览与事件时间线；治理操作区位于详情下方。三个面板有明确中文标题、可读加载/成功/失败状态和键盘可操作控件。
- 审批提交时禁用两个决策按钮，成功后刷新详情；非待审批详情不渲染决策按钮。
- Planner 状态只显示“未配置”或掩码后缀；清除操作不要求或显示旧密钥。失败消息固定，不拼接服务端响应内容。
- 上传仅接受 `.zip`/`application/zip` 的文件选择；无文件、传输失败和成功元数据均有中文文本反馈。前端不负责解压、校验或放宽后端安全限制。
- 不新增创建运行、原始事件、工具输出、文件内容/路径展示、策略编辑、浏览器持久化或真实外部 Planner 调用。

## 旧项目复用边界

只在新仓库先写出同等行为的失败测试后，参考旧项目的以下源文件：

- `D:\2026_summer_project\frontend\src\components\ConfigPanel.tsx`：仅复用受控表单、复选状态联动和逐行文本解析思路；不复制其运行工作区/测试命令/策略写入范围。
- `D:\2026_summer_project\frontend\src\components\WorkspaceUploadPanel.tsx`：仅参考文件选择、上传状态和成功反馈结构；不得复制 `localStorage`、自定义事件或真实工作区路径显示。
- `D:\2026_summer_project\backend\src\safe_code_harness\api\routes_config.py`：仅记录其策略 API 可作为未来扩展依据；任务 12 不迁入该文件或其策略路由。

## 验证

- TDD：先为每个 API 客户端与三个面板建立失败测试，再最小实现、重构。
- 前端测试断言密钥不在已渲染 DOM、错误文本、状态或请求后 state 中；上传不写 localStorage；审批只在待审批状态可用。
- 运行 `npm.cmd ci --ignore-scripts`、`npm.cmd test`、`npm.cmd run build`。任务 13 再验证浏览器、真实 API 和 320px 响应式行为。
- 进行两阶段独立审查：规格/安全边界审查后再做代码质量/无障碍审查。提交前扫描凭据模式且不输出命中内容。

## 自查

- 无 TBD、假 API 或隐含持久化路径。
- 三个核心面板均绑定已存在的任务 8–10 路由；策略扩展被明确延后。
- 旧项目代码只作为经测试的局部参考，未整体复制，也不迁入其路径泄露或 localStorage 行为。

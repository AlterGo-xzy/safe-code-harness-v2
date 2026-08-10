# SafeCodeHarness v2

SafeCodeHarness v2 是一个自实现的 Coding Agent Harness。LLM 每次只提出一条受约束的 JSON 动作；本项目自己的 Python 代码负责动作解析、规则与路径治理、命令护栏、人工审批、工具分派、反馈回灌、有界记忆和停机，不调用高层 agent runner 代替主循环。

项目默认使用确定性的 Mock LLM，离线测试、三份机制演示和浏览器审批闭环都不需要真实 API key。可选的 OpenAI-compatible Planner 只负责单次补全，不拥有工具权限或 Harness 控制权。

## 获取源码与本地开发

源码仓库：<https://github.com/AlterGo-xzy/safe-code-harness-v2>。

本地开发要求：

- Python 3.12 或更高版本；
- Node.js 20；
- 前端依赖使用已提交的 `frontend/package-lock.json`；
- 只有运行容器或构建镜像时才需要 Docker Engine。

在类 Unix 系统中：

```sh
git clone https://github.com/AlterGo-xzy/safe-code-harness-v2.git
cd safe-code-harness-v2
python -m venv .venv
.venv/bin/python -m pip install -e "backend[dev]"
npm --prefix frontend ci --ignore-scripts
.venv/bin/python -m uvicorn safe_code_harness.api.main:app --app-dir backend/src --host 127.0.0.1 --port 8000
```

另开终端运行 `npm --prefix frontend run dev`，然后打开 Vite 显示的本地地址。

在 Windows PowerShell 中：

```powershell
git clone https://github.com/AlterGo-xzy/safe-code-harness-v2.git
Set-Location safe-code-harness-v2
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e "backend[dev]"
npm.cmd --prefix frontend ci --ignore-scripts
.\.venv\Scripts\python.exe -m uvicorn safe_code_harness.api.main:app --app-dir backend/src --host 127.0.0.1 --port 8000
```

另开 PowerShell 运行 `npm.cmd --prefix frontend run dev`。如果本机没有 `py -3.12`，可用任何满足 `>=3.12` 的 Python 可执行文件创建 `.venv`。

## 一键测试

类 Unix 系统在完成上述依赖安装后运行：

```sh
make test
```

它依次使用仓库自己的 `.venv/bin/python` 运行全部后端测试，并运行前端单元测试。Windows 没有 GNU Make 时，执行两个等价目标：

```powershell
New-Item -ItemType Directory -Force -Path .pytest-tmp | Out-Null
.\.venv\Scripts\python.exe -m pytest backend/tests --basetemp .pytest-tmp\local -q
npm.cmd --prefix frontend test
```

生产构建和真实 Chromium E2E：

```powershell
npm.cmd --prefix frontend run build
Push-Location frontend
npx.cmd playwright install chromium
npm.cmd run test:e2e
Pop-Location
```

E2E 启动真实 FastAPI 和 Vite，经过真实 HTTP API 创建确定性待审批运行，在浏览器中批准，再读取最终 API 状态；没有路由拦截。专用 E2E app 注入初始为空的进程内凭据存储，不读取 Windows Credential Manager，也不访问外部 Planner。

## 确定性机制演示

三份机制演示均离线运行并输出稳定 JSON：

```sh
make demos
```

Windows PowerShell 等价入口：

```powershell
.\scripts\run_demos.ps1
```

演示按顺序证明：

1. 真实命令护栏确定性拦截危险动作；
2. 注入失败测试结果后，反馈闭环让 Mock LLM 的下一步动作变为修复；
3. 治理重点维度的人工审批状态机在批准前不执行工具，批准后才恢复。

## OCI 容器分发

本地从源码构建和启动各只需一条命令：

```sh
docker build -t safe-code-harness-v2:local .
docker run --rm --name safe-code-harness -p 127.0.0.1:8000:8000 safe-code-harness-v2:local
```

打开 <http://localhost:8000>。镜像使用 Node/Python 多阶段构建，由同一个 FastAPI 进程提供 API 与编译后的 WebUI；等价 Compose 命令是 `docker compose up --build`。容器以非 root 用户运行，Compose 进一步使用只读根文件系统、临时工作区、丢弃 Linux capabilities 和 `no-new-privileges`。

已验证的公开 GHCR 获取方式如下：

```sh
docker pull ghcr.io/altergo-xzy/safe-code-harness-v2:latest
docker run --rm -p 127.0.0.1:8000:8000 ghcr.io/altergo-xzy/safe-code-harness-v2:latest
```

截至 2026-08-10，GitHub main 的发布 workflow 已成功；使用空 Docker 配置（未登录）实际拉取不可变的 `sha-c633003a06ad8073852f9125e3e195635f159bbb` 镜像，digest 为 `sha256:efebd5cc0277b73ddbfbecf00ad843af1c127b3ba31e0395f3de6b46825694d2`。临时 loopback 容器就绪后 `/` 与 `/api/runs` 均返回 HTTP 200。`latest` 由同一成功发布 workflow 推送；可复现部署优先使用 `sha-*` 标签。

## Planner key 安全配置

### 可选扩展：仅本机真实 Planner 模式

#### 作用与范围

SafeCodeHarness 默认使用确定性的 Mock LLM，因此离线测试、机制演示、浏览器审批闭环和 Railway 演示站都不需要真实 API key。

本扩展增加“本地真实 Planner”模式：用户在自己的 Windows 电脑上配置一个 OpenAI-compatible API 后，Planner 可以实际向该服务请求一次 JSON 动作建议，再交由 SafeCodeHarness 自己实现的 AgentLoop、治理规则、审批状态机和工具分派器执行。

该扩展具有以下边界：

- 仅位于独立分支 `codex/extension-local-real-planner`。
- 不属于当前 `main`、GitHub 发布镜像或 Railway Mock 演示站。
- 尚未合并、未部署；删除该分支即可完整回退，不影响已交付项目。
- Planner 只负责提出动作建议，不直接拥有写文件、运行测试或执行命令的权限。
- 默认仍为 Mock；真实模式必须由用户显式开启，且绝不会自动降级到 Mock。

#### 获取扩展分支

```powershell
git clone --branch codex/extension-local-real-planner --single-branch https://github.com/AlterGo-xzy/safe-code-harness-v2.git
Set-Location safe-code-harness-v2
```

如果已经克隆项目：

```powershell
git fetch origin
git switch codex/extension-local-real-planner
```

#### 本机启动

本扩展面向原生 Windows 本机使用。需要 Python 3.12+、Node.js/npm，以及一个浏览器。首次安装依赖：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .\backend
npm.cmd --prefix frontend ci --ignore-scripts
```

启动后端前，显式开启真实 Planner 功能：

```powershell
$env:SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER = "1"
.\.venv\Scripts\python.exe -m uvicorn safe_code_harness.api.main:app --app-dir backend/src --host 127.0.0.1 --port 8000
```

另开一个 PowerShell 窗口启动前端：

```powershell
Set-Location safe-code-harness-v2
npm.cmd --prefix frontend run dev
```

然后访问 Vite 输出的本地地址，通常为 <http://127.0.0.1:5173>。

#### 使用步骤

1. 在 WebUI 中上传一个不包含敏感信息的本地项目 ZIP。
2. 打开 Planner 设置，填写 OpenAI-compatible 服务的 Base URL、模型名和 API key。
3. 点击保存。Windows 原生运行时，key 由后端写入 Windows Credential Manager；界面和 GET API 只显示已配置状态及掩码，不会回显明文。
4. 在“创建运行”区域选择“本地真实 Planner”。
5. 输入任务描述并创建运行。
6. 当运行进入待审批状态时，检查事件时间线和建议动作。
7. 仅在确认安全后点击“批准”；写文件、运行测试和执行命令都需要单独审批。

真实模式要求同时满足以下条件：

- 环境变量 `SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER=1` 已设置；
- 已配置 Planner API key；
- 已上传并选择有效工作区；
- 创建运行时明确选择“本地真实 Planner”。

缺少任一条件时，服务会拒绝创建真实运行，而不会在用户不知情的情况下改用 Mock。

#### 安全边界

即使使用真实 Planner，以下安全控制仍由 SafeCodeHarness 本身执行：

- LLM 只能提出一条受 JSON 协议约束的动作建议。
- 文件操作受 PathSandbox 限制，只能作用于上传后的隔离工作区。
- `write_file`、`run_tests` 和 `run_command` 必须经过人工审批。
- 命令仍经过 RuntimePolicy 和 CommandGuard 检查。
- Planner key 不会返回给前端、写入日志、嵌入运行事件或发送到工具调用参数中。
- 没有 API key 时，不会发出外部 Planner 请求。

请勿在聊天、Issue、终端命令、`.env`、Compose 文件、Docker build 参数或仓库文件中粘贴真实 key。首次试用应使用无敏感文件、权限和额度都受限的专用测试 key；在批准任何动作前，应先检查任务描述、建议动作、目标文件路径和事件时间线。

#### Docker、Railway 与公网限制

本扩展故意不支持在当前 Docker/Railway 部署中启用真实 Planner。镜像内置 `SAFE_CODE_HARNESS_DEPLOYMENT=mock`，因此即使容器环境中错误设置了 `SAFE_CODE_HARNESS_ENABLE_REAL_PLANNER=1`，真实模式仍会被拒绝。Railway 地址仅用于无真实 key、无敏感工作区的 Mock 演示。

当前应用没有用户认证、租户隔离或生产级审计存储。因此不得把未认证的 Planner 配置、ZIP 上传、审批或真实 key 直接暴露到局域网或公网。若未来需要公网真实使用，必须先增加独立的认证与 TLS 网关、平台 Secret Manager 和多用户密钥隔离；在这些能力完成前，真实 Planner 模式仅应在受信任的本机环境使用。

#### 回退方式

该功能位于独立分支，不影响 `main`。如不再需要：

```powershell
git switch main
git branch -D codex/extension-local-real-planner
```

如已删除本地分支但保留远程分支，可按需再次检出；如确认不再保留，也可在 GitHub 删除对应远程分支。

默认 Mock LLM 完全不需要 key。仓库的 `.gitignore` 与 `.dockerignore` 排除根目录和嵌套的 dotenv 文件；它们是最后一道防误提交措施，不会把 `.env` 变成安全存储。

## CI/CD 与部署架构

`.github/workflows/ci.yml` 定义每次 push/PR 的后端、机制演示、前端单测、构建、真实 Chromium E2E 和 Docker build。只有默认分支 push 的同一 CI 成功后，`.github/workflows/publish-image.yml` 才 checkout 被测试的 SHA，并使用权限受限的 `GITHUB_TOKEN` 发布 `latest` 与 `sha-*` 到 GHCR。`.gitlab-ci.yml` 提供课程要求的顶层 `unit-test` job。

公开部署的安全架构必须是：

```text
浏览器 -> 认证与 TLS 网关 -> SafeCodeHarness 容器 -> 可选 Planner API
                              -> 进程内 key / 平台 Secret Manager
```

应用本身没有身份认证（the application does not implement authentication；public deployment requires an authentication and TLS gateway）。Docker/Compose 示例因此只绑定 `127.0.0.1`；不得把未加认证的审批、Planner 配置或 ZIP 上传 API 直接暴露到局域网或公网。Render、Railway、Fly.io 或等效平台只有在提供认证与 TLS 网关后才可使用。

截至 2026-08-10，用户已在 Railway 部署一个 HTTPS Mock 演示站：`https://safe-code-harness-v2-production.up.railway.app`；用户提供的浏览器截图显示首页返回“暂无运行记录”，协调会话对根地址的只读 HTTP 请求也得到 `200`。该站没有应用认证，且未配置真实 Planner key，因此它仅是无凭据、无敏感工作区的演示证据，不能替代下述认证/TLS 安全架构，也不能写成安全生产部署完成。GitHub main CI 与 GHCR 公开匿名拉取均已有外部成功证据；NJU Git 已同步 main，用户截图确认最终 main `a205a231` 的 GitLab pipeline `#319806` / `unit-test` job `#610513` 通过。

## 目录结构

- `backend/src/safe_code_harness/`：LLM/action 协议、治理、工具、反馈、记忆、主循环与 FastAPI。
- `backend/tests/`：离线单元测试、API/机制演示集成测试和发布契约测试。
- `frontend/src/`：React 中文运行工作台、安全 API 投影和审批/配置/上传界面。
- `frontend/e2e/`：真实 FastAPI/Vite/Chromium 审批闭环。
- `scripts/`：三份机制演示和 Windows 测试入口。
- `.github/workflows/`、`.gitlab-ci.yml`：CI 与镜像发布定义。
- `Dockerfile`、`docker-compose.yml`：OCI 构建与 loopback-only 本地运行。
- `SPEC.md`、`PLAN.md`、`SPEC_PROCESS.md`、`AGENT_LOG.md`、`REQUIREMENTS_TRACEABILITY.md`：规约、过程和验收证据。

## 安全边界

- LLM 只能建议动作；确定性代码决定解析、路径和命令许可、审批、执行与停机。
- ZIP 上传先完整校验归档元数据，再写入隔离工作区；错误响应不暴露服务器路径。
- 列表与时间线 API/前端只消费固定安全 DTO，不显示原始工具输出、事件文本或 key。
- 真实 Planner 是可选单次补全适配器，不替代 Harness loop，也不拥有工具调用权。
- 本项目没有用户认证、租户隔离、网络沙箱或生产级审计存储；公网部署必须增加外部认证/TLS 边界。

## 已知限制

- GHCR package 已发布且已由未登录 Docker 实际 pull/run；当前镜像不包含真实 Planner key。
- GitHub Actions 最终 main CI 已通过；NJU Git 已同步 main。最终 main `a205a231` 的 GitLab pipeline `#319806` / `unit-test` job `#610513` 已由用户截图确认通过。
- Railway HTTPS Mock 演示站已可访问，但没有认证网关；不得录入真实 Planner key、上传敏感工作区或把它写成安全生产部署。认证边界作为后续扩展。
- NJU Git 已配置并同步最终 main；GitLab main pipeline `#319806` 已通过。
- 镜像只验证了当前 Docker Engine 选择的架构；没有 multi-architecture manifest 或独立新机器验证。
- Windows Credential Manager 只适用于原生 Windows 后端；Linux 容器的进程内 key 重启即失。
- 前端 `npm ci` 的既有依赖树报告上游审计风险；没有执行破坏性 `--force` 升级，发布前需单独评估兼容升级。
- PR #1–#17 已普通 merge；GitHub/NJU main 为 `a205a231`，其 GitHub CI 和 GitLab `unit-test` 均有通过证据。
- `REFLECTION.md` 由学生本人提供，中文汉字计数为 1583；agent 未代写或润色。


## 许可证与第三方组件

本仓库自有源码采用 [MIT License](LICENSE)。直接依赖、开发工具和容器基础镜像的许可证说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；传递依赖的精确版本与元数据以 `frontend/package-lock.json` 和安装后的 Python distribution metadata 为准。

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

默认 Mock LLM 完全不需要 key。

Windows 原生运行时，可在 WebUI 的 Planner 设置中通过密码输入框录入、更新或清除可选 key；后端只把它写入 Windows Credential Manager，GET API 和界面只显示是否已配置及掩码，不回显明文。非 Windows 原生环境没有 Credential Manager 适配器时拒绝持久化，不降级到明文文件。

Linux 容器中的 Planner key 只保存在当前容器进程内存，推荐在仅本机访问的 WebUI 密码输入框中录入，容器重启后丢失。托管部署如需可重启配置，应通过托管平台的 Secret Manager 设置 `SAFE_CODE_HARNESS_PLANNER_API_KEY`；不要把真实值写入 `docker run` 命令、shell history、Compose YAML、Docker build argument、仓库文件或 `.env`。环境注入仍可能被宿主机或容器高权限主体读取，因此生产托管必须同时限制平台权限并启用 HTTPS。

仓库的 `.gitignore` 与 `.dockerignore` 排除根目录和嵌套的 dotenv 文件；它们是最后一道防误提交措施，不会把 `.env` 变成安全存储。

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

## 外部交付核验清单

以下项目只有取得真实外部结果后才能勾选：

- [x] 按依赖顺序审查并合并 PR #1–#17，最终默认分支包含完整项目；
- [x] GitHub Actions 最终 CI 成功：[run 31390746883](https://github.com/AlterGo-xzy/safe-code-harness-v2/actions/runs/31390746883)，commit `a205a231`；
- [x] NJU Git `main` 已与 GitHub main 同步；
- [x] GitLab `unit-test` 针对最终 NJU main 成功：pipeline `#319806` / job `#610513` / commit `a205a231`（用户截图）；
- [x] GHCR package 为 public，未登录环境 `docker pull`/run 成功；
- [x] Railway HTTPS Mock 演示站可访问（用户截图验证首页）；它未满足认证网关边界，真实 key/敏感工作区与生产使用仍为后续扩展；
- [x] 学生本人提供 `REFLECTION.md`，中文汉字计数为 1583；
- [x] 高置信历史扫描候选均为已分类的合成测试 fixture，未发现未分类真实 key。

## 许可证与第三方组件

本仓库自有源码采用 [MIT License](LICENSE)。直接依赖、开发工具和容器基础镜像的许可证说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；传递依赖的精确版本与元数据以 `frontend/package-lock.json` 和安装后的 Python distribution metadata 为准。

# 第三方组件与许可证声明

SafeCodeHarness v2 自有源码使用 MIT License。项目依赖以下第三方组件；各组件仍由其作者按各自许可证授权。本文件不是对第三方许可证文本的替代，发布者应随分发产物保留相应版权和许可证声明。

## Python 直接依赖

| 组件 | 用途 | 许可证 | 来源 |
| --- | --- | --- | --- |
| FastAPI | HTTP API | MIT | <https://github.com/fastapi/fastapi> |
| HTTPX | OpenAI-compatible HTTP transport 与 API 测试 | BSD-3-Clause | <https://github.com/encode/httpx> |
| python-multipart | ZIP multipart 上传 | Apache-2.0 | <https://github.com/Kludex/python-multipart> |
| Uvicorn | ASGI server | BSD-3-Clause | <https://github.com/encode/uvicorn> |
| pytest | 开发与测试 | MIT | <https://github.com/pytest-dev/pytest> |

许可证标识取自 2026-08-10 本地安装的 distribution metadata；实际解析版本由 `backend/pyproject.toml` 的范围和安装环境决定。

## Node.js 直接依赖

| 组件 | 许可证 |
| --- | --- |
| React、React DOM | MIT |
| Playwright Test | Apache-2.0 |
| Testing Library（jest-dom、react） | MIT |
| React TypeScript 类型声明 | MIT |
| Vite、Vite React plugin、Vitest | MIT |
| jsdom | MIT |
| TypeScript | Apache-2.0 |

上表标识来自已提交的 `frontend/package-lock.json`。该锁文件同时记录全部传递依赖的精确版本、来源、完整性摘要和许可证字段；发布前应以锁文件或生成的 SBOM 再次核验完整依赖树。

## 容器与 CI 工具

- `node:20-alpine` 与 `python:3.12-slim` 是 Docker Official Images；镜像内操作系统、Python、Node.js 与系统包分别遵循其上游许可证。
- GitHub Actions workflow 引用 `actions/*` 与 `docker/*` actions；这些远程 action 不作为源码复制进本仓库，使用时仍受各自仓库许可证和 GitHub 服务条款约束。
- Playwright 下载的 Chromium 及其组件遵循 Chromium 和各上游组件许可证，不提交到本仓库。

本仓库没有复制旧项目源码作为任务 15 的实现，也没有把 Open Design skill 或高层 agent framework 打包为运行时依赖。

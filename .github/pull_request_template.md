## 任务范围

- Task / 目标：
- 基线分支与目标分支：
- 实现 subagent 标识：
- 人工决策与人工修改：
- 旧仓库参考文件、参考范围与改写说明（未使用请写“未使用”）：

## TDD 证据

- RED 命令、预期失败与实际结果：
- GREEN 命令与实际结果：
- 完整回归命令与结果：

## 审查与安全

- Spec 合规审查（reviewer / Critical / Important / Minor）：
- 代码质量审查（reviewer / Critical / Important / Minor）：
- 已修复 findings 与复审结论：
- `git diff --check`：
- 凭据扫描命令与结果（不得粘贴任何真实 key）：
- 是否更改凭据、网络、审批、上传或公网暴露边界：

## 外部证据

- CI / registry / 部署 / NJU Git 的真实 URL、日期与 commit：
- 尚未执行或仍被外部条件阻断的项目：

## 检查清单

- [ ] PR 只包含当前 Task 的范围。
- [ ] 生产行为先有真实 RED，再有最小 GREEN。
- [ ] 没有提交 key、`.env`、虚拟环境、`node_modules`、构建输出或测试缓存。
- [ ] 没有把“已配置”或“已设计”写成“已外部验证”。
- [ ] Critical findings 已修复并复审；未修复项已明确列出。
- [ ] 进度、计划、追踪矩阵和 agent 日志已同步真实证据。

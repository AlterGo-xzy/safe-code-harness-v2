import { useState } from "react";

import { createRun, type RunDetail } from "../api/runs";

type Props = {
  workspaceId: string | null;
  onStarted: (run: RunDetail) => void;
};

export function RunLauncher({ workspaceId, onStarted }: Props) {
  const [mode, setMode] = useState<"mock" | "real">("mock");
  const [scenario, setScenario] = useState<"pending_write" | "secret_write">("pending_write");
  const [task, setTask] = useState("");
  const [pending, setPending] = useState(false);
  const [failed, setFailed] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setFailed(false);
    try {
      const run = mode === "mock"
        ? await createRun({ mode, scenario })
        : await createRun({ mode, task, workspaceId: workspaceId ?? "" });
      onStarted(run);
    } catch {
      setFailed(true);
    } finally {
      setPending(false);
    }
  }

  const realDisabled = !workspaceId || !task.trim();

  return (
    <section className="panel" aria-labelledby="run-launcher-heading">
      <h2 id="run-launcher-heading">创建运行</h2>
      <form className="settings-form" onSubmit={submit}>
        <label>
          运行模式
          <select value={mode} disabled={pending} onChange={(event) => setMode(event.currentTarget.value as "mock" | "real")}>
            <option value="mock">Mock 演示（默认）</option>
            <option value="real">本地真实 Planner</option>
          </select>
        </label>
        {mode === "mock" ? <label>
          演示场景
          <select value={scenario} disabled={pending} onChange={(event) => setScenario(event.currentTarget.value as "pending_write" | "secret_write")}>
            <option value="pending_write">安全写入，等待审批</option>
            <option value="secret_write">密钥写入，被规则阻止</option>
          </select>
        </label> : <>
          <label>
            工作任务
            <textarea value={task} disabled={pending} onChange={(event) => setTask(event.currentTarget.value)} />
          </label>
          <p>真实模式仅在本机显式启用、已配置 Planner key 且已上传工作区时可用；写入、测试和命令仍必须审批。</p>
        </>}
        <div className="panel-actions">
          <button type="submit" disabled={pending || (mode === "real" && realDisabled)}>创建运行</button>
        </div>
      </form>
      {mode === "real" && !workspaceId ? <p className="state-message state-message--error">请先上传本地项目 ZIP。</p> : null}
      {failed ? <p className="state-message state-message--error">无法创建运行：请检查本机真实 Planner 开关、配置和网络。</p> : null}
    </section>
  );
}

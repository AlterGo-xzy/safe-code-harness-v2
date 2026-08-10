import { useEffect, useRef, useState } from "react";

import { getRun, listRuns, type RunDetail, type RunSummary } from "./api/runs";
import { ApprovalPanel } from "./components/ApprovalPanel";
import { PlannerSettings } from "./components/PlannerSettings";
import { RunCardGrid } from "./components/RunCardGrid";
import { RunLauncher } from "./components/RunLauncher";
import { RunTimeline } from "./components/RunTimeline";
import { WorkspaceUpload } from "./components/WorkspaceUpload";

export function App() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [listState, setListState] = useState<"loading" | "ready" | "error">("loading");
  const [detail, setDetail] = useState<RunDetail | null>(null);
  const [detailError, setDetailError] = useState(false);
  const [workspaceId, setWorkspaceId] = useState<string | null>(null);
  const detailRequest = useRef(0);
  const currentRunId = useRef<string | null>(null);

  currentRunId.current = selectedRunId;

  function reloadRun(runId: string) {
    if (currentRunId.current !== runId) return;
    const request = ++detailRequest.current;
    setDetail(null);
    setDetailError(false);
    getRun(runId).then((loadedDetail) => {
      if (detailRequest.current === request) setDetail(loadedDetail);
    }).catch(() => {
      if (detailRequest.current === request) setDetailError(true);
    });
  }

  useEffect(() => {
    let active = true;
    listRuns().then((loadedRuns) => {
      if (!active) return;
      setRuns(loadedRuns);
      setSelectedRunId(loadedRuns[0]?.id ?? null);
      setListState("ready");
    }).catch(() => {
      if (active) setListState("error");
    });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!selectedRunId) return;
    reloadRun(selectedRunId);
  }, [selectedRunId]);

  function handleStarted(run: RunDetail) {
    setRuns((current) => [{ id: run.id, scenario: run.scenario, status: run.status, updatedAt: new Date().toISOString() }, ...current]);
    setSelectedRunId(run.id);
    setDetail(run);
    setDetailError(false);
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>受治理运行工作台</h1>
        <p>查看、创建并审批受治理运行。</p>
      </header>
      <div className="control-grid">
        <PlannerSettings />
        <WorkspaceUpload onUploaded={(workspace) => setWorkspaceId(workspace.id)} />
        <RunLauncher workspaceId={workspaceId} onStarted={handleStarted} />
      </div>
      {listState === "loading" ? <p className="state-message">正在加载运行…</p> : null}
      {listState === "error" ? <p className="state-message state-message--error">无法加载运行列表</p> : null}
      {listState === "ready" && runs.length === 0 ? <p className="state-message">暂无运行记录</p> : null}
      {runs.length > 0 ? <div className="workbench">
        <section className="panel" aria-labelledby="run-list-heading">
          <h2 id="run-list-heading">运行列表</h2>
          <RunCardGrid runs={runs} selectedRunId={selectedRunId} onSelect={setSelectedRunId} />
        </section>
        <section className="panel" aria-labelledby="timeline-heading">
          <h2 id="timeline-heading">事件时间线</h2>
          {detail?.id === selectedRunId && detail.status === "waiting_approval" && detail.approvalId ? (
            <ApprovalPanel runId={detail.id} approvalId={detail.approvalId} onResolved={() => reloadRun(detail.id)} />
          ) : null}
          {detailError ? <p className="state-message state-message--error">无法加载运行详情</p> : detail?.id === selectedRunId ? <RunTimeline events={detail.events} /> : <p className="state-message">正在加载运行详情…</p>}
        </section>
      </div> : null}
    </main>
  );
}

import { useEffect, useState } from "react";

import { getRun, listRuns, type RunDetail, type RunSummary } from "./api/runs";
import { RunCardGrid } from "./components/RunCardGrid";
import { RunTimeline } from "./components/RunTimeline";

export function App() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [listState, setListState] = useState<"loading" | "ready" | "error">("loading");
  const [detail, setDetail] = useState<RunDetail | null>(null);
  const [detailError, setDetailError] = useState(false);

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
    let active = true;

    setDetail(null);
    setDetailError(false);
    getRun(selectedRunId).then((loadedDetail) => {
      if (active) setDetail(loadedDetail);
    }).catch(() => {
      if (active) setDetailError(true);
    });

    return () => { active = false; };
  }, [selectedRunId]);

  if (listState === "loading") {
    return <main className="app-shell"><p className="state-message">正在加载运行…</p></main>;
  }

  if (listState === "error") {
    return <main className="app-shell"><p className="state-message state-message--error">无法加载运行列表</p></main>;
  }

  if (runs.length === 0) {
    return <main className="app-shell"><p className="state-message">暂无运行记录</p></main>;
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>受治理运行工作台</h1>
        <p>查看只读运行记录和治理事件。</p>
      </header>
      <div className="workbench">
        <section className="panel" aria-labelledby="run-list-heading">
          <h2 id="run-list-heading">运行列表</h2>
          <RunCardGrid runs={runs} selectedRunId={selectedRunId} onSelect={setSelectedRunId} />
        </section>
        <section className="panel" aria-labelledby="timeline-heading">
          <h2 id="timeline-heading">事件时间线</h2>
          {detailError ? <p className="state-message state-message--error">无法加载运行详情</p> : detail ? <RunTimeline events={detail.events} /> : <p className="state-message">正在加载运行详情…</p>}
        </section>
      </div>
    </main>
  );
}

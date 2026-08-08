import type { RunSummary } from "../api/runs";

type Props = {
  runs: RunSummary[];
  selectedRunId: string | null;
  onSelect: (runId: string) => void;
};

export function RunCardGrid({ runs, selectedRunId, onSelect }: Props) {
  return (
    <div className="run-card-grid" aria-label="运行列表">
      {runs.map((run) => (
        <button
          key={run.id}
          type="button"
          className="run-card"
          aria-label={`运行 ${run.scenario}，状态 ${run.status}，更新 ${formatTimestamp(run.updatedAt)}`}
          aria-pressed={run.id === selectedRunId}
          onClick={() => onSelect(run.id)}
        >
          <span className="run-card__label">运行</span>
          <strong>{run.scenario}</strong>
          <span>状态：{run.status}</span>
          <span>更新：{formatTimestamp(run.updatedAt)}</span>
        </button>
      ))}
    </div>
  );
}

function formatTimestamp(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, "0")}-${String(date.getUTCDate()).padStart(2, "0")} ${String(date.getUTCHours()).padStart(2, "0")}:${String(date.getUTCMinutes()).padStart(2, "0")} UTC`;
}

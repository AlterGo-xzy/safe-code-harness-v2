import type { RunEvent } from "../api/runs";

type Props = {
  events: RunEvent[];
};

export function RunTimeline({ events }: Props) {
  if (events.length === 0) {
    return <p className="timeline-empty">暂无事件</p>;
  }

  return (
    <ul className="run-timeline" aria-label="运行事件时间线">
      {events.map((event, index) => (
        <li key={`${event.createdAt}-${event.type}-${index}`} className={`run-event run-event--${event.level}`}>
          <div className="run-event__meta">
            <span aria-label="事件类型">{event.type}</span>
            <time dateTime={event.createdAt}>{formatTimestamp(event.createdAt)}</time>
          </div>
          <p className="run-event__summary" aria-label="事件摘要">{event.summaryCode}</p>
          <p>状态：<strong>{event.displayStatus}</strong></p>
        </li>
      ))}
    </ul>
  );
}

function formatTimestamp(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, "0")}-${String(date.getUTCDate()).padStart(2, "0")} ${String(date.getUTCHours()).padStart(2, "0")}:${String(date.getUTCMinutes()).padStart(2, "0")} UTC`;
}

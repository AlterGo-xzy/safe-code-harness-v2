export type RunSummary = {
  id: string;
  scenario: string;
  status: string;
  updatedAt: string;
};

export type RunEvent = {
  kind: string;
  step: number;
  summary: string;
  actionType: string | null;
  ok: boolean | null;
  failure: string | null;
};

export type RunDetail = {
  id: string;
  scenario: string;
  status: string;
  events: RunEvent[];
};

type JsonRecord = Record<string, unknown>;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function readString(value: JsonRecord, key: string, message: string): string {
  if (typeof value[key] !== "string") {
    throw new Error(message);
  }
  return value[key];
}

function readNullableString(value: JsonRecord, key: string, message: string): string | null {
  const field = value[key];
  if (field !== null && typeof field !== "string") {
    throw new Error(message);
  }
  return field;
}

function readNullableBoolean(value: JsonRecord, key: string, message: string): boolean | null {
  const field = value[key];
  if (field !== null && typeof field !== "boolean") {
    throw new Error(message);
  }
  return field;
}

function toSummary(value: unknown): RunSummary {
  const message = "无法加载运行列表";
  if (!isRecord(value)) {
    throw new Error(message);
  }
  return {
    id: readString(value, "id", message),
    scenario: readString(value, "scenario", message),
    status: readString(value, "status", message),
    updatedAt: readString(value, "updated_at", message),
  };
}

function toEvent(value: unknown): RunEvent {
  const message = "无法加载运行详情";
  if (!isRecord(value) || typeof value.step !== "number") {
    throw new Error(message);
  }
  return {
    kind: readString(value, "kind", message),
    step: value.step,
    summary: readString(value, "summary", message),
    actionType: readNullableString(value, "action_type", message),
    ok: readNullableBoolean(value, "ok", message),
    failure: readNullableString(value, "failure", message),
  };
}

function toDetail(value: unknown): RunDetail {
  const message = "无法加载运行详情";
  if (!isRecord(value) || !Array.isArray(value.events)) {
    throw new Error(message);
  }
  return {
    id: readString(value, "id", message),
    scenario: readString(value, "scenario", message),
    status: readString(value, "status", message),
    events: value.events.map(toEvent),
  };
}

export async function listRuns(signal?: AbortSignal): Promise<RunSummary[]> {
  const response = await fetch("/api/runs", { signal });
  if (!response.ok) {
    throw new Error("无法加载运行列表");
  }
  const payload: unknown = await response.json();
  if (!Array.isArray(payload)) {
    throw new Error("无法加载运行列表");
  }
  return payload.map(toSummary);
}

export async function getRun(runId: string, signal?: AbortSignal): Promise<RunDetail> {
  const response = await fetch(`/api/runs/${encodeURIComponent(runId)}`, { signal });
  if (!response.ok) {
    throw new Error("无法加载运行详情");
  }
  return toDetail(await response.json());
}

export type RunSummary = {
  id: string;
  scenario: string;
  status: string;
  updatedAt: string;
};

export type RunEvent = {
  type: string;
  createdAt: string;
  level: string;
  displayStatus: string;
  summaryCode: string;
};

export type RunDetail = {
  id: string;
  scenario: string;
  status: string;
  events: RunEvent[];
  approvalId: string | null;
};

export type CreateRunInput =
  | { mode: "mock"; scenario: "pending_write" | "secret_write" }
  | { mode: "real"; task: string; workspaceId: string };

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
  if (!isRecord(value)) {
    throw new Error(message);
  }
  return {
    type: readString(value, "type", message),
    createdAt: readString(value, "created_at", message),
    level: readString(value, "level", message),
    displayStatus: readString(value, "display_status", message),
    summaryCode: readString(value, "summary_code", message),
  };
}

function toDetail(value: unknown): RunDetail {
  const message = "无法加载运行详情";
  if (!isRecord(value) || !Array.isArray(value.events)) {
    throw new Error(message);
  }
  const status = readString(value, "status", message);
  return {
    id: readString(value, "id", message),
    scenario: readString(value, "scenario", message),
    status,
    events: value.events.map(toEvent),
    approvalId: status === "waiting_approval" && typeof value.approval_id === "string"
      ? value.approval_id
      : null,
  };
}

export async function listRuns(signal?: AbortSignal): Promise<RunSummary[]> {
  try {
    const response = await fetch("/api/runs", { signal });
    if (!response.ok) {
      throw new Error();
    }
    const payload: unknown = await response.json();
    if (!Array.isArray(payload)) {
      throw new Error();
    }
    return payload.map(toSummary);
  } catch {
    throw new Error("无法加载运行列表");
  }
}

export async function getRun(runId: string, signal?: AbortSignal): Promise<RunDetail> {
  try {
    const response = await fetch(`/api/runs/${encodeURIComponent(runId)}`, { signal });
    if (!response.ok) {
      throw new Error();
    }
    return toDetail(await response.json());
  } catch {
    throw new Error("无法加载运行详情");
  }
}

export async function createRun(input: CreateRunInput): Promise<RunDetail> {
  const message = "无法创建运行";
  const payload = input.mode === "mock"
    ? { mode: "mock", scenario: input.scenario }
    : { mode: "real", task: input.task, workspace_id: input.workspaceId };
  try {
    const response = await fetch("/api/runs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error();
    return toDetail(await response.json());
  } catch {
    throw new Error(message);
  }
}

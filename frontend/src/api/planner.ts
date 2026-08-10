export type PlannerInput = {
  baseUrl: string;
  model: string;
  apiKey: string;
};

export type PlannerSettings = {
  configured: boolean;
  maskedSuffix: string | null;
  baseUrl: string;
  model: string;
};

type JsonRecord = Record<string, unknown>;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function toPlanner(value: unknown, message: string): PlannerSettings {
  if (
    !isRecord(value)
    || typeof value.configured !== "boolean"
    || (typeof value.masked_suffix !== "string" && value.masked_suffix !== null)
    || typeof value.base_url !== "string"
    || typeof value.model !== "string"
  ) {
    throw new Error(message);
  }
  return {
    configured: value.configured,
    maskedSuffix: value.masked_suffix,
    baseUrl: value.base_url,
    model: value.model,
  };
}

async function readPlanner(response: Response, message: string): Promise<PlannerSettings> {
  if (!response.ok) {
    throw new Error(message);
  }
  return toPlanner(await response.json(), message);
}

export async function getPlanner(): Promise<PlannerSettings> {
  const message = "无法加载 Planner 配置";
  try {
    return await readPlanner(await fetch("/api/config/planner"), message);
  } catch {
    throw new Error(message);
  }
}

export async function savePlanner(input: PlannerInput): Promise<PlannerSettings> {
  const message = "无法保存 Planner 配置";
  try {
    return await readPlanner(await fetch("/api/config/planner", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ base_url: input.baseUrl, model: input.model, api_key: input.apiKey }),
    }), message);
  } catch {
    throw new Error(message);
  }
}

export async function clearPlanner(): Promise<PlannerSettings> {
  const message = "无法清除 Planner 配置";
  try {
    return await readPlanner(await fetch("/api/config/planner", { method: "DELETE" }), message);
  } catch {
    throw new Error(message);
  }
}

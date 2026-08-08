export type WorkspaceUploadResult = {
  id: string;
  fileCount: number;
};

type JsonRecord = Record<string, unknown>;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function toWorkspace(value: unknown): WorkspaceUploadResult {
  if (!isRecord(value) || typeof value.id !== "string" || typeof value.file_count !== "number") {
    throw new Error("无法上传工作区");
  }
  return { id: value.id, fileCount: value.file_count };
}

export async function uploadWorkspace(file: File): Promise<WorkspaceUploadResult> {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("/api/workspaces/upload-zip", { method: "POST", body: formData });
    if (!response.ok) {
      throw new Error();
    }
    return toWorkspace(await response.json());
  } catch {
    throw new Error("无法上传工作区");
  }
}

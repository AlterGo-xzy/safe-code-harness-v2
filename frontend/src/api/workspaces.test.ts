import { afterEach, expect, it, vi } from "vitest";

import { uploadWorkspace } from "./workspaces";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("projects upload output to ID and file count only", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "ws-1", file_count: 3, path: "/private/workspace" }), { status: 201 })));
  await expect(uploadWorkspace(new File(["zip"], "project.zip", { type: "application/zip" }))).resolves.toEqual({ id: "ws-1", fileCount: 3 });
});

it("submits the selected ZIP as multipart form data", async () => {
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ id: "ws-1", file_count: 3 }), { status: 201 }));
  vi.stubGlobal("fetch", fetchMock);
  const file = new File(["zip"], "project.zip", { type: "application/zip" });

  await uploadWorkspace(file);

  const [url, options] = fetchMock.mock.calls[0] as [string, RequestInit];
  expect(url).toBe("/api/workspaces/upload-zip");
  expect(options.method).toBe("POST");
  expect(options.body).toBeInstanceOf(FormData);
  expect((options.body as FormData).get("file")).toBe(file);
});

it("rejects an upload error without exposing its response body", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("/private/workspace", { status: 500 })));

  await expect(uploadWorkspace(new File(["zip"], "project.zip", { type: "application/zip" }))).rejects.toThrow(/^无法上传工作区$/);
});

import { useState } from "react";

import { uploadWorkspace, type WorkspaceUploadResult } from "../api/workspaces";

export function WorkspaceUpload({ onUploaded }: { onUploaded?: (workspace: WorkspaceUploadResult) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<WorkspaceUploadResult | null>(null);
  const [pending, setPending] = useState(false);
  const [hasError, setHasError] = useState(false);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) return;

    setPending(true);
    setHasError(false);
    try {
      const uploaded = await uploadWorkspace(file);
      setResult(uploaded);
      onUploaded?.(uploaded);
    } catch {
      setHasError(true);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="panel" aria-labelledby="workspace-upload-heading">
      <h2 id="workspace-upload-heading">上传工作区</h2>
      <form className="settings-form" onSubmit={submit}>
        <label>
          项目 ZIP
          <input
            type="file"
            accept=".zip,application/zip"
            disabled={pending}
            onChange={(event) => setFile(event.currentTarget.files?.[0] ?? null)}
          />
        </label>
        <div className="panel-actions">
          <button type="submit" disabled={!file || pending}>上传工作区</button>
        </div>
      </form>
      {hasError ? <p className="state-message state-message--error">无法上传工作区</p> : null}
      {result ? <p>工作区 {result.id}：{result.fileCount} 个文件</p> : null}
    </section>
  );
}

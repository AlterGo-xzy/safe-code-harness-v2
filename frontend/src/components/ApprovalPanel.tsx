import { useState } from "react";

import { decideApproval } from "../api/approvals";

type ApprovalPanelProps = {
  runId: string;
  approvalId: string;
  onResolved: () => void;
};

export function ApprovalPanel({ runId, approvalId, onResolved }: ApprovalPanelProps) {
  const [pending, setPending] = useState(false);
  const [hasError, setHasError] = useState(false);

  if (!runId || !approvalId) return null;

  async function submit(decision: "approve" | "reject") {
    setPending(true);
    setHasError(false);
    try {
      await decideApproval(runId, approvalId, decision);
      onResolved();
    } catch {
      setHasError(true);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="approval-panel" aria-labelledby="approval-heading">
      <h3 id="approval-heading">审批决定</h3>
      <p>此运行正在等待审批。</p>
      {hasError ? <p className="state-message state-message--error">无法提交审批决定</p> : null}
      <div className="panel-actions">
        <button type="button" disabled={pending} onClick={() => submit("approve")}>批准</button>
        <button type="button" disabled={pending} onClick={() => submit("reject")}>拒绝</button>
      </div>
    </section>
  );
}

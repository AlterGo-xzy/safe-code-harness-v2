export async function decideApproval(
  runId: string,
  approvalId: string,
  decision: "approve" | "reject",
): Promise<void> {
  try {
    const response = await fetch(
      `/api/runs/${encodeURIComponent(runId)}/approvals/${encodeURIComponent(approvalId)}/${decision}`,
      { method: "POST" },
    );
    if (!response.ok) {
      throw new Error();
    }
  } catch {
    throw new Error("无法提交审批决定");
  }
}

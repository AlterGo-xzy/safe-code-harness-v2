import { expect, test, type APIRequestContext, type Locator, type Page } from "@playwright/test";

const apiBase = "http://127.0.0.1:8000";

type RunSnapshot = {
  id: string;
  status: string;
  approval_id: string | null;
  events: Array<{ summary_code: string }>;
};

async function createPendingRun(request: APIRequestContext): Promise<RunSnapshot> {
  const created = await request.post(`${apiBase}/api/runs`, {
    data: { scenario: "pending_write" },
  });
  expect(created.status()).toBe(201);

  const createdBody = await created.json() as RunSnapshot;
  const response = await request.get(`${apiBase}/api/runs/${createdBody.id}`);
  expect(response.status()).toBe(200);
  return await response.json() as RunSnapshot;
}

async function expectFullyInsideViewport(page: Page, locator: Locator): Promise<void> {
  const box = await locator.boundingBox();
  const viewport = page.viewportSize();

  expect(box).not.toBeNull();
  expect(viewport).not.toBeNull();
  expect(box!.x).toBeGreaterThanOrEqual(0);
  expect(box!.y).toBeGreaterThanOrEqual(0);
  expect(box!.x + box!.width).toBeLessThanOrEqual(viewport!.width);
  expect(box!.y + box!.height).toBeLessThanOrEqual(viewport!.height);
}

test("real API run is approved through the browser and completes", async ({ page, request }) => {
  const pending = await createPendingRun(request);
  expect(pending.status).toBe("waiting_approval");
  expect(typeof pending.approval_id).toBe("string");

  await page.goto("/");
  await expect(page.getByText("approval_pending")).toBeVisible();
  await page.getByRole("button", { name: "批准" }).click();

  await expect.poll(async () => {
    const response = await request.get(`${apiBase}/api/runs/${pending.id}`);
    return (await response.json() as RunSnapshot).status;
  }).toBe("completed");

  const completedResponse = await request.get(`${apiBase}/api/runs/${pending.id}`);
  expect(completedResponse.status()).toBe(200);
  const completed = await completedResponse.json() as RunSnapshot;
  expect(completed.events.map((event) => event.summary_code)).toEqual(expect.arrayContaining([
    "approval_approved",
    "tool_succeeded",
    "run_finished",
  ]));
});

test("workbench remains usable at 320px", async ({ page, request }) => {
  const pending = await createPendingRun(request);
  expect(pending.status).toBe("waiting_approval");
  expect(typeof pending.approval_id).toBe("string");

  await page.setViewportSize({ width: 320, height: 720 });
  await page.goto("/");
  await page.getByRole("button", { name: /运行 pending_write，状态 waiting_approval/ }).last().click();

  const approveButton = page.getByRole("button", { name: "批准" });
  await expect(approveButton).toBeVisible();
  await expectFullyInsideViewport(page, approveButton);
  expect(await page.evaluate(() => (
    document.documentElement.scrollWidth <= window.innerWidth
    && document.body.scrollWidth <= window.innerWidth
  ))).toBeTruthy();
});

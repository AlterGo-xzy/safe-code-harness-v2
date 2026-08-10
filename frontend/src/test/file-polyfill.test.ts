import { expect, it } from "vitest";

import { installFilePolyfill } from "./file-polyfill";

it("installs File in a File-free Node-like global target", () => {
  const target: { File?: typeof File } = {};

  installFilePolyfill(target);

  expect(target.File).toBeTypeOf("function");
  expect(new target.File!(["zip"], "project.zip").name).toBe("project.zip");
});

import { File as NodeFile } from "node:buffer";

type FileTarget = {
  File?: typeof File;
};

export function installFilePolyfill(target: FileTarget): void {
  target.File ??= NodeFile as unknown as typeof File;
}

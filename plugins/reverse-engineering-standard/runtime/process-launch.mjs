import { existsSync } from "node:fs";
import { dirname, resolve, delimiter } from "node:path";

// Invoke trusted JavaScript entrypoints directly, never .cmd wrappers or a shell.
export function packageManagerInvocation(env = process.env) {
  const explicit = env.DEV_WORKFLOW_PACKAGE_MANAGER_JS;
  if (explicit) {
    if (!existsSync(explicit) || !/\.(?:c?js|mjs)$/i.test(explicit)) throw new Error("DEV_WORKFLOW_PACKAGE_MANAGER_JS must name an existing JavaScript package-manager entrypoint");
    return { executable: process.execPath, args: [resolve(explicit)], kind: /pnpm/i.test(explicit) ? "pnpm" : "npm" };
  }
  const roots = [dirname(process.execPath), ...(env.PATH ?? "").split(delimiter)];
  for (const root of roots) {
    for (const relative of ["node_modules/npm/bin/npm-cli.js", "../lib/node_modules/npm/bin/npm-cli.js"]) {
      const entry = resolve(root, relative);
      if (existsSync(entry)) return { executable: process.execPath, args: [entry], kind: "npm" };
    }
  }
  if (process.platform !== "win32") return { executable: "npm", args: [], kind: "npm" };
  throw new Error("npm JavaScript entrypoint not found; install supported Node/npm or set DEV_WORKFLOW_PACKAGE_MANAGER_JS to your trusted npm-cli.js or pnpm.cjs");
}

export function reaInvocation(here) {
  return { executable: process.execPath, args: [resolve(here, "node_modules/rea-agents/scripts/rea.mjs")] };
}

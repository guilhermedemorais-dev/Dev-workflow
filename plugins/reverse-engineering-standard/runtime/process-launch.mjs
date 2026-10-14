import { existsSync, realpathSync } from "node:fs";
import { dirname, resolve, delimiter } from "node:path";

// Invoke trusted JavaScript entrypoints directly, never .cmd wrappers or a shell.
export function packageManagerInvocation(env = process.env, requiredKind = null) {
  const explicit = env.DEV_WORKFLOW_PACKAGE_MANAGER_JS;
  if (explicit) {
    if (!existsSync(explicit) || !/\.(?:c?js|mjs)$/i.test(explicit)) throw new Error("DEV_WORKFLOW_PACKAGE_MANAGER_JS must name an existing JavaScript package-manager entrypoint");
    const kind = /pnpm/i.test(explicit) ? "pnpm" : "npm";
    if (requiredKind && kind !== requiredKind) throw new Error(`Committed lockfile requires ${requiredKind}; DEV_WORKFLOW_PACKAGE_MANAGER_JS selects ${kind}`);
    return { executable: process.execPath, args: [resolve(explicit)], kind };
  }
  const kind = requiredKind ?? "npm";
  const roots = [dirname(process.execPath), ...(env.PATH ?? "").split(delimiter)];
  for (const root of roots) {
    const candidates = kind === "pnpm"
      ? ["node_modules/pnpm/bin/pnpm.cjs", "../lib/node_modules/pnpm/bin/pnpm.cjs", "pnpm.cjs", "pnpm"]
      : ["node_modules/npm/bin/npm-cli.js", "../lib/node_modules/npm/bin/npm-cli.js"];
    for (const relative of candidates) {
      const entry = resolve(root, relative);
      if (existsSync(entry)) {
        const realEntry = realpathSync(entry);
        if (/\.(?:c?js|mjs)$/i.test(realEntry)) return { executable: process.execPath, args: [realEntry], kind };
      }
    }
  }
  if (process.platform !== "win32") return { executable: kind, args: [], kind };
  throw new Error(`${kind} JavaScript entrypoint not found; install the required manager or set DEV_WORKFLOW_PACKAGE_MANAGER_JS to your trusted ${kind === "pnpm" ? "pnpm.cjs" : "npm-cli.js"}`);
}

export function reaInvocation(here) {
  return { executable: process.execPath, args: [resolve(here, "node_modules/rea-agents/scripts/rea.mjs")] };
}

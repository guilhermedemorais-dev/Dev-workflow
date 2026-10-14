#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { readFileSync, existsSync, statSync } from "node:fs";
import { dirname, resolve, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";

import { reaInvocation } from "./process-launch.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const catalog = JSON.parse(readFileSync(resolve(here, "rea-capability-catalog.json"), "utf8"));
const action = process.argv[2] ?? "probe";

// Local provider paths only; this configuration is not a second health cache.
function providerEnvironment() {
  const configPath = resolve(here, "runtime-state/providers.json");
  if (!existsSync(configPath)) return process.env;
  const config = JSON.parse(readFileSync(configPath, "utf8"));
  const allowed = ["GHIDRA_INSTALL_DIR", "JAVA_HOME"];
  if (config.schema_version !== 1 || !config.paths || Object.keys(config).some(key => !["schema_version", "paths"].includes(key))) throw new Error("Invalid local provider configuration schema");
  for (const [key, value] of Object.entries(config.paths)) {
    if (!allowed.includes(key) || typeof value !== "string" || !isAbsolute(value) || !existsSync(value) || !statSync(value).isDirectory()) throw new Error("Invalid local provider path: " + key);
  }
  return {...config.paths, ...process.env};
}

function run(args) {
  // REA's native Win32 boundary requires normalized drive paths, not slash paths.
  const normalized = args.map(value => process.platform === "win32" && isAbsolute(value) && existsSync(value) ? resolve(value) : value);
  const result = spawnSync(reaInvocation(here).executable, [...reaInvocation(here).args, ...normalized], {shell: false, env: providerEnvironment(), encoding:"utf8", stdio:["ignore","pipe","pipe"]});
  return {
    ok: result.status === 0,
    exit_code: result.status,
    stdout: result.stdout ?? "",
    stderr: result.error ? result.error.message : (result.stderr ?? "")
  };
}

if (action === "catalog") {
  process.stdout.write(JSON.stringify(catalog, null, 2) + "\n");
  process.exit(0);
}

if (action === "probe") {
  const result = run(["doctor","--json"]);
  let diagnostics = null;
  let diagnosticError = null;
  if (result.stdout) {
    try { diagnostics = JSON.parse(result.stdout); }
    catch { diagnosticError = "REA doctor returned invalid JSON"; }
  }
  process.stdout.write(JSON.stringify({
    runtime: "rea-agents",
    pinned_version: catalog.upstream.version,
    runtime_available: diagnostics !== null && !diagnosticError,
    healthy: result.ok && !diagnosticError,
    diagnostics,
    stderr: diagnosticError || result.stderr || null
  }, null, 2) + "\n");
  process.exit(result.ok && !diagnosticError ? 0 : 1);
}

if (action === "analyze-javascript") {
  const target = process.argv[3];
  if (!target) throw new Error("target path required");
  const result = run(["analyze-javascript-application", target, "--json"]);
  process.stdout.write(result.stdout || JSON.stringify(result));
  process.exit(result.ok ? 0 : 1);
}

if (action === "cli") {
  const args = process.argv.slice(3);
  if (!args.length) throw new Error("REA CLI arguments required");
  const result = run(args);
  process.stdout.write(result.stdout);
  process.stderr.write(result.stderr);
  process.exit(result.ok ? 0 : (result.exit_code ?? 1));
}

throw new Error("unknown action");

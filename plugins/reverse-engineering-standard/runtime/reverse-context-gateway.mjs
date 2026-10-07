#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const catalog = JSON.parse(readFileSync(resolve(here, "rea-capability-catalog.json"), "utf8"));
const action = process.argv[2] ?? "probe";

function reaBin() {
  const local = resolve(here, "node_modules", ".bin", process.platform === "win32" ? "rea.cmd" : "rea");
  return local;
}

function run(args) {
  const result = spawnSync(reaBin(), args, {encoding:"utf8", stdio:["ignore","pipe","pipe"]});
  return {
    ok: result.status === 0,
    exit_code: result.status,
    stdout: result.stdout ?? "",
    stderr: result.stderr ?? ""
  };
}

if (action === "catalog") {
  process.stdout.write(JSON.stringify(catalog, null, 2) + "\n");
  process.exit(0);
}

if (action === "probe") {
  const result = run(["doctor","--json"]);
  process.stdout.write(JSON.stringify({
    runtime: "rea-agents",
    pinned_version: catalog.upstream.version,
    healthy: result.ok,
    diagnostics: result.stdout ? JSON.parse(result.stdout) : null,
    stderr: result.stderr || null
  }, null, 2) + "\n");
  process.exit(result.ok ? 0 : 1);
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

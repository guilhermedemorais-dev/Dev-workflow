#!/usr/bin/env node
import { createHash } from "node:crypto";
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

import { packageManagerInvocation, reaInvocation } from "./process-launch.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const vendorDir = resolve(here, "../vendor/rea-runtime");
const tarball = resolve(vendorDir, "rea-agents-4.1.0.tgz");
const checksumFile = tarball + ".sha256";

function fail(message) {
  process.stderr.write(message + "\n");
  process.exit(1);
}

if (!existsSync(tarball)) fail("vendored REA runtime tarball is missing");
if (!existsSync(checksumFile)) fail("vendored REA runtime checksum is missing");

const expected = readFileSync(checksumFile, "utf8").trim().split(/\s+/)[0];
const actual = createHash("sha256").update(readFileSync(tarball)).digest("hex");
if (actual !== expected) fail("vendored REA runtime checksum mismatch");

let manager;
try { manager = packageManagerInvocation(); } catch (error) { fail(error.message); }
const installArgs = manager.kind === "pnpm"
  ? ["install", "--ignore-scripts", existsSync(resolve(here, "pnpm-lock.yaml")) ? "--frozen-lockfile" : "--no-frozen-lockfile"]
  : ["install", "--ignore-scripts", "--no-audit", "--no-fund"];
const result = spawnSync(manager.executable, [...manager.args, ...installArgs], { cwd: here, stdio: "inherit", shell: false });

if (result.error) fail("package manager bootstrap failed to start: " + result.error.message);
if (result.status !== 0) process.exit(result.status ?? 1);

const reaBin = reaInvocation(here).args[0];
if (!existsSync(reaBin)) fail("vendored REA runtime did not expose the rea CLI");

process.stdout.write(JSON.stringify({
  runtime: "rea-agents",
  source: "vendored-tarball",
  version: "4.1.0",
  sha256: actual,
  executable: reaBin
}, null, 2) + "\n");

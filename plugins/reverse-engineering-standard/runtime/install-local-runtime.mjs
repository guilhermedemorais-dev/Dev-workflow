#!/usr/bin/env node
import { createHash } from "node:crypto";
import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

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

const result = spawnSync(
  process.platform === "win32" ? "npm.cmd" : "npm",
  ["install", "--ignore-scripts", "--no-audit", "--no-fund"],
  { cwd: here, stdio: "inherit" }
);

if (result.error) fail("npm bootstrap failed to start");
if (result.status !== 0) process.exit(result.status ?? 1);

const reaBin = resolve(here, "node_modules", ".bin", process.platform === "win32" ? "rea.cmd" : "rea");
if (!existsSync(reaBin)) fail("vendored REA runtime did not expose the rea CLI");

process.stdout.write(JSON.stringify({
  runtime: "rea-agents",
  source: "vendored-tarball",
  version: "4.1.0",
  sha256: actual,
  executable: reaBin
}, null, 2) + "\n");

#!/usr/bin/env python3
"""Local, per-skill tool availability cache. Never installs tools implicitly."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
OWNERS = {"security-standard", "ui-ux-standard", "dev-implementation-standard"}


def paths(owner):
    if owner not in OWNERS:
        raise ValueError("unknown owner")
    registry_override = os.environ.get("TOOL_REGISTRY_PATH")
    state_override = os.environ.get("TOOL_STATE_PATH")
    if bool(registry_override) != bool(state_override):
        raise ValueError("TOOL_REGISTRY_PATH and TOOL_STATE_PATH must be set together")
    if registry_override and state_override:
        return Path(registry_override), Path(state_override)
    skill = ROOT / "plugins" / owner / "skills" / owner
    return skill / "references" / "tool-registry.json", skill / "runtime-state" / "tool-state.json"


def fingerprint(workspace):
    """A small runtime boundary; explicit override supports container/CI identities."""
    return "|".join((platform.node(), sys.platform, sys.prefix,
                     str(Path(workspace).resolve()), os.environ.get("VIRTUAL_ENV", ""),
                     os.environ.get("TOOL_RUNTIME_ID", "host")))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def registry_tool(owner, tool_id):
    registry, _ = paths(owner)
    data = json.loads(registry.read_text(encoding="utf-8"))
    return next(tool for tool in data["tools"] if tool["id"] == tool_id)


def read_state(owner, workspace):
    _, state_path = paths(owner)
    env = fingerprint(workspace)
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    if data.get("environment_id") != env:
        return {"environment_id": env, "tools": {}}
    return data


def save_state(owner, data):
    _, state_path = paths(owner)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now()
    temporary = state_path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(state_path)


def cached(owner, tool_id, workspace, required_version=None):
    entry = read_state(owner, workspace)["tools"].get(tool_id)
    if not entry or entry.get("status") != "installed":
        return None
    executable = Path(entry.get("executable", ""))
    if (not executable.is_file() or not os.access(executable, os.X_OK)
            or (required_version and entry.get("version") != required_version)):
        invalidate(owner, tool_id, workspace, "missing executable or incompatible version")
        return None
    return entry


def invalidate(owner, tool_id, workspace, reason):
    state = read_state(owner, workspace)
    state["tools"][tool_id] = {"status": "stale", "reason": reason, "last_attempt": now()}
    save_state(owner, state)


def detect(owner, tool_id, workspace, install_method="preexisting"):
    tool = registry_tool(owner, tool_id)
    executable = shutil.which(tool["command"])
    if not executable:
        return None
    if "verify_distribution" in tool:
        interpreter = next((str(candidate) for candidate in
                            (Path(executable).with_name("python"), Path(executable).with_name("python3"))
                            if candidate.is_file()), sys.executable)
        try:
            result = subprocess.run([interpreter, "-c",
                "import importlib.metadata as m; print(m.version(__import__('sys').argv[1]))",
                tool["verify_distribution"]], capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if result.returncode:
            return None
        version = result.stdout.strip()
    else:
        try:
            result = subprocess.run([executable, *tool["verify_args"]], capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if result.returncode:
            return None
        version = (result.stdout or result.stderr).strip().splitlines()[0]
    state = read_state(owner, workspace)
    entry = {"status": "installed", "version": version, "executable": str(Path(executable).resolve()),
             "source": tool["repository"], "install_method": install_method, "last_verified": now()}
    state["tools"][tool_id] = entry
    save_state(owner, state)
    return entry


def record_failure(owner, tool_id, workspace, reason):
    tool = registry_tool(owner, tool_id)
    state = read_state(owner, workspace)
    state["tools"][tool_id] = {"status": "install_failed", "source": tool["repository"],
                               "reason": reason, "last_attempt": now()}
    save_state(owner, state)


def run(owner, tool_id, workspace, args, required_version=None):
    entry = cached(owner, tool_id, workspace, required_version)
    source = "cached-installed"
    if entry is None:
        entry = detect(owner, tool_id, workspace)
        source = "detected-existing"
    if entry is None:
        return {"status": "missing", "tool_state_source": "unavailable"}
    if required_version and entry["version"] != required_version:
        invalidate(owner, tool_id, workspace, "incompatible required version")
        return {"status": "incompatible", "tool_state_source": source}
    try:
        result = subprocess.run([entry["executable"], *args], check=False)
    except FileNotFoundError:
        invalidate(owner, tool_id, workspace, "executable disappeared during execution")
        return {"status": "stale", "tool_state_source": source}
    return {"status": "executed", "exit_code": result.returncode, "tool_state_source": source,
            "tool_version": entry["version"], "tool_repository": entry["source"]}


def install(owner, tool_id, workspace, command, method, force_retry=False):
    """Run an owner-selected official installer without a shell, then verify."""
    registry_tool(owner, tool_id)
    if not command or not method or method == "preexisting":
        raise ValueError("installation command and actual method are required")
    previous = read_state(owner, workspace)["tools"].get(tool_id, {})
    if previous.get("status") == "install_failed" and not force_retry:
        return {"status": "retry_deferred", "reason": previous.get("reason", "previous failure")}
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired) as error:
        record_failure(owner, tool_id, workspace, type(error).__name__)
        return {"status": "install_failed", "reason": type(error).__name__}
    if result.returncode:
        record_failure(owner, tool_id, workspace, f"installer exit {result.returncode}")
        return {"status": "install_failed", "exit_code": result.returncode}
    entry = detect(owner, tool_id, workspace, method)
    if entry is None:
        record_failure(owner, tool_id, workspace, "installer exited successfully but verification failed")
        return {"status": "install_failed", "reason": "verification failed"}
    return {"status": "installed", "tool_version": entry["version"],
            "tool_repository": entry["source"], "installation_performed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner", choices=sorted(OWNERS))
    parser.add_argument("tool_id")
    parser.add_argument("action", choices=("resolve", "detect", "install", "run", "invalidate", "install-failed"))
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--required-version")
    parser.add_argument("--reason", default="")
    parser.add_argument("--install-method", default="preexisting")
    parser.add_argument("--force-retry", action="store_true")
    opts, tool_args = parser.parse_known_args()
    if opts.action == "resolve":
        result = cached(opts.owner, opts.tool_id, opts.workspace, opts.required_version)
    elif opts.action == "detect":
        result = detect(opts.owner, opts.tool_id, opts.workspace, opts.install_method)
    elif opts.action == "invalidate":
        invalidate(opts.owner, opts.tool_id, opts.workspace, opts.reason or "explicit invalidation")
        result = {"status": "stale"}
    elif opts.action == "install-failed":
        record_failure(opts.owner, opts.tool_id, opts.workspace, opts.reason or "installation failed")
        result = {"status": "install_failed"}
    elif opts.action == "install":
        result = install(opts.owner, opts.tool_id, opts.workspace,
                         tool_args[1:] if tool_args[:1] == ["--"] else tool_args,
                         opts.install_method, opts.force_retry)
    else:
        result = run(opts.owner, opts.tool_id, opts.workspace,
                     tool_args[1:] if tool_args[:1] == ["--"] else tool_args,
                     opts.required_version)
    print(json.dumps(result or {"status": "unknown"}, sort_keys=True))
    return 0 if result and result.get("status") not in ("missing", "stale", "incompatible", "install_failed", "retry_deferred") else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Local, per-skill tool availability cache. Never installs tools implicitly."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[3]


def paths(owner):
    if not isinstance(owner, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", owner):
        raise ValueError("invalid owner")
    registry_override = os.environ.get("TOOL_REGISTRY_PATH")
    state_override = os.environ.get("TOOL_STATE_PATH")
    if bool(registry_override) != bool(state_override):
        raise ValueError("TOOL_REGISTRY_PATH and TOOL_STATE_PATH must be set together")
    if registry_override and state_override:
        return Path(registry_override), Path(state_override)
    candidates = list((ROOT / "plugins").glob(f"*/skills/{owner}/references/tool-registry.json"))
    if len(candidates) != 1:
        raise ValueError("owner registry missing or ambiguous")
    registry = candidates[0]
    if not registry.resolve().is_relative_to((ROOT / "plugins").resolve()):
        raise ValueError("owner registry escapes plugin root")
    skill = registry.parent.parent
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
    if not isinstance(data, dict) or data.get("owner", owner) != owner or not isinstance(data.get("tools"), list):
        raise ValueError("invalid owner registry")
    matches = [tool for tool in data["tools"] if isinstance(tool, dict) and tool.get("id") == tool_id]
    if len(matches) != 1:
        raise ValueError("tool missing or ambiguous")
    tool = matches[0]
    source = urlsplit(tool.get("repository", ""))
    if source.scheme != "https" or not source.netloc or source.username or source.password or source.query or source.fragment:
        raise ValueError("invalid public tool repository")
    if not re.fullmatch(r"[a-zA-Z0-9_.+-]+", tool.get("command", "")) or tool["command"] in (".", ".."):
        raise ValueError("invalid executable name")
    args = tool.get("verify_args", [])
    if not isinstance(args, list) or not all(isinstance(arg, str) and "\x00" not in arg for arg in args):
        raise ValueError("invalid verification arguments")
    if not args and not isinstance(tool.get("verify_distribution"), str):
        raise ValueError("verification is required")
    return tool


def read_state(owner, workspace):
    _, state_path = paths(owner)
    env = fingerprint(workspace)
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if (not isinstance(data, dict) or data.get("environment_id") != env
            or not isinstance(data.get("tools"), dict)):
        return {"environment_id": env, "tools": {}}
    # Cache is operational evidence, not a container for arbitrary imported logs.
    keys = {"status", "version", "executable", "source", "install_method", "last_verified", "last_attempt"}
    return {"environment_id": env, "tools": {
        key: {field: value for field, value in entry.items() if field in keys and isinstance(value, str)}
        for key, entry in data["tools"].items() if isinstance(entry, dict)}}


def save_state(owner, data):
    _, state_path = paths(owner)
    state_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    data["updated_at"] = now()
    fd, name = tempfile.mkstemp(prefix=".tool-state-", dir=state_path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, sort_keys=True)
            stream.write("\n")
        temporary.replace(state_path)
    finally:
        temporary.unlink(missing_ok=True)


def cached(owner, tool_id, workspace, required_version=None, read_only=False):
    entry = read_state(owner, workspace)["tools"].get(tool_id)
    if not isinstance(entry, dict) or entry.get("status") != "installed":
        return None
    if not all(isinstance(entry.get(key), str) and entry[key] for key in ("executable", "version", "source")):
        return None
    executable = Path(entry["executable"])
    tool = registry_tool(owner, tool_id)
    expected = resolve_executable(tool["command"], workspace)
    if (not executable.is_file() or not os.access(executable, os.X_OK)
            or entry["source"] != tool["repository"]
            or expected != str(executable)
            or (required_version and entry.get("version") != required_version)):
        if not read_only:
            invalidate(owner, tool_id, workspace, "missing executable or incompatible version")
        return None
    return entry


def invalidate(owner, tool_id, workspace, reason):
    state = read_state(owner, workspace)
    state["tools"][tool_id] = {"status": "stale", "reason": "explicit invalidation", "last_attempt": now()}
    save_state(owner, state)


def resolve_executable(command, workspace):
    """Prefer the project environment without invoking a package manager."""
    if not isinstance(command, str) or not re.fullmatch(r"[a-zA-Z0-9_.+-]+", command) or command in (".", ".."):
        raise ValueError("invalid executable name")
    base = Path(workspace).resolve()
    for directory in (".venv/bin", ".venv/Scripts", "venv/bin", "venv/Scripts", "node_modules/.bin"):
        candidate = shutil.which(command, path=str(base / directory))
        if candidate:
            return str(Path(candidate).absolute())
    found = shutil.which(command)
    return str(Path(found).absolute()) if found else None


def probe(owner, tool_id, workspace, install_method="preexisting"):
    """Read-only availability verification. Never creates or invalidates state."""
    tool = registry_tool(owner, tool_id)
    if not isinstance(install_method, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,80}", install_method):
        raise ValueError("invalid installation method label")
    executable = resolve_executable(tool["command"], workspace)
    if not executable:
        return None
    if "verify_distribution" in tool:
        interpreter = next((str(candidate) for candidate in
                            (Path(executable).with_name("python"), Path(executable).with_name("python3"),
                             Path(executable).with_name("python.exe"))
                            if candidate.is_file()), sys.executable)
        try:
            result = subprocess.run([interpreter, "-c",
                "import importlib.metadata as m; print(m.version(__import__('sys').argv[1]))",
                tool["verify_distribution"]], capture_output=True, text=True, timeout=20, cwd=workspace)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if result.returncode:
            return None
        version = result.stdout.strip()
    else:
        try:
            result = subprocess.run([executable, *tool["verify_args"]], capture_output=True, text=True, timeout=20, cwd=workspace)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if result.returncode:
            return None
        version = result.stdout or result.stderr
    # Store the version token only, never arbitrary verification logs or secrets.
    match = re.search(r"(?<![\w.-])v?(\d+\.\d+(?:\.[0-9]+)*(?:[a-z][0-9]+)?)(?![\w.-])", version)
    if match is None:
        return None
    return {"status": "installed", "version": match.group(1), "executable": str(Path(executable).absolute()),
             "source": tool["repository"], "install_method": install_method, "last_verified": now()}


def detect(owner, tool_id, workspace, install_method="preexisting"):
    entry = probe(owner, tool_id, workspace, install_method)
    if entry is None:
        return None
    state = read_state(owner, workspace)
    state["tools"][tool_id] = entry
    save_state(owner, state)
    return entry


def record_failure(owner, tool_id, workspace, reason):
    tool = registry_tool(owner, tool_id)
    state = read_state(owner, workspace)
    state["tools"][tool_id] = {"status": "install_failed", "source": tool["repository"],
                               "reason": "installation failed", "last_attempt": now()}
    save_state(owner, state)


def run(owner, tool_id, workspace, args, required_version=None, *, quiet=False):
    if not Path(workspace).is_dir():
        return {"status": "invalid_workspace", "reason": "workspace must be an existing directory"}
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
        result = subprocess.run([entry["executable"], *args], check=False, cwd=workspace,
                                stdout=subprocess.DEVNULL if quiet else None,
                                stderr=subprocess.DEVNULL if quiet else None)
    except OSError:
        invalidate(owner, tool_id, workspace, "executable disappeared during execution")
        return {"status": "stale", "tool_state_source": source}
    return {"status": "executed", "exit_code": result.returncode, "tool_state_source": source,
            "tool_version": entry["version"], "tool_repository": entry["source"]}


def install(owner, tool_id, workspace, command, method, force_retry=False):
    """Run an owner-selected official installer without a shell, then verify."""
    registry_tool(owner, tool_id)
    if not command or not method or method == "preexisting":
        raise ValueError("installation command and actual method are required")
    if not isinstance(method, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,80}", method):
        raise ValueError("invalid installation method label")
    previous = read_state(owner, workspace)["tools"].get(tool_id, {})
    if previous.get("status") == "install_failed" and not force_retry:
        return {"status": "retry_deferred", "reason": previous.get("reason", "previous failure")}
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=300, cwd=workspace)
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
    parser.add_argument("owner")
    parser.add_argument("tool_id")
    parser.add_argument("action", choices=("resolve", "probe", "detect", "install", "run", "invalidate", "install-failed"))
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--required-version")
    parser.add_argument("--reason", default="")
    parser.add_argument("--install-method", default="preexisting")
    parser.add_argument("--force-retry", action="store_true")
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="suppress output of an explicitly run tool")
    opts, tool_args = parser.parse_known_args()
    if opts.read_only and opts.action not in ("resolve", "probe"):
        parser.error("--read-only is supported only for resolve and probe")
    if opts.action == "resolve":
        result = cached(opts.owner, opts.tool_id, opts.workspace, opts.required_version, opts.read_only)
    elif opts.action == "probe":
        result = probe(opts.owner, opts.tool_id, opts.workspace)
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
                     opts.required_version, quiet=opts.quiet)
    print(json.dumps(result or {"status": "unknown"}, sort_keys=True))
    if result and result.get("status") == "executed":
        code = result["exit_code"]
        return code if code >= 0 else 128 - code
    return 0 if result and result.get("status") not in ("missing", "stale", "incompatible", "install_failed", "retry_deferred", "invalid_workspace") else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"status": "error", "reason": "invalid configuration or inaccessible local state"}))
        raise SystemExit(2)

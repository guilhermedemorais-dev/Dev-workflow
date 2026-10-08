"""Safely enable read-only GitHub Actions tools in Codex or Claude MCP config."""
import argparse
import json
from pathlib import Path
import re
import tempfile
import sys
import tomllib

TOOLS = "actions_list,actions_get,get_job_logs"
ENDPOINT = "https://api.githubcopilot.com/mcp/"
HEADERS = {
    "X-MCP-Tools": TOOLS,
    "X-MCP-Exclude-Tools": "actions_run_trigger",
    "X-MCP-Readonly": "true",
}


def _merge_headers(headers):
    if not isinstance(headers, dict):
        raise ValueError("invalid headers")
    merged = dict(headers)
    for key, value in HEADERS.items():
        previous = merged.get(key)
        if previous is not None and previous != value:
            if key == "X-MCP-Tools":
                merged[key] = ",".join(dict.fromkeys(x.strip() for x in (previous + "," + value).split(",") if x.strip()))
            elif key == "X-MCP-Exclude-Tools":
                merged[key] = ",".join(dict.fromkeys(x.strip() for x in (previous + "," + value).split(",") if x.strip()))
            else:
                merged[key] = value
        else:
            merged[key] = value
    return merged


def update_claude(path):
    path = Path(path)
    original = path.read_text() if path.exists() else None
    data = json.loads(original) if original is not None else {}
    servers = data.setdefault("mcpServers", {})
    server = servers.get("github")
    if server is None:
        server = {"type": "http", "url": ENDPOINT}
        servers["github"] = server
    if not isinstance(server, dict) or server.get("url") != ENDPOINT:
        raise ValueError("GitHub MCP server is not an official compatible endpoint")
    server["headers"] = _merge_headers(server.get("headers", {}))
    content = json.dumps(data, indent=2) + "\n"
    if original == content:
        return False
    _atomic(path, content, original)
    return True


def update_codex(path):
    path = Path(path)
    original = path.read_text() if path.exists() else None
    source = original or ""
    data = tomllib.loads(source)
    server = data.get("mcp_servers", {}).get("github")
    if server is None:
        if "mcp_servers" in data and not isinstance(data["mcp_servers"], dict):
            raise ValueError("invalid MCP server table")
        addition = "\n[mcp_servers.github]\nurl = " + json.dumps(ENDPOINT) + "\nhttp_headers = { " + ", ".join(
            json.dumps(key) + " = " + json.dumps(value) for key, value in HEADERS.items()) + " }\n"
        content = source.rstrip() + "\n" + addition
        tomllib.loads(content)
        _atomic(path, content, original)
        return True
    if not isinstance(server, dict) or server.get("url") != ENDPOINT:
        raise ValueError("GitHub MCP server is not an official compatible endpoint")
    headers = _merge_headers(server.get("http_headers", {}))
    # Locate just the github table and rewrite only its http_headers value.
    match = re.search(r"(?ms)^\[mcp_servers\.github\]\s*$", source)
    if not match:
        raise ValueError("unsupported GitHub MCP TOML table")
    end_match = re.search(r"(?m)^\[", source[match.end():])
    end = match.end() + end_match.start() if end_match else len(source)
    table = source[match.end():end]
    header_line = re.search(r"(?m)^http_headers\s*=.*$", table)
    encoded = "{ " + ", ".join(json.dumps(key, ensure_ascii=False) + " = " +
                                   json.dumps(value, ensure_ascii=False)
                                   for key, value in headers.items()) + " }"
    if header_line:
        table = table[:header_line.start()] + "http_headers = " + encoded + table[header_line.end():]
    else:
        table += "\nhttp_headers = " + encoded + "\n"
    content = source[:match.end()] + table + source[end:]
    tomllib.loads(content)
    if content == source:
        return False
    _atomic(path, content, original)
    return True


def classify_repository_access(repository, workflow_status, runs_status, jobs_status, logs_status):
    """Classify observed HTTP statuses without extrapolating to other repositories."""
    checks = {"workflows": workflow_status, "runs": runs_status, "jobs": jobs_status, "logs": logs_status}
    if not isinstance(repository, str) or not repository.strip() or any(type(code) is not int for code in checks.values()):
        raise ValueError("invalid repository evidence")
    if all(code == 200 for code in checks.values()):
        status = "VERIFIED_READ"
    elif any(code == 403 for code in checks.values()):
        status = "DENIED_PERMISSION_OR_POLICY"
    elif any(code == 404 for code in checks.values()):
        status = "NOT_FOUND_OR_NO_REPOSITORY_ACCESS"
    else:
        status = "UNVERIFIED"
    return {"repository": repository, "status": status, "checks": checks}


def _atomic(path, content, expected_source):
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text() if path.exists() else None
    if current != expected_source:
        raise ValueError("host configuration changed during update")
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                     prefix="." + path.name + ".", delete=False) as handle:
        temp = Path(handle.name)
        handle.write(content)
    temp.chmod(mode)
    current = path.read_text() if path.exists() else None
    if current != expected_source:
        temp.unlink(missing_ok=True)
        raise ValueError("host configuration changed during update")
    temp.replace(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", choices=("codex", "claude"))
    parser.add_argument("--config", required=True)
    args = parser.parse_args(argv)
    try:
        changed = update_codex(args.config) if args.host == "codex" else update_claude(args.config)
        print(json.dumps({"status": "UPDATED" if changed else "ALREADY_CONFIGURED", "host": args.host,
                          "actions_tools": ["actions_list", "actions_get", "get_job_logs"],
                          "trigger_excluded": True, "readonly": True}))
        return 0
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({"status": "BLOCKED", "error": "invalid or inaccessible MCP configuration"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

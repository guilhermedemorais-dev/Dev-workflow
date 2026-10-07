#!/usr/bin/env python3
"""Retrieve bounded workspace context for an Engineering Harness execution list."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import fnmatch
import json
from pathlib import Path
import re
import shutil
import subprocess
from typing import Iterable


EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "coverage",
    ".next", ".cache", "__pycache__", ".venv", "venv", "runtime-state"
}
SECRET_NAMES = {
    ".env", ".env.local", ".env.production", ".npmrc", ".pypirc",
    "id_rsa", "id_ed25519", "credentials", "credentials.json"
}
TEXT_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".php", ".go", ".rs", ".java", ".kt",
    ".rb", ".cs", ".c", ".cc", ".cpp", ".h", ".hpp", ".sql", ".sh", ".bash",
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".xml", ".html",
    ".css", ".scss", ".vue", ".svelte", ".graphql", ".gql"
}
MAX_FILE_BYTES = 512 * 1024


@dataclass(frozen=True)
class Hit:
    path: str
    score: float
    line_start: int
    line_end: int
    snippet: str

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "score": round(self.score, 4),
            "line_start": self.line_start,
            "line_end": self.line_end,
            "snippet": self.snippet,
        }


def workspace_root(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise ValueError("workspace must be an existing directory")
    return root


def is_secret(path: Path) -> bool:
    name = path.name.lower()
    return name in SECRET_NAMES or name.startswith(".env.") or name.endswith((".pem", ".key", ".p12", ".pfx"))


def relative_safe(root: Path, path: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("path escapes workspace")
    return resolved.relative_to(root).as_posix()


def allowed(relative: str, patterns: list[str]) -> bool:
    if not patterns:
        return True
    for pattern in patterns:
        normalized = pattern.replace("\\", "/").lstrip("./")
        prefix = normalized.rstrip("/*")
        if fnmatch.fnmatch(relative, normalized) or relative == prefix or relative.startswith(prefix + "/"):
            return True
    return False


def iter_files(root: Path, patterns: list[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = relative_safe(root, path)
        parts = Path(relative).parts
        if any(part in EXCLUDED_DIRS for part in parts):
            continue
        if is_secret(path) or not allowed(relative, patterns):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Dockerfile", "Makefile", "README"}:
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        yield path


def tokenize(query: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9_./:-]{2,}", query)]


def lexical_hit(root: Path, path: Path, query: str, terms: list[str]) -> Hit | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    lowered = text.lower()
    query_l = query.strip().lower()
    phrase = lowered.find(query_l) if query_l else -1
    term_positions = [lowered.find(term) for term in terms if term in lowered]
    if phrase < 0 and not term_positions:
        return None

    score = 0.0
    if phrase >= 0:
        score += 5.0
    for term in terms:
        count = lowered.count(term)
        if count:
            score += min(count, 10) * 0.4

    lines = text.splitlines()
    char_pos = phrase if phrase >= 0 else min(term_positions)
    line_index = text[:char_pos].count("\n")
    start = max(0, line_index - 3)
    end = min(len(lines), line_index + 5)
    snippet = "\n".join(lines[start:end])
    return Hit(relative_safe(root, path), score, start + 1, end, snippet)


def local_search(root: Path, query: str, patterns: list[str], limit: int) -> list[Hit]:
    terms = tokenize(query)
    hits = []
    for path in iter_files(root, patterns):
        hit = lexical_hit(root, path, query, terms)
        if hit:
            hits.append(hit)
    hits.sort(key=lambda item: (-item.score, item.path))
    return hits[:limit]


def required_sources(root: Path, sources: list[str], patterns: list[str]) -> tuple[list[dict], list[str]]:
    loaded: list[dict] = []
    warnings: list[str] = []
    for raw in sources:
        path = (root / raw).resolve()
        try:
            relative = relative_safe(root, path)
        except ValueError:
            warnings.append(f"required_source_escape:{raw}")
            continue
        if not path.is_file():
            warnings.append(f"required_source_missing:{raw}")
            continue
        if is_secret(path):
            warnings.append(f"required_source_secret_blocked:{raw}")
            continue
        if patterns and not allowed(relative, patterns):
            warnings.append(f"required_source_outside_allowed_paths:{raw}")
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            warnings.append(f"required_source_unreadable:{raw}")
            continue
        loaded.append({
            "path": relative,
            "line_start": 1,
            "line_end": min(len(lines), 120),
            "snippet": "\n".join(lines[:120]),
            "normative": True,
        })
    return loaded, warnings


def potpie_search(root: Path, query: str, limit: int) -> tuple[list[Hit] | None, str | None]:
    executable = shutil.which("potpie")
    if not executable:
        return None, "potpie_not_installed"
    try:
        result = subprocess.run(
            [executable, "--json", "search", query],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=25,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None, "potpie_execution_failed"
    if result.returncode != 0:
        return None, "potpie_not_ready"
    try:
        payload = json.loads(result.stdout)
    except ValueError:
        return None, "potpie_invalid_json"

    items = payload.get("items", []) if isinstance(payload, dict) else []
    hits: list[Hit] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        body = item.get("payload", {})
        if not isinstance(body, dict):
            continue
        path = body.get("path") or body.get("source_path") or body.get("file")
        snippet = body.get("fact") or body.get("summary") or body.get("snippet")
        if not isinstance(path, str) or not isinstance(snippet, str):
            continue
        candidate = (root / path).resolve()
        try:
            relative = relative_safe(root, candidate)
        except ValueError:
            continue
        if is_secret(candidate):
            continue
        score = item.get("score")
        hits.append(Hit(relative, float(score) if isinstance(score, (int, float)) else 0.0, 0, 0, snippet))
        if len(hits) >= limit:
            break
    return hits, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--allowed-path", action="append", default=[])
    parser.add_argument("--required-source", action="append", default=[])
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--backend", choices=("auto", "potpie", "local"), default="auto")
    args = parser.parse_args()

    root = workspace_root(args.workspace)
    limit = min(max(args.limit, 1), 50)
    required, warnings = required_sources(root, args.required_source, args.allowed_path)

    hits: list[Hit] | None = None
    backend = "local"
    if args.backend in {"auto", "potpie"}:
        hits, warning = potpie_search(root, args.query, limit)
        if warning:
            warnings.append(warning)
        elif hits is not None:
            filtered = [hit for hit in hits if allowed(hit.path, args.allowed_path)]
            hits = filtered[:limit]
            backend = "potpie"

    if hits is None or (args.backend == "auto" and not hits):
        hits = local_search(root, args.query, args.allowed_path, limit)
        backend = "local"

    required_paths = {item["path"] for item in required}
    results = [hit.as_dict() for hit in hits if hit.path not in required_paths]
    output = {
        "backend": backend,
        "query": args.query,
        "required_sources": required,
        "results": results,
        "warnings": sorted(set(warnings)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

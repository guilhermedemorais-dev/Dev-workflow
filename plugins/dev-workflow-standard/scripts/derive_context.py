#!/usr/bin/env python3
"""Create and verify opt-in, excerpt-based derived context artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


class ContextError(ValueError):
    def __init__(self, message: str, fallback_text: str = ""):
        super().__init__(message)
        self.fallback_text = fallback_text


SECRET_NAMES = {
    ".env", ".env.local", ".env.production", ".npmrc", ".pypirc",
    "id_rsa", "id_ed25519", "credentials", "credentials.json",
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(?:password|token|secret|api[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9/+_=-]{12,}"),
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _within_root(path: Path, root: Path, label: str) -> Path:
    resolved_root = root.resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ContextError(f"{label} resolves outside the allowed root")
    return resolved


def _read_plan(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContextError(f"cannot read plan: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ContextError("plan must be a JSON object with schema_version 1")
    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ContextError("plan requires at least one source")
    cases = value.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ContextError("plan requires curated positive retrieval cases")
    controls = value.get("negative_controls")
    if not isinstance(controls, list) or not controls:
        raise ContextError("plan requires negative mutation controls")
    if not any(c.get("operation") == "remove" for c in controls if isinstance(c, dict)):
        raise ContextError("plan requires a remove-exception control")
    if not any(c.get("operation") == "replace" for c in controls if isinstance(c, dict)):
        raise ContextError("plan requires an inversion control")
    return value


def _excerpt_source(item: dict[str, Any], root: Path) -> dict[str, Any]:
    if not isinstance(item, dict) or not isinstance(item.get("path"), str):
        raise ContextError("each source requires a path")
    source_name = Path(item["path"]).name.lower()
    if source_name in SECRET_NAMES or source_name.startswith(".env."):
        raise ContextError(f"sensitive source path is excluded: {Path(item['path']).name}")
    relative = Path(item["path"])
    if relative.is_absolute():
        raise ContextError("source paths must be relative to the allowed root")
    path = _within_root(root / relative, root, "source path")
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise ContextError(f"cannot read UTF-8 source {item.get('path')!r}: {exc}") from exc
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        raise ContextError(f"possible secret detected in source {item['path']!r}")
    lines = text.splitlines(keepends=True)
    selections = item.get("selections")
    if not isinstance(selections, list) or not selections:
        raise ContextError(f"source {item['path']!r} requires line selections")
    excerpts: list[dict[str, Any]] = []
    seen: set[int] = set()
    for selection in selections:
        if not isinstance(selection, dict):
            raise ContextError("line selections must be objects")
        start, end = selection.get("start"), selection.get("end")
        purpose = selection.get("purpose")
        if (not isinstance(start, int) or isinstance(start, bool) or
                not isinstance(end, int) or isinstance(end, bool) or
                start < 1 or end < start or end > len(lines)):
            raise ContextError(f"invalid line range for {item['path']!r}")
        if not isinstance(purpose, str) or not purpose.strip():
            raise ContextError("each excerpt requires a non-empty purpose")
        selected = set(range(start, end + 1))
        if seen & selected:
            raise ContextError(f"overlapping line selections in {item['path']!r}")
        seen.update(selected)
        excerpts.append({
            "lines": [start, end],
            "purpose": purpose,
            "text": "".join(lines[start - 1:end]),
        })
    excerpts.sort(key=lambda excerpt: excerpt["lines"][0])
    return {
        "reference": path.relative_to(root.resolve()).as_posix(),
        "sha256": sha256(raw),
        "excerpts": excerpts,
        "_full_text": text,
    }


def _derived_text(sources: list[dict[str, Any]]) -> str:
    blocks = []
    for source in sources:
        for excerpt in source["excerpts"]:
            blocks.append(excerpt["text"])
    return "".join(blocks)


def evaluate_positive_facts(text: str, plan: dict[str, Any], label: str) -> list[str]:
    failures: list[str] = []
    for case in plan["cases"]:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            failures.append("invalid retrieval case")
            continue
        required = case.get("must_include")
        if not isinstance(required, list) or not required:
            failures.append(f"{case['id']}: must_include is empty")
            continue
        for fact in required:
            if not isinstance(fact, str) or not fact or fact not in text:
                failures.append(f"{case['id']}: expected fact not present in {label}")
    return failures


def evaluate(text: str, plan: dict[str, Any]) -> list[str]:
    failures = evaluate_positive_facts(text, plan, "derived context")
    for control in plan["negative_controls"]:
        if not isinstance(control, dict) or not isinstance(control.get("id"), str):
            failures.append("invalid negative control")
            continue
        operation = control.get("operation")
        target = control.get("target")
        if not isinstance(target, str) or not target or target not in text:
            failures.append(f"{control['id']}: mutation target absent")
            continue
        changed = text.replace(target, "", 1)
        if operation == "replace":
            replacement = control.get("replacement")
            if not isinstance(replacement, str) or not replacement:
                failures.append(f"{control['id']}: replacement is empty")
                continue
            changed = text.replace(target, replacement, 1)
        elif operation != "remove":
            failures.append(f"{control['id']}: unsupported mutation")
            continue
        guards = control.get("must_fail_cases")
        if not isinstance(guards, list) or not guards:
            failures.append(f"{control['id']}: must_fail_cases is empty")
            continue
        by_id = {case.get("id"): case for case in plan["cases"] if isinstance(case, dict)}
        for case_id in guards:
            case = by_id.get(case_id)
            if case is None:
                failures.append(f"{control['id']}: unknown guarded case")
            else:
                required_facts = case.get("must_include", [])
                # A case fails when any required fact is missing; the mutation is
                # undetected only if every required fact remains present.
                case_still_passes = bool(required_facts) and all(
                    isinstance(fact, str) and fact in changed for fact in required_facts
                )
                if case_still_passes:
                    failures.append(f"{control['id']}: mutation was not detected by {case_id}")
    return failures


def build_artifact(plan_path: Path, root: Path | None = None) -> tuple[dict[str, Any], str]:
    root = (root or plan_path.parent).resolve()
    plan_path = _within_root(plan_path, root, "plan path")
    plan = _read_plan(plan_path)
    sources = [_excerpt_source(item, root) for item in plan["sources"]]
    original_text = "\n".join(source["_full_text"] for source in sources)
    source_failures = evaluate_positive_facts(original_text, plan, "canonical source")
    if source_failures:
        raise ContextError("curated cases are not answerable from the canonical source: " + "; ".join(source_failures), original_text)
    text = _derived_text(sources)
    failures = evaluate(text, plan)
    if failures:
        fallback = "\n".join(source["_full_text"] for source in sources)
        raise ContextError("curated retrieval evaluation failed: " + "; ".join(failures), fallback)
    source_bytes = sum(len(source["_full_text"].encode("utf-8")) for source in sources)
    derived_bytes = len(text.encode("utf-8"))
    if source_bytes == 0 or derived_bytes >= source_bytes:
        fallback = "\n".join(source["_full_text"] for source in sources)
        raise ContextError("derived context is not smaller than its canonical source set", fallback)
    clean_sources = [{k: v for k, v in source.items() if k != "_full_text"} for source in sources]
    artifact = {
        "schema_version": 1,
        "mode": "opt_in_exact_excerpts",
        "plan_reference": plan_path.relative_to(root).as_posix(),
        "plan_sha256": sha256(plan_path.read_bytes()),
        "evaluation": {
            "method": "curated literal retrieval assertions and mutation controls",
            "positive_cases": len(plan["cases"]),
            "comparison": "expected literals checked in canonical source and derived excerpts",
            "negative_controls": len(plan["negative_controls"]),
            "result": "PASS",
            "semantic_equivalence_claim": False,
            "size_measurement": {
                "method": "UTF-8 bytes",
                "canonical_source_bytes": source_bytes,
                "derived_context_bytes": derived_bytes,
                "reduction_ratio": round(1 - derived_bytes / source_bytes, 4),
            },
        },
        "sources": clean_sources,
        "derived_context": text,
    }
    return artifact, text


def _atomic_write(destination: Path, data: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    mode = destination.stat().st_mode & 0o777 if destination.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def verify_artifact(artifact_path: Path, root: Path | None = None) -> tuple[bool, str, str]:
    root = (root or artifact_path.parent).resolve()
    try:
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        if not isinstance(artifact, dict):
            raise ContextError("derived-context artifact must be a JSON object")
        if (artifact.get("schema_version") != 1 or
                not isinstance(artifact.get("sources"), list) or not artifact["sources"] or
                not isinstance(artifact.get("plan_reference"), str) or
                not isinstance(artifact.get("plan_sha256"), str)):
            raise ContextError("invalid derived-context artifact")
        if any(not isinstance(item, dict) or not isinstance(item.get("reference"), str) or
               not isinstance(item.get("sha256"), str) for item in artifact["sources"]):
            raise ContextError("invalid derived-context source records")
        plan_reference = Path(artifact["plan_reference"])
        if plan_reference.is_absolute():
            raise ContextError("artifact plan reference must be relative to the allowed root")
        plan_path = _within_root(root / plan_reference, root, "artifact plan reference")
        plan_bytes = plan_path.read_bytes()
        if sha256(plan_bytes) != artifact["plan_sha256"]:
            return False, "curated plan changed; regenerate and review derived context", ""
        for item in artifact["sources"]:
            reference = Path(item["reference"])
            if reference.is_absolute():
                raise ContextError("artifact source reference must be relative to the allowed root")
            path = _within_root(root / reference, root, "artifact source reference")
            raw = path.read_bytes()
            if sha256(raw) != item["sha256"]:
                return False, "source changed; use canonical source", raw.decode("utf-8", errors="replace")
        current_artifact, _ = build_artifact(plan_path, root)
        current_artifact["plan_reference"] = artifact["plan_reference"]
        if current_artifact != artifact:
            return False, "derived context or evaluation changed; use canonical source", ""
        return True, "source and plan hashes current; curated retrieval and mutation checks pass", ""
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ContextError) as exc:
        return False, f"cannot verify derived context: {exc}", ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, help="curated JSON plan to create an artifact")
    parser.add_argument("--output", type=Path, help="artifact output path, written atomically")
    parser.add_argument("--verify", type=Path, help="verify source hashes in an existing artifact")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="allowed root for plan and source paths (default: current directory)")
    args = parser.parse_args()
    try:
        if args.verify:
            ok, message, fallback = verify_artifact(args.verify, args.root)
            print(message, file=sys.stderr)
            if not ok:
                if fallback:
                    sys.stdout.write(fallback)
                return 2
            return 0
        if not args.plan or not args.output:
            parser.error("--plan and --output are required unless --verify is used")
        artifact, _ = build_artifact(args.plan, args.root)
        root = args.root.resolve()
        protected_paths = {
            _within_root(args.plan, root, "plan path"),
            *(_within_root(root / Path(source["reference"]), root, "source path") for source in artifact["sources"]),
        }
        if args.output.resolve() in protected_paths:
            raise ContextError("output path must not overwrite the plan or a canonical source")
        _atomic_write(args.output, (json.dumps(artifact, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        print("derived context created; opt-in only; source hashes and curated checks recorded")
        return 0
    except (ContextError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        fallback = getattr(exc, "fallback_text", "")
        if fallback:
            sys.stdout.write(fallback)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

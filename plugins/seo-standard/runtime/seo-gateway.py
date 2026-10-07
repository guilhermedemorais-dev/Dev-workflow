#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = json.loads((HERE / "runtime.lock.json").read_text(encoding="utf-8"))
ZIP = (HERE / LOCK["vendored_zip"]).resolve()
RUNTIME = HERE / ".runtime"

def find_project(root: Path):
    candidates = [root] + [p for p in root.iterdir() if p.is_dir()]
    return next((p for p in candidates if (p / "scripts" / "run.py").is_file()), None)

def python_bin():
    return RUNTIME / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

def run_cli(args):
    py = python_bin()
    if not py.is_file():
        print(json.dumps({"ok": False, "error": "runtime_not_bootstrapped"}))
        return 2
    with tempfile.TemporaryDirectory(prefix="seo-standard-run-") as tmp:
        root = Path(tmp) / "source"
        with zipfile.ZipFile(ZIP) as zf:
            zf.extractall(root)
        project = find_project(root)
        if project is None:
            print(json.dumps({"ok": False, "error": "vendored_runtime_invalid"}))
            return 2
        cmd = [str(py), str(project / "scripts" / "run.py"), "--runtime", str(RUNTIME), *args]
        return subprocess.call(cmd)

action = sys.argv[1] if len(sys.argv) > 1 else "probe"
if action == "probe":
    raise SystemExit(run_cli(["doctor"]))
if action == "audit":
    if len(sys.argv) < 4:
        print("usage: seo-gateway.py audit <url> <out-dir> [extra BeyondSEO args...]", file=sys.stderr)
        raise SystemExit(2)
    url, out = sys.argv[2], sys.argv[3]
    raise SystemExit(run_cli(["crawl", url, "--out", out, *sys.argv[4:]]))
if action == "cli":
    raise SystemExit(run_cli(sys.argv[2:]))
print("unknown action", file=sys.stderr)
raise SystemExit(2)

#!/usr/bin/env python3
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOCK = json.loads((HERE / "runtime.lock.json").read_text(encoding="utf-8"))
ZIP = (HERE / LOCK["vendored_zip"]).resolve()
EXPECTED = LOCK["sha256"]
RUNTIME = HERE / ".runtime"

def fail(message, code=1):
    print(message, file=sys.stderr)
    raise SystemExit(code)

if not ZIP.is_file():
    fail("vendored BeyondSEO runtime is missing")

actual = hashlib.sha256(ZIP.read_bytes()).hexdigest()
if actual != EXPECTED:
    fail("vendored BeyondSEO checksum mismatch")

if sys.version_info < (3, 10):
    fail("Python 3.10+ is required", 2)

with tempfile.TemporaryDirectory(prefix="seo-standard-") as tmp:
    source = Path(tmp) / "source"
    with zipfile.ZipFile(ZIP) as zf:
        zf.extractall(source)

    candidates = [source]
    children = [p for p in source.iterdir() if p.is_dir()]
    if len(children) == 1:
        candidates.insert(0, children[0])

    project = next((p for p in candidates if (p / "scripts" / "setup.py").is_file()), None)
    if project is None:
        fail("BeyondSEO setup.py not found in vendored runtime")

    if RUNTIME.exists():
        shutil.rmtree(RUNTIME)

    command = [
        sys.executable,
        str(project / "scripts" / "setup.py"),
        "--venv",
        str(RUNTIME),
    ]
    result = subprocess.run(command)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

print(json.dumps({
    "runtime": "BeyondSEO",
    "version": LOCK["version"],
    "source": "vendored-release",
    "sha256": actual,
    "runtime_path": str(RUNTIME),
}, indent=2))

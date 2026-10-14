#!/usr/bin/env python3
import hashlib
import argparse
import stat
import json
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
parser = argparse.ArgumentParser(description='Prepare the pinned local BeyondSEO runtime.')
parser.add_argument('--http-only', action='store_true', help='Prepare HTTP/report dependencies without optional browser installation.')
args = parser.parse_args()

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

    try:
        runtime_attributes = getattr(RUNTIME.lstat(), 'st_file_attributes', 0)
    except FileNotFoundError:
        runtime_attributes = 0
    if RUNTIME.is_symlink() or runtime_attributes & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400):
        fail('runtime reparse point is not an approved installation target')

    command = [
        sys.executable,
        str(project / "scripts" / "setup.py"),
        "--venv",
        str(RUNTIME),
    ]
    if args.http_only:
        command.append('--http-only')
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

#!/usr/bin/env python3
"""Generate a deterministic JSON manifest for a cinematic frame directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FRAME_RE = re.compile(r"^(?P<prefix>.+?)(?P<number>\d+)(?P<ext>\.(?:webp|avif|jpg|jpeg|png))$", re.IGNORECASE)


def collect_frames(directory: Path):
    frames = []
    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = FRAME_RE.match(path.name)
        if not match:
            continue
        frames.append((int(match.group("number")), path))
    frames.sort(key=lambda item: (item[0], item[1].name))
    return frames


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--base-url", default="", help="Optional URL prefix for frame src values")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        print(f"Error: directory not found: {directory}", file=sys.stderr)
        return 2

    frames = collect_frames(directory)
    if not frames:
        print(f"Error: no numbered image frames found in {directory}", file=sys.stderr)
        return 1

    base = args.base_url.rstrip("/")
    payload = {
        "frameCount": len(frames),
        "firstFrameNumber": frames[0][0],
        "lastFrameNumber": frames[-1][0],
        "totalBytes": sum(path.stat().st_size for _, path in frames),
        "frames": [
            {
                "index": number,
                "file": path.name,
                "src": f"{base}/{path.name}" if base else path.name,
                "bytes": path.stat().st_size,
            }
            for number, path in frames
        ],
    }

    json.dump(payload, sys.stdout, indent=2 if args.pretty else None, separators=None if args.pretty else (",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

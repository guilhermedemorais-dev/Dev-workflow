#!/usr/bin/env python3
"""Validate numbered cinematic frames for gaps and media-budget violations."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRAME_RE = re.compile(r"^(?P<prefix>.+?)(?P<number>\d+)(?P<ext>\.(?:webp|avif|jpg|jpeg|png))$", re.IGNORECASE)


def collect(directory: Path):
    rows = []
    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = FRAME_RE.match(path.name)
        if match:
            rows.append((int(match.group("number")), path))
    rows.sort(key=lambda item: (item[0], item[1].name))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--max-total-mb", type=float, default=35.0)
    parser.add_argument("--max-frame-kb", type=float, default=350.0)
    parser.add_argument("--max-frames", type=int, default=800)
    parser.add_argument("--strict", action="store_true", help="Treat all warnings as errors")
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        print(f"ERROR directory not found: {directory}")
        return 2

    rows = collect(directory)
    if not rows:
        print("ERROR no numbered image frames found")
        return 1

    numbers = [number for number, _ in rows]
    expected = set(range(numbers[0], numbers[-1] + 1))
    missing = sorted(expected.difference(numbers))
    duplicate_numbers = sorted({n for n in numbers if numbers.count(n) > 1})
    total_bytes = sum(path.stat().st_size for _, path in rows)
    largest_number, largest_path = max(rows, key=lambda item: item[1].stat().st_size)
    largest_bytes = largest_path.stat().st_size

    errors = []
    warnings = []

    if missing:
        errors.append(f"missing frame numbers: {missing[:20]}{' ...' if len(missing) > 20 else ''}")
    if duplicate_numbers:
        errors.append(f"duplicate frame numbers: {duplicate_numbers[:20]}")
    if len(rows) > args.max_frames:
        warnings.append(f"frame count {len(rows)} exceeds budget {args.max_frames}")

    max_total_bytes = args.max_total_mb * 1024 * 1024
    max_frame_bytes = args.max_frame_kb * 1024
    if total_bytes > max_total_bytes:
        warnings.append(f"total size {total_bytes / 1024 / 1024:.2f} MB exceeds budget {args.max_total_mb:.2f} MB")
    if largest_bytes > max_frame_bytes:
        warnings.append(
            f"largest frame {largest_path.name} ({largest_bytes / 1024:.1f} KB) exceeds budget {args.max_frame_kb:.1f} KB"
        )

    print(f"frames={len(rows)} range={numbers[0]}-{numbers[-1]}")
    print(f"total_mb={total_bytes / 1024 / 1024:.2f}")
    print(f"largest_frame={largest_path.name} largest_kb={largest_bytes / 1024:.1f}")

    for item in errors:
        print(f"ERROR {item}")
    for item in warnings:
        print(f"WARNING {item}")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

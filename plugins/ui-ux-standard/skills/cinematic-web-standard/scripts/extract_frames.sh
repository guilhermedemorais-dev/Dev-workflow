#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <input-video> <output-dir> [fps=12] [max-width=1920] [webp-quality=82]" >&2
  exit 2
fi

INPUT=$1
OUTPUT_DIR=$2
FPS=${3:-12}
MAX_WIDTH=${4:-1920}
QUALITY=${5:-82}

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg is required but was not found in PATH." >&2
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: input video not found: $INPUT" >&2
  exit 1
fi

case "$FPS" in
  ''|*[!0-9.]* ) echo "Error: fps must be numeric." >&2; exit 2 ;;
esac
case "$MAX_WIDTH" in
  ''|*[!0-9]* ) echo "Error: max-width must be an integer." >&2; exit 2 ;;
esac
case "$QUALITY" in
  ''|*[!0-9]* ) echo "Error: webp-quality must be an integer." >&2; exit 2 ;;
esac

mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/frame-*.webp

ffmpeg -hide_banner -loglevel error -y \
  -i "$INPUT" \
  -vf "fps=${FPS},scale=${MAX_WIDTH}:-2:force_original_aspect_ratio=decrease:flags=lanczos" \
  -an \
  -c:v libwebp \
  -quality "$QUALITY" \
  -compression_level 6 \
  "$OUTPUT_DIR/frame-%05d.webp"

COUNT=$(find "$OUTPUT_DIR" -maxdepth 1 -type f -name 'frame-*.webp' | wc -l | tr -d ' ')
if [ "$COUNT" -eq 0 ]; then
  echo "Error: ffmpeg completed but no frames were produced." >&2
  exit 1
fi

echo "Extracted $COUNT WebP frames to $OUTPUT_DIR"

#!/usr/bin/env bash
set -euo pipefail

# Convert PPTX if slides directory empty
if [ -z "$(ls -A /app/slides 2>/dev/null)" ]; then
  echo "No slides found; attempting conversion..."
  python /app/convert.py --pptx "${PPTX_FILE:-/app/e_learning_platform_architecture.pptx}" --out /app/slides || true
fi

# Start Flask
exec python /app/app.py

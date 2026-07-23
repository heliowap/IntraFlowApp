#!/usr/bin/env bash
# Render perennial OG card: og.html → og.png (+ og-image.png). No version in the art.
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
HTML="file://$(pwd)/og.html?still=1"
OUT="$(pwd)/og.png"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --screenshot="$OUT" "$HTML" 2>/dev/null
sips -z 630 1200 "$OUT" --out "$OUT" >/dev/null
cp "$OUT" og-image.png
# Keep legacy filename so old absolute URLs keep working during cache bleed.
cp "$OUT" og-release-v0.1.2.png
echo "wrote $OUT (+ og-image.png)"

#!/usr/bin/env bash
# Render og-release-v0.1.2.html → PNG via Chrome headless.
set -euo pipefail
cd "$(dirname "$0")"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
HTML="file://$(pwd)/og-release-v0.1.2.html?still=1"
OUT="$(pwd)/og-release-v0.1.2.png"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --screenshot="$OUT" "$HTML" 2>/dev/null
sips -z 630 1200 "$OUT" --out "$OUT" >/dev/null
cp "$OUT" og-image.png
echo "wrote $OUT"

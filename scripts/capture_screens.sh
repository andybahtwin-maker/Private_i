#!/usr/bin/env bash
set -euo pipefail
OUT=./captures
mkdir -p "$OUT"
curl -fsS http://localhost:5005/shot.jpg -o "$OUT/shot.jpg"
curl -fsS http://localhost:5005/annotated.jpg -o "$OUT/annotated.jpg"
curl -fsS http://localhost:5005/summary.json -o "$OUT/summary.json"
echo "[ok] Wrote $OUT/shot.jpg, $OUT/annotated.jpg, $OUT/summary.json"

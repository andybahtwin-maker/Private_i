#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p models

PT=models/MobileNetSSD_deploy.prototxt
CM=models/MobileNetSSD_deploy.caffemodel

# Prototxt (same as before)
if [ ! -f "$PT" ]; then
  echo "[i] fetching prototxt…"
  wget -O "$PT" \
    https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/deploy/MobileNetSSD_deploy.prototxt
fi

# Caffemodel (use raw.githubusercontent.com)
if [ ! -f "$CM" ]; then
  echo "[i] fetching caffemodel…"
  set +e
  wget -O "$CM" \
    https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.caffemodel
  rc=$?
  set -e
  if [ $rc -ne 0 ] || [ ! -s "$CM" ]; then
    echo "[!] Primary URL failed. If this repeats, ping me and we’ll swap to a different lightweight model (e.g., YOLOv8n)."
    exit 1
  fi
fi

echo "[ok] Models present in ./models"

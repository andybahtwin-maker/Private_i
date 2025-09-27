#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
./scripts/fetch_models.sh
echo "[i] Using .env:"
grep -v '^\s*$\|^\s*#' .env || true
python app.py

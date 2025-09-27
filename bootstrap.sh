#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/andhe001/projects/ai_cam_node"
cd "$ROOT"

# Python deps
cat <<'PKG' > requirements.txt
flask==3.0.3
requests==2.32.3
numpy==1.26.4
opencv-python-headless==4.10.0.84
python-dotenv==1.0.1
PKG

# Example .env
cat <<'ENV' > .env.example
# Your Android IP Webcam base URL (no trailing slash)
CAMERA_URL=http://192.168.30.106:8080
ANALYZE_EVERY=2
HOST=0.0.0.0
PORT=5005
ENV

cp .env.example .env

# Git hygiene
cat <<'GIT' > .gitignore
__pycache__/
*.pyc
.venv/
.env
.DS_Store
GIT

mkdir -p scripts models

# Model fetch script
cat <<'FM' > scripts/fetch_models.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p models
PT=models/MobileNetSSD_deploy.prototxt
CM=models/MobileNetSSD_deploy.caffemodel
[ -f "$PT" ] || wget -O "$PT" https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/deploy/MobileNetSSD_deploy.prototxt
[ -f "$CM" ] || wget -O "$CM" https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel
echo "[ok] Models present in ./models"
FM
chmod +x scripts/fetch_models.sh

# Run script
cat <<'RUN' > scripts/dev_run.sh
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
RUN
chmod +x scripts/dev_run.sh

echo "[ok] Project scaffold ready at $ROOT"
echo "Next steps:"
echo "  1) Edit .env to set your CAMERA_URL"
echo "  2) Run: ./scripts/dev_run.sh"

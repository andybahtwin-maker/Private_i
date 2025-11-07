# 🕵️‍♂️ Private_i — IP Webcam → Edge AI Camera Node

**Private_i** turns any Android phone running **IP Webcam** into a self-contained **AI camera node**.  
It pulls frames from your phone (`/shot.jpg`), runs **MobileNet-SSD** locally (CPU) via OpenCV’s DNN, and serves a **Flask dashboard** with annotated video, live JSON summaries, and machine-readable endpoints.  
It’s a working demo of *“phone → edge inference → web UI → JSON API.”*

---

## 🚀 What It Does
- 📷 Pulls frames from an Android IP Webcam (`CAMERA_URL` in `.env`)
- 🧠 Runs **MobileNet-SSD** object detection (`person`, `dog`, `bottle`, `car`, etc.)
- 🗣️ Generates sentences like: `I currently see 2 people, 1 bottle.`
- 🌐 Serves a live dashboard (`/`) plus machine endpoints:
  - `/health`
  - `/summary.json`
  - `/shot.jpg`
  - `/annotated.jpg`
  - `/video` (MJPEG stream)
- 💾 Includes capture + bootstrap scripts
- 🧩 Stores examples in `captures/` for easy portfolio embedding

---

## 📁 Repo Layout

Private_i/
├── app.py # Flask app + detection + dashboard
├── requirements.txt # Flask, OpenCV, requests, numpy, dotenv
├── .env.example # CAMERA_URL, PORT, refresh interval
├── scripts/
│ ├── dev_run.sh # create venv, install deps, run app
│ ├── fetch_models.sh # download MobileNetSSD model
│ └── capture_screens.sh # save annotated frames + JSON → captures/
├── models/
│ ├── MobileNetSSD_deploy.prototxt
│ └── MobileNetSSD_deploy.caffemodel
├── captures/ # sample screenshots + summaries
│ ├── shot.jpg
│ ├── annotated.jpg
│ └── summary.json
└── bootstrap.sh # legacy setup script


---

## ⚙️ Setup & Run
```bash
git clone https://github.com/your-username/Private_i.git
cd Private_i
./scripts/dev_run.sh

That script:

    creates .venv

    installs dependencies

    fetches models if missing

    starts python app.py

Then visit:

http://localhost:5005/

Or configure manually:

cat <<'ENV' > .env
CAMERA_URL=http://192.168.0.42:8080
ANALYZE_EVERY=2
HOST=0.0.0.0
PORT=5005
ENV

🧠 How It Works
Stage	Description
1. Frame grab	pulls /shot.jpg from CAMERA_URL
2. Detection	MobileNet-SSD DNN infers every few seconds
3. Annotation	draws boxes + labels using OpenCV
4. State	keeps latest frame + summary in memory
5. Presentation	Flask dashboard + REST endpoints
🧩 Endpoints

    / — auto-refreshing dashboard

    /health — quick status JSON

    /summary.json — counts + English summary

    /shot.jpg — raw current frame

    /annotated.jpg — frame with boxes

    /video — MJPEG stream (auto-fallback if camera stream fails)

Example:

{
  "timestamp": 1730950000.123,
  "counts": { "person": 2, "bottle": 1 },
  "english": "I currently see 2 people, 1 bottle.",
  "camera": "http://192.168.0.42:8080"
}

🧪 Capture Evidence

Regenerate static captures for your portfolio:

./scripts/capture_screens.sh

🛠️ Model Fetching

If missing:

./scripts/fetch_models.sh

Downloads:

    models/MobileNetSSD_deploy.prototxt

    models/MobileNetSSD_deploy.caffemodel

🧑‍💻 Requirements

flask==3.0.3
requests==2.32.3
numpy==1.26.4
opencv-python-headless==4.10.0.84
python-dotenv==1.0.1

💡 Portfolio Framing

Private_i demonstrates end-to-end edge AI:

    runs on CPU with no GPU

    turns any phone into a visual sensor

    exposes clean endpoints for other apps (e.g. Jarvis or dashboards)

    small enough to demo live in interviews

It’s your “real-time computer-vision node” — fast, portable, and entirely local.
🪪 License

MIT — free to fork, modify, and deploy.

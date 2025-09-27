#!/usr/bin/env python3
import os, time, threading, io, requests, json
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, send_file, render_template_string
import cv2, numpy as np

load_dotenv()
CAMERA_URL   = os.getenv("CAMERA_URL", "http://127.0.0.1:8080").rstrip("/")
ANALYZE_EVERY= float(os.getenv("ANALYZE_EVERY", "2"))
HOST         = os.getenv("HOST", "0.0.0.0")
PORT         = int(os.getenv("PORT", "5005"))
PTX_PATH     = "models/MobileNetSSD_deploy.prototxt"
CAFFEM_PATH  = "models/MobileNetSSD_deploy.caffemodel"

CLASSES = ["background","aeroplane","bicycle","bird","boat","bottle","bus","car","cat",
           "chair","cow","diningtable","dog","horse","motorbike","person","pottedplant",
           "sheep","sofa","train","tvmonitor"]

# Load model (fail fast with nice message)
if not (os.path.exists(PTX_PATH) and os.path.exists(CAFFEM_PATH)):
    raise SystemExit("[!] Missing model files. Run: ./scripts/fetch_models.sh")
net = cv2.dnn.readNetFromCaffe(PTX_PATH, CAFFEM_PATH)

last_frame = None
last_summary = {"timestamp": 0, "counts": {}, "detections": []}

app = Flask(__name__)

def grab_frame() -> np.ndarray:
    r = requests.get(f"{CAMERA_URL}/shot.jpg", timeout=5)
    r.raise_for_status()
    data = np.frombuffer(r.content, dtype=np.uint8)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if frame is None:
        raise RuntimeError("decode failed")
    return frame

def analyze_frame(frame: np.ndarray):
    global last_summary
    (h,w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)), 0.007843,(300,300),127.5)
    net.setInput(blob)
    dets = net.forward()
    counts, detections = {}, []
    for i in range(dets.shape[2]):
        conf = float(dets[0,0,i,2])
        if conf < 0.5: continue
        idx = int(dets[0,0,i,1])
        label = CLASSES[idx] if 0 <= idx < len(CLASSES) else f"id{idx}"
        counts[label] = counts.get(label, 0) + 1
        x1,y1,x2,y2 = (dets[0,0,i,3:7] * np.array([w,h,w,h])).astype(int)
        detections.append({"label":label,"conf":round(conf,2),"box":[int(x1),int(y1),int(x2),int(y2)]})
    last_summary = {"timestamp": time.time(), "counts": counts, "detections": detections}

def english_summary(summary: dict) -> str:
    if not summary["counts"]:
        return "No notable objects detected."
    parts=[]
    for k,v in sorted(summary["counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        name = "people" if k=="person" and v>1 else ("person" if k=="person" else k)
        parts.append(f"{v} {name}")
    return "I currently see " + ", ".join(parts) + "."

def mjpeg_generator():
    # Try native MJPEG first
    try:
        with requests.get(f"{CAMERA_URL}/video", stream=True, timeout=5) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: yield chunk
            return
    except Exception:
        pass
    # Fallback: roll our own from snapshots
    while True:
        try:
            frame = grab_frame()
            ok, buf = cv2.imencode(".jpg", frame)
            if not ok: raise RuntimeError("encode failed")
            jpg = buf.tobytes()
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n")
            time.sleep(0.15)
        except Exception:
            time.sleep(0.5)

def analyzer_loop():
    global last_frame
    while True:
        try:
            frame = grab_frame()
            last_frame = frame
            if (time.time() - last_summary["timestamp"]) > ANALYZE_EVERY:
                analyze_frame(frame)
        except Exception:
            time.sleep(0.5)

DASHBOARD_HTML = """
<!doctype html><html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Cam Node</title>
<style>
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:24px}
.wrap{display:grid;gap:16px;grid-template-columns:1fr;max-width:980px}
.card{border:1px solid #ddd;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
img,video{max-width:100%;border-radius:8px}
.summary{font-size:1.1rem}.muted{color:#666;font-size:.9rem}code{background:#f5f5f5;padding:2px 6px;border-radius:6px}
</style></head><body><div class="wrap">
<div class="card"><h2>Live Feed</h2><img id="feed" src="/video" alt="Live video"/>
<div class="muted">If you see nothing, verify IP Webcam is running & CAMERA_URL in <code>.env</code>.</div></div>
<div class="card"><h2>AI Summary</h2><div id="summary" class="summary">Loading…</div>
<div class="muted">Updates every {{interval}}s • <code>/summary.json</code> • snapshot: <a href="/shot.jpg">/shot.jpg</a></div></div>
</div>
<script>
async function refresh(){try{const r=await fetch('/summary.json');const j=await r.json();document.getElementById('summary').textContent=j.english;}catch(e){document.getElementById('summary').textContent='No summary yet.'}}
setInterval(refresh, {{interval}}*1000);refresh();
</script></body></html>
"""

@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML, interval=int(ANALYZE_EVERY))

@app.route("/summary.json")
def summary_json():
    return jsonify({
        "ts": last_summary["timestamp"],
        "counts": last_summary["counts"],
        "detections": last_summary["detections"],
        "english": english_summary(last_summary)
    })

@app.route("/shot.jpg")
def shot_jpg():
    global last_frame
    frame = last_frame
    if frame is None:
        try: frame = grab_frame()
        except Exception: return ("", 204)
    ok, buf = cv2.imencode(".jpg", frame)
    if not ok: return ("", 204)
    return send_file(io.BytesIO(buf.tobytes()), mimetype="image/jpeg")

@app.route("/video")
def video():
    return Response(mjpeg_generator(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    threading.Thread(target=analyzer_loop, daemon=True).start()
    app.run(host=HOST, port=PORT, threaded=True)

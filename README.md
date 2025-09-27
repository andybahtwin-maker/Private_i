
## Why this matters (portfolio)
- **Android → IP Webcam → Flask UI**: turns a phone into an AI camera node.
- **Edge AI** (CPU): MobileNet-SSD detects people/objects; live English summary at `/summary.json`.
- **Embeddable demo**: UI/frames/json can be embedded in Notion (token-gated).
- **Endpoints**: `/` · `/video` · `/shot.jpg` · `/annotated.jpg` · `/summary.json` · `/health`

**Run locally:** `./scripts/dev_run.sh` then open `http://localhost:5005/?token=YOURTOKEN`

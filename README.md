# 🕵️‍♂️ Private_i — Personal Intelligence Desk

**Private_i** is a lightweight, local-first intelligence console for tracking fast-changing information — companies, roles, markets, and opportunities — in one place.  
It unifies the data-ingestion, normalization, and visualization layers from your other projects into a single control panel that runs anywhere.

---

## 🚀 Quick Overview
**Private_i** is not just a scraper.  
It’s an *intake → normalize → snapshot → visualize* pipeline for your personal intelligence.

Think of it as a **self-hosted “inbox for signals”**: run it, let it collect from multiple feeds, and browse results from one dashboard.

---

## 📁 Project Structure

private_i/
├── README.md # Documentation (this file)
├── run_all.sh # Full pipeline runner
├── app.py # Streamlit dashboard
├── ingest_sources.py # Fetch and merge external feeds
├── process_intel.py # Clean, tag, and score items
├── snapshot_store.py # Store results in /data
├── notion_sync.py # Optional Notion integration
├── config/ # Source and tagging configuration
│ └── sources.yaml
├── data/ # Local caches & historical snapshots
├── secrets/ # .env with API keys (ignored by git)
└── scripts/ # Operator scripts (publish, clean, demo)


---

## ⚙️ Installation
```bash
git clone https://github.com/your-username/private_i.git
cd private_i
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a file at secrets/.env:

NOTION_API_KEY=your_key_here
OPENAI_API_KEY=optional_here
SLACK_WEBHOOK_URL=optional_here
PRIMARY_FEEDS=remotive,lever,greenhouse

Then run:

chmod +x run_all.sh
./run_all.sh

🧠 How It Works
Stage	Description
1. Ingest	Pulls data from sources defined in config/sources.yaml
2. Process	Cleans titles, tags keywords (e.g. SE, AI, Remote)
3. Snapshot	Saves latest run in /data for comparison
4. Visualize	Displays interactive tables & filters in Streamlit
5. Publish	(Optional) Syncs results to Notion for daily review
🪄 Features

    🔎 Multi-source intake — aggregate jobs or market data from several feeds

    🏷️ Smart tagging — apply SE/AI/remote labels automatically

    📦 Local snapshots — keep historical JSON/CSV runs

    📊 Dashboard view — filter and explore your data visually

    🗒️ Notion sync (optional) — export curated results

    🤖 AI summaries (optional) — GPT-based daily insights

    🛠️ Automation scripts — one-command demos & publish routines

🧰 Example Usage

# Run full pipeline
./run_all.sh

# Fetch only
python ingest_sources.py

# Open dashboard
streamlit run app.py

# Sync to Notion
python notion_sync.py

🧩 Integrations

    Notion API — export top results to your workspace

    OpenAI API — summarize new signals automatically

    Local filesystem — all data stays private and offline

    Streamlit — dashboard UI for review

💡 Example Scenarios

    Daily prospect / job review from multiple feeds

    Competitive tracking for target companies

    Personal SE pipeline and opportunity filtering

    Portfolio demo showing full-stack data orchestration

🧑‍💻 Development Notes

    Language: Python 3.11+

    Frameworks: Streamlit + Pandas

    Config: YAML under config/

    Secrets: .env in secrets/

    Logging: CSV/JSON snapshots in data/

🔗 Related Projects

    Coinbase Pipeline — Crypto trading analytics dashboard

    Job Pipeline — Job ingestion + Notion sync

    UX Job Scraper (ApplyPilot Ultra) — Multi-source job finder

    Jarvis — Terminal automation powering all orchestration

🪪 License

MIT — free to fork, modify, and deploy.

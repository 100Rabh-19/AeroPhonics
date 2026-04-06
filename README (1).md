# 🌿 LeafSense — AI Plant Disease Detection

Upload a photo of a plant leaf and get an instant AI-powered diagnosis, severity assessment, and treatment recommendations.

## How it works

LeafSense uses Claude's vision model (claude-sonnet-4) to analyse leaf images and return structured diagnostics including disease name, confidence score, severity, spread risk, and recommended actions.

## Project structure

```
leafsense/
├── main.py              # FastAPI backend (proxies Anthropic API calls)
├── requirements.txt
├── render.yaml          # Render deployment config
├── .gitignore
└── static/
    └── index.html       # Frontend UI
```

## Local development

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here

# Run the server
uvicorn main:app --reload
```

Then open http://localhost:8000

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — just confirm the settings
5. Add your `ANTHROPIC_API_KEY` in the **Environment** tab
6. Click **Deploy**

## Note on the dataset

The `winnig_dataset/` folder (used in `plant_disease.ipynb`) is excluded from this repo via `.gitignore`. The deployed app uses Claude's vision model directly and does not require the local dataset.

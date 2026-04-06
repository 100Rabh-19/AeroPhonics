import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="LeafSense API")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

class AnalyseRequest(BaseModel):
    image_base64: str
    media_type: str = "image/jpeg"

@app.post("/api/analyse")
async def analyse(req: AnalyseRequest):
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    prompt = """You are a world-class plant pathologist. Analyse this plant leaf image carefully and respond ONLY with a valid JSON object — no markdown fences, no preamble, just raw JSON:
{
  "disease": "Common disease name or 'Healthy Plant'",
  "scientific": "Pathogen scientific name or 'N/A'",
  "confidence": <integer 0-100>,
  "severity": "None | Mild | Moderate | Severe",
  "spread_risk": "Low | Medium | High",
  "is_healthy": <true|false>,
  "not_a_leaf": <true|false>,
  "description": "2-3 sentence clinical description of what you observe",
  "treatments": ["action 1", "action 2", "action 3"]
}
If the image does not show a plant leaf, set not_a_leaf to true."""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": req.media_type,
                        "data": req.image_base64
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json=payload
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Upstream API error")

    data = resp.json()
    raw = (data.get("content", [{}])[0].get("text", "{}"))
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse model response")

@app.get("/health")
def health():
    return {"status": "ok"}

# Serve frontend — must be LAST so it doesn't catch API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")

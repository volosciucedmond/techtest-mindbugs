import requests
import logging
import json

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://ollama:11434"
MODEL_NAME = "llama3.2:1b"

EXTRACTION_PROMPT = """[INST] <<SYS>>
Extract key highlights and pain points from the review.
Rules:
- Output ONLY short 2-4 word phrases (e.g., "Clean room", "Slow check-in").
- Do not output nested dictionaries.
<</SYS>>

Review: "{review}"

Return EXACTLY this JSON format:
{{
  "highlights": ["phrase 1", "phrase 2"],
  "pain_points": ["phrase 1"]
}}
[/INST]"""

def extract_insights(review: str) -> dict:    
    prompt = EXTRACTION_PROMPT.format(review=review)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json" 
    }
    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        raw_text = response.json().get("response", "")
        parsed = json.loads(raw_text)
        return {
            "highlights": parsed.get("highlights", []),
            "pain_points": parsed.get("pain_points", [])
        }
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return {"highlights": [], "pain_points": []}
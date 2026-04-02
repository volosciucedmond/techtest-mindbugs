# LLM extraction logic using Ollama

import requests
import logging
import json

logger = logging.getLogger(__name__)

# local Ollama endpoint
OLLAMA_BASE_URL = "http://ollama:11434"

# using the 1B model to keep inference fast and memory-efficiency
MODEL_NAME = "llama3.2:1b"

# strict prompt to force the LLM to output clean, structred JSON
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
    # inject the text into the predefined template
    prompt = EXTRACTION_PROMPT.format(review=review)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False, # returns full response at once instead of word by word
        "format": "json" # forces the model to output JSON
    }
    try:
        # long timeout to allow for a slower model startup
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        
        # pull the text out of the Ollama response wrapper
        raw_text = response.json().get("response", "")
        parsed = json.loads(raw_text)
        
        # return structured data or empty lists if keys are missing
        return {
            "highlights": parsed.get("highlights", []),
            "pain_points": parsed.get("pain_points", [])
        }
    except Exception as e:
        # graceful failure: if the LLM hallucinates or the API is down, return empty results
        logger.error(f"Extraction failed: {e}")
        return {"highlights": [], "pain_points": []}
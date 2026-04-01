import requests
import logging

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://ollama:11434"

def extract_insights(review: str) -> dict:
    """ Simple llm extaraction """
    
    prompt = f"Identify the positives and negatives in this otel review: {review}"
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
    
    # basic request
    response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
    result = response.json().get("response", "")
    
    # return a dummy structure
    return {
        "highlights": [result],
        "pain_points": []
    }
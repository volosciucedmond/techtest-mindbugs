import logging
from app.llm import extract_insights

logger = logging.getLogger(__name__)

def process_reviews(reviews: list[str]) -> dict:
    all_highlights = []
    all_pain_points = []
    
    for idx, review in enumerate(reviews):
        logger.info(f"Processing review {idx + 1}/{len(reviews)}")
        insights = extract_insights(review)
        
        all_highlights.extend(insights.get("highlights", []))
        all_pain_points.extend(insights.get("pain_points", []))
        
    # return a raw list
    return {
        "highlights": [{"item": h, "count": 1} for h in all_highlights],
        "pain_points": [{"item": p, "count": 1} for p in all_pain_points]
    }
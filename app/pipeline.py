import logging
from app.llm import extract_insights

logger = logging.getLogger(__name__)

def process_reviews(reviews: list[str]) -> dict:
    """ simple pipeline that just extracts and collects all insights """
    
    all_highlights = []
    all_pain_points = []
    
    for idx, review in enumerate(reviews):
        logger.info(f"Processing review {idx + 1}/{len(reviews)}")
        insights = extract_insights(review)
        
        all_highlights.extend(insights.get("highlights", []))
        all_pain_points.extend(insights.get("pain_points", []))
        
    # return a raw list
    return {
        "highlights": all_highlights,
        "pain_points": all_pain_points
    }
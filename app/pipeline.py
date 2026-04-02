# LLM extraction and semantic clustering

import logging
from app.llm import extract_insights
from app.embeddings import deduplicate

logger = logging.getLogger(__name__)

def process_reviews(reviews: list[str]) -> dict:
    # containers to gather all the raw signal before deduplication
    all_highlights = []
    all_pain_points = []
    
    for idx, review in enumerate(reviews):
        # tracking progress in the logic
        logger.info(f"[{idx + 1}/{len(reviews)}] Extracting insights...")
        insights = extract_insights(review)
        
        h_val = insights.get("highlights", [])
        p_val = insights.get("pain_points", [])
        
        # Simple, readable loops that ignore hallucinated dictionaries
        for h in h_val:
            if isinstance(h, str): 
                all_highlights.append(h)
                
        for p in p_val:
            if isinstance(p, str): 
                all_pain_points.append(p)
        
    logger.info("Starting semantic deduplication...")
    
    # final output to merge similar data points
    return {
        "highlights": deduplicate(all_highlights),
        "pain_points": deduplicate(all_pain_points)
    }
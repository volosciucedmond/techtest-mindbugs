import os
import logging
from fastapi import FastAPI, HTTPException
from app.pipeline import process_reviews

# basic logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI isntance, automatically generates Swagger UI
app = FastAPI(
    title="Hotel Review Intelligence System",
    description="Extract and deduplicates insights from hotel reviews",
)

# pulls file path from environment
REVIEWS_FILE_PATH = os.getenv("REVIEWS_FILE_PATH", "data/reviews.txt")

app.get("/health")
def health_check():
    # Simple endpoint to verify API
    return {"status": "ok"}

@app.post("/process_file")
def process_file():
    # Reads the txt file, extracts insights using LLM, deduplicates them, and returns the final structured report
    
    if not os.path.exists(REVIEWS_FILE_PATH):
        raise HTTPException(
            status_code=404, 
            detail=f"Reviews file not found at {REVIEWS_FILE_PATH}"
        )
        
    # read reviews, stripping whitespace and ignoring empty lines    
    with open(REVIEWS_FILE_PATH, "r", encoding="utf-8") as f:
        reviews = [line.strip() for line in f if line.strip()]
    
    # early exit if the soruce file is empty
    if not reviews:
        raise HTTPException(
            status_code=400, 
            detail="No reviews found in the file."
        )
        
    logger.info(f"Processing {len(reviews)} reviews from {REVIEWS_FILE_PATH}...")
    
    
    result = process_reviews(reviews)
    logger.info("Processing completed successfully.")
    return result

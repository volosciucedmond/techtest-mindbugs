import os
import logging
from fastapi import FastAPI

# basic logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hotel Review Intelligence System",
    description="Extract and deduplicates insights from hotel reviews",
)

@app.get("/health")
def health_check():
    """ Simple endpoint to verify API"""
    return {"status": "ok"}
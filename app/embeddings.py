# embedding generation and cosine similarity deduplication logic

import logging
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# fast, small model good for real time inference
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
SIMILIARITY_THRESHOLD = 0.8

# global variable
_model: SentenceTransformer | None = None

def get_model() -> SentenceTransformer:
    # loads the model only once and reuses it
    global _model
    if _model is None:
        logger.info(f"Loading embedding model '{EMBEDDING_MODEL_NAME}'...")
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    # calculates how similar two vecotrs are
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

def deduplicate(items: list[str]) -> list[dict]:
    # groups similar phrases and returns a count
    if not items:
        return []
    
    cleaned = [i.lower().replace("the ", "").replace(".", "").strip() for i in items]
    
    model = get_model()
    logger.info(f"Generating embeddings for {len(items)} items...")
    
    embeddings = model.encode(cleaned, convert_to_numpy=True)
    
    assigned = [False] * len(items)
    groups: list[dict] = []
    
    for i in range(len(items)):
        if assigned[i]:
            continue
        
        # start new cluster
        cluster_indices =[i]
        assigned[i] = True
        
        # expand cluster 
        for j in range(i + 1, len(items)):
            if assigned[j]:
                continue
            
            # check siilarity 
            is_similar = False
            for k in cluster_indices:
                sim = cosine_similarity(embeddings[k], embeddings[j])
                if sim >= SIMILIARITY_THRESHOLD:
                    is_similar = True
                    break
            
            if is_similar:
                cluster_indices.append(j)
                assigned[j] = True
                logger.debug(f"Merged '{items[j]}' into cluster with '{items[i]}'")
                
        # build group
        cluster_items = [items[idx] for idx in cluster_indices]
        
        # choose representative phrase 
        representative = cluster_items[0]
        
        groups.append({
            "item": representative,
            "count": len(cluster_items)
        })
    
    return groups
        
                    
    
    
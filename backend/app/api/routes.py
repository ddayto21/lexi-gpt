# app/api/routes.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas.search_books import SearchRequest, SearchResponse

from app.services.profanity import contains_profanity
from sentence_transformers import SentenceTransformer

from app.services.semantic_search import (
    create_vector_embedding,
    calculate_similarity_scores,
    get_top_k_books,
)
import json
import redis
import logging
import numpy as np
import torch


# Initialize router
router = APIRouter()


# Redis Client Setup
def get_redis_client():
    try:
        client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        client.ping()
        return client
    except redis.exceptions.ConnectionError:

        class DummyRedis:
            def get(self, key):
                return None

            def setex(self, key, ttl, value):
                pass

        return DummyRedis()


redis_client = get_redis_client()


@router.post("/search_books", response_model=SearchResponse)
async def search_books(request: Request, payload: SearchRequest):
    """Handles book search queries using semantic similarity."""

    query = payload.query.strip().lower()
    logging.info(f"Processing search query: '{query}'")

    # Profanity Filter
    if contains_profanity(query):
        raise HTTPException(status_code=403, detail="Profanity is not allowed.")

    # Ensure model & device are available
    model = getattr(request.app.state, "model", None)
    device = getattr(request.app.state, "device", "cpu")

    if model is None:
        logging.error("Model is not loaded in application state.")
        raise HTTPException(
            status_code=500, detail="Server error: Model not initialized."
        )

    # Ensure book embeddings & metadata are available
    document_embeddings = getattr(request.app.state, "document_embeddings", None)
    books_metadata = getattr(request.app.state, "books_metadata", None)

    if document_embeddings is None or books_metadata is None:
        logging.error("Book embeddings or metadata are not loaded.")
        raise HTTPException(
            status_code=500, detail="Server error: Book data not available."
        )

    # Check Redis cache
    cache_key = f"books:{query}"
    cached_results = redis_client.get(cache_key)
    if cached_results:
        logging.info("Cache hit: Returning cached search results.")
        return JSONResponse(content=json.loads(cached_results))

    # Ensure embeddings and metadata are loaded
    if document_embeddings is None or books_metadata is None:
        logging.error("Book embeddings or metadata are not loaded.")
        raise HTTPException(
            status_code=500, detail="Server error: book data not available."
        )

    try:
        # Generate query embedding
        query_embedding = create_vector_embedding(model, query, device)

        # Compute similarity scores
        similarity_scores = calculate_similarity_scores(
            query_embedding, document_embeddings
        )

        # Retrieve top 5 recommended books
        top_books = get_top_k_books(similarity_scores, books_metadata, k=5)

        # Cache results in Redis (1-hour expiration)
        redis_client.setex(cache_key, 3600, json.dumps(top_books))

        logging.info(f"Returning top {len(top_books)} books for query '{query}'")

        return JSONResponse(content=jsonable_encoder(top_books))

    except Exception as e:
        logging.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your request."
        )

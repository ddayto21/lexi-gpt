# app/api/routes.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas.search_books import Book, SearchRequest, SearchResponse

from app.services.profanity import contains_profanity
from sentence_transformers import SentenceTransformer

from app.services.semantic_search import (
    load_book_embeddings,
    load_books_metadata,
    create_vector_embedding,
    calculate_similarity_scores,
    get_top_k_books,
)
import json
import redis
import logging
import numpy as np
import torch
from pathlib import Path


router = APIRouter()

# Load embeddings and metadata once during startup
BASE_DIR = Path(__file__).resolve().parent.parent.parent
EMBEDDINGS_FILE = BASE_DIR / "app" / "data" / "book_metadata" / "embedding_outputs.json"
BOOKS_METADATA_FILE = (
    BASE_DIR / "app" / "data" / "book_metadata" / "books_metadata.json"
)

logging.info("Loading book embeddings and metadata into memory...")
try:
    document_embeddings = load_book_embeddings(str(EMBEDDINGS_FILE))
    books_metadata = load_books_metadata(str(BOOKS_METADATA_FILE))
    logging.info(f"Successfully loaded {len(books_metadata)} books and embeddings.")
except Exception as e:
    logging.error(f"Failed to load book embeddings or metadata: {e}")
    document_embeddings, books_metadata = None, None

# Load SentenceTransformer model
logging.info("Initializing SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")


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


@router.post("/search_books")
async def search_books(request: Request, payload: SearchRequest):
    query = payload.query.strip().lower()
    logging.info(f"Received search query: {query}")

    if contains_profanity(query):
        raise HTTPException(status_code=403, detail="Profanity is not allowed.")

    # Check Redis cache
    cache_key = f"books:{query}"
    # Check Redis cache
    cached_results = redis_client.get(f"books:{query}")
    if cached_results:
        return SearchResponse(recommendations=json.loads(cached_results))

    # Ensure embeddings and metadata are loaded
    if document_embeddings is None or books_metadata is None:
        raise HTTPException(
            status_code=500, detail="Server error: book data not loaded."
        )

    # Generate query embedding
    query_embedding = create_vector_embedding(model, query, device)

    # Compute similarity scores
    similarity_scores = calculate_similarity_scores(
        query_embedding, document_embeddings
    )

    # Retrieve top 5 recommended books
    top_books = get_top_k_books(similarity_scores, books_metadata, k=5)
    print("Top books:", top_books)
    # Cache results
    redis_client.setex(cache_key, 3600, json.dumps(top_books))

    logging.info(f"Top recommended books: {[book['title'] for book in top_books]}")
    
    json_compatible_item_data = jsonable_encoder(top_books)
    return JSONResponse(content=json_compatible_item_data)

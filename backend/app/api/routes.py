# app/api/routes.py

from fastapi import APIRouter, Request, HTTPException
from app.schemas.search_books import SearchRequest, SearchResponse
from app.services.book_processor import process_results
from app.services.profanity import contains_profanity
import json
import redis


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
router = APIRouter()


@router.post("/search_books", response_model=SearchResponse)
async def search_books(request: Request, payload: SearchRequest):

    query = payload.query.strip().lower()
    print(f"Received query: {query}")

    if contains_profanity(query):
        raise HTTPException(status_code=403, detail="Profanity is not allowed.")

    # 1) Check Redis cache
    cached_results = redis_client.get(f"books:{query}")
    if cached_results:
        # The cache should store already-processed results
        return SearchResponse(recommendations=json.loads(cached_results))

    llm_client = request.app.state.llm_client

    # 2) The LLM client returns (refined_query, raw_docs)
    refined_query, raw_docs = await llm_client.process_query(query)

    # 4) Process the raw docs into proper shape (title, authors, description)
    processed_books = process_results({"docs": raw_docs})
    print("processed_books:", processed_books)

    # 5) Cache the processed results
    redis_client.setex(
        f"books:{query}", 3600, json.dumps([b.dict() for b in processed_books])
    )

    # 6) Return books in correct shape for SearchResponse
    return SearchResponse(recommendations=processed_books)

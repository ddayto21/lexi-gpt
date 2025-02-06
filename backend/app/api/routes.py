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

    # Check Redis cache
    cached_results = redis_client.get(f"books:{query}")
    if cached_results:
        return SearchResponse(recommendations=json.loads(cached_results))

    # Retrieve clients from the app state.
    open_library_client = request.app.state.open_library_client
    llm_client = request.app.state.llm_client

    # Await the extraction of keywords.
    keywords = await llm_client.extract_keywords(query)
    print("Extracted keywords:", keywords)

    # Search OpenLibrary with the refined keywords.
    search_results = await open_library_client.search(keywords)
    print("Search results:", search_results)
    books = search_results.get("docs", [])
    print("Books:", books)

    # Process raw OpenLibrary docs into the proper book format.
    processed_books = process_results({"docs": books})
    print("Processed books:", processed_books)

    # Optionally, you can cache processed_books here.

    return SearchResponse(recommendations=processed_books)

from fastapi import APIRouter, Request, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
import os

from app.schemas.search_books import SearchRequest, SearchResponse
from app.services.book_processor import process_results
from app.services.profanity import contains_profanity


public_router = APIRouter()


@public_router.post("/search_books", response_model=SearchResponse)
async def search_books(request: Request, payload: SearchRequest):
    if contains_profanity(payload.query):
        raise HTTPException(
            status_code=403,
            detail="The Book Search service is moderated and does not allow for profanity.",
        )

    refined_query = await request.app.state.llm_client.refine_query(payload.query)
    results = await request.app.state.open_library_client.search(refined_query)

    books_data = process_results(results)
    enhanced_data = await request.app.state.llm_client.enhance_book_descriptions(
        books_data
    )

    return SearchResponse(recommendations=enhanced_data)


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("INTERNAL_API_KEY"):
        raise HTTPException(status_code=403, detail="Not authorized")
    return api_key


internal_router = APIRouter()


@internal_router.post("/llm/refine", dependencies=[Depends(get_api_key)])
async def refine_query_endpoint(query: str):
    # Replace with actual logic for refining a query via LLM
    return {"refined_query": "example refined query"}


@internal_router.post("/llm/enhance", dependencies=[Depends(get_api_key)])
async def enhance_books_endpoint(books: list):
    # Replace with actual logic for enhancing book data via LLM
    return {"enhanced_books": books}

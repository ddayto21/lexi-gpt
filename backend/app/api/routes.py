from fastapi import APIRouter, Request, HTTPException, Depends, Security, Body
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

    # Call the LLM to refine the query
    refined_query = await request.app.state.llm_client.refine_query(payload.query)
    # Search OpenLibrary using the refined query
    results = await request.app.state.open_library_client.search(refined_query)
    # Process the raw search results into a list of book dicts
    books_data = process_results(results)
    # Enhance the book data with the LLM
    enhanced_data = await request.app.state.llm_client.enhance_book_descriptions(books_data)

    return SearchResponse(recommendations=enhanced_data)

# Security dependency for internal endpoints
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("INTERNAL_API_KEY"):
        raise HTTPException(status_code=403, detail="Not authorized")
    return api_key

internal_router = APIRouter()

@internal_router.post("/llm/refine", dependencies=[Depends(get_api_key)])
async def refine_query_endpoint(payload: dict = Body(...)):
    """
    Expects a JSON payload like: {"query": "some query"}
    For now, returns a simple refined query.
    """
    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing 'query' field")
    # In a real scenario, call the LLM service logic here.
    return {"refined_query": f"{query} refined"}

@internal_router.post("/llm/enhance", dependencies=[Depends(get_api_key)])
async def enhance_books_endpoint(books: list = Body(...)):
    """
    Expects a bare JSON array (list) of books.
    For now, simply returns them wrapped in an "enhanced_books" key.
    """
    # In a real scenario, enhance the books data using the LLM.
    return {"enhanced_books": books}
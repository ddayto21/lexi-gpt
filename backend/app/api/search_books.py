from fastapi import APIRouter, HTTPException
from app.models.query import QueryRequest
from app.models.book import Book
from app.services.openlibrary import fetch_books
from app.services.llm import enhance_results

router = APIRouter()

@router.post("/search-books", response_model=list[Book])
async def search_books(request: QueryRequest):
    """
    Handles book search requests.
    1. Processes the query with LLM.
    2. Fetches books from OpenLibrary.
    3. Enhances the results using LLM.
    """
    try:
        # Step 1: Process the query with LLM
        processed_query = await enhance_results(request.query)

        # Step 2: Fetch books from OpenLibrary
        books = await fetch_books(processed_query)

        # Step 3: Return the enhanced book data
        return books

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
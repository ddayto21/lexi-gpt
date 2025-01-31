from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.search_books import (
    SearchBooksRequest,
    SearchBooksResponse,
    Book,
)
from app.services.openlibrary import OpenLibraryAPI


router = APIRouter()


@router.post("/", response_model=SearchBooksResponse)
async def search_books(request: SearchBooksRequest):
    # 1. Check for profanity in request.query; if found, raise 403
    if contains_profanity(request.query):
        raise HTTPException(
            status_code=403,
            detail="The Book Search service is moderated and does not allow for profanity.",
        )
    # 2. Refine the query using an LLM
    refined_query = call_llm_for_query_refinement(request.query)

    # 3. Query OpenLibrary asynchronously
    client = OpenLibraryAPI()
    results = await client.search(refined_query)

    # Extract book documents from the "book_search" key.
    book_docs = results.get("book_search", [])
    books_data = []
    for doc in book_docs:
        title = doc.get("title", "Untitled")
        authors = doc.get("author_name", [])
        # Often "description" isn't in the search document - this is an example
        description = ""
        if "first_sentence" in doc:
            first_sentence = doc["first_sentence"]
            if isinstance(first_sentence, dict):
                description = first_sentence.get("value", "")
            elif isinstance(first_sentence, str):
                description = first_sentence
        books_data.append(
            {"title": title, "authors": authors, "description": description}
        )
        # 4. Process or enhance book data with the LLM if needed
    enhanced_data = call_llm_for_book_descriptions(books_data)

    # 5. Return recommendations
    return SearchBooksResponse(recommendations=enhanced_data)


def contains_profanity(query: str) -> bool:
    # Minimal profanity check (example)
    prohibited_words = ["badword"]
    return any(word in query.lower() for word in prohibited_words)


def call_llm_for_query_refinement(query: str) -> str:

    return query


def call_llm_for_book_descriptions(books_data: List[dict]) -> List[Book]:
    # Use LLM to create natural-language descriptions for each book

    return [Book(**book) for book in books_data]

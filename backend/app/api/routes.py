from fastapi import APIRouter, Request, HTTPException
from schemas.search_books import SearchRequest, SearchResponse
from app.services.book_processor import process_results
from app.services.profanity import contains_profanity

router = APIRouter()


@router.post("/search_books", response_model=SearchResponse)
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

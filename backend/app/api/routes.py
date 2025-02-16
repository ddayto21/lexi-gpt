# app/api/routes.py

from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse

import asyncio
import time


from app.schemas.search_books import SearchRequest, SearchResponse
from app.clients.book_cache_client import BookCacheClient
from app.clients.llm_client import DeepSeekAPIClient


from app.services.profanity import contains_profanity


from app.services.semantic_search import (
    create_vector_embedding,
    calculate_similarity_scores,
    get_top_k_books,
)

from app.services.preprocessing import preprocess_book

import json
import redis
import logging
import numpy as np
import torch

# app/api/routes.py
# Create a router instance to define API endpoints.
router = APIRouter()


# -----------------------------------------------------------------------------
# Route: Search Books
# This endpoint processes user queries to find relevant books using semantic similarity.
# It leverages embeddings to understand the meaning behind the query and retrieves the most relevant books.
# -----------------------------------------------------------------------------
@router.post("/search_books")
async def search_books(request: Request, payload: SearchRequest):
    """
    Process a search query by performing semantic search over precomputed embeddings,
    then using the RAG pipeline to generate book recommendations.

    The process involves:
      1. Cleaning and validating the user query.
      2. Retrieving the language model, device, book embeddings, and metadata from application state.
      3. Checking a Redis cache for previously computed results.
      4. Running the RAG pipeline to produce a JSON array of recommendations.
    """
    # Clean the query by stripping whitespace and converting to lowercase.
    query = payload.query.strip().lower()
    logging.info(f"Processing search query: '{query}'")

    # 1. Profanity Check
    if contains_profanity(query):
        raise HTTPException(status_code=403, detail="Profanity is not allowed.")

    # 2. Retrieve Model and Device from the application state
    model = getattr(request.app.state, "model", None)
    device = getattr(request.app.state, "device", "cpu")
    if model is None:
        logging.error("Model is not loaded in application state.")
        raise HTTPException(
            status_code=500, detail="Server error: Model not initialized."
        )

    # 3. Retrieve precomputed book embeddings and metadata from application state.
    document_embeddings = getattr(request.app.state, "document_embeddings", None)
    books_metadata = getattr(request.app.state, "books_metadata", None)

    if document_embeddings is None or books_metadata is None:
        logging.error("Book embeddings or metadata are not loaded.")
        raise HTTPException(
            status_code=500, detail="Server error: Book data not available."
        )

    # 3. Retrieve Book Embeddings & Metadata
    document_embeddings = getattr(request.app.state, "document_embeddings", None)
    books_metadata = getattr(request.app.state, "books_metadata", None)
    if document_embeddings is None or books_metadata is None:
        logging.error("Book data not loaded.")
        raise HTTPException(
            status_code=500, detail="Server error: Book data not available."
        )

    # 4. Check Redis Cache
    # book_cache: BookCacheClient = request.app.state.book_cache
    # if book_cache:
    #     cache_key = f"books:{query}"
    #     cached_results = book_cache.get_books(cache_key)
    #     if cached_results:
    #         logging.info("Cache hit: Returning cached search results.")
    #         # Return immediately so no duplicate streaming occurs.
    #         return JSONResponse(content=json.loads(cached_results))
    # else:
    #     logging.warning("Redis cache client unavailable. Proceeding without caching.")

    try:
        # ---------------------------
        # 5. Generate Query Embedding and Calculate Similarity
        # ---------------------------

        # Convert the search query into an embedding vector
        query_embedding = create_vector_embedding(model, query, device)

        # Compare the query embedding against the book embeddings to compute similarity scores.
        similarity_scores = calculate_similarity_scores(
            query_embedding, document_embeddings
        )

        # 6. Retrieve Top Book Recommendations
        # Based on similarity scores, retrieve the top 5 recommended books.
        top_books = get_top_k_books(similarity_scores, books_metadata, k=5)

        # 7. Construct the LLM Prompt
        book_summaries = [preprocess_book(book) for book in top_books]
        llm_prompt = (
            f"User query: '{query}'. RAG system has retrieved relevant book details:\n\n"
            + "\n".join(
                f"{idx + 1}. {summary}" for idx, summary in enumerate(book_summaries)
            )
            + "\n\n"
            "Based on these details, provide a JSON array of book recommendations. "
            "Each recommendation should be an object with a 'title' and a 'description' that explains in clear, friendly language why the book is relevant to the query. "
            "If none of the retrieved books match the query, please generate your own recommendations based on your internal knowledge. "
            "Return only the JSON array."
        )

        # 8. Prepare LLM Client & Streaming
        llm_client = DeepSeekAPIClient()

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides book recommendations and explanations.",
            },
            {"role": "user", "content": llm_prompt},
        ]
        # print("messages:")
        # print(messages)

        # 8. Define a single streaming generator that yields chunks and then a final marker.
        async def generate():
            async for chunk in llm_client.async_stream(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
            ):
                print(chunk, end="", flush=True)
                # Yield each chunk prefixed with "data:" (SSE format).
                yield f"data: {chunk}\n\n"

        # 9. Return the StreamingResponse.
        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        logging.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your request."
        )


def event_stream():
    # Send event every second with data: "Message {i}"
    for i in range(10):
        event_str = "event: stream_event"
        data_str = f"data: Message {i}"
        yield f"{event_str}\n{data_str}\n\n"
        time.sleep(1)


@router.get("/stream")
async def stream():
    return StreamingResponse(event_stream(), media_type="text/event-stream")

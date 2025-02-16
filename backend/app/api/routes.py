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

    # 4. Check redis cache for existing results
    book_cache: BookCacheClient = request.app.state.book_cache
    if not book_cache:
        logging.warning("Redis cache client unavailable. Proceeding without caching.")
    cache_key = f"books:{query}"
    cached_results = book_cache.get_books(cache_key) if book_cache else None
    if cached_results:
        logging.info("Cache hit: Returning cached search results.")
        return JSONResponse(content=json.loads(cached_results))

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

        # ---------------------------
        #  6. Retrieve Top Book Recommendations
        # ---------------------------
        # Based on similarity scores, retrieve the top 5 recommended books.
        top_books = get_top_k_books(similarity_scores, books_metadata, k=5)

        print("top_books", top_books)

        # ---------------------------
        # 7. Construct the LLM Prompt
        # ---------------------------

        # Build a list of concise summaries for each top book.
        book_summaries = [preprocessing(book) for book in top_books]

        # Construct the prompt for the LLM.
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

        # ---------------------------
        # 8. Initialize LLM Client and Prepare Conversation History
        # ---------------------------
        llm_client = DeepSeekAPIClient()

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides book recommendations and explanations.",
            },
            {"role": "user", "content": llm_prompt},
        ]
        print("messages:")
        print(messages)

        # ------------------------------------------------
        # 9. Define the Streaming Response Generator
        # ------------------------------------------------
        async def generate():
            """
            Asynchronous generator that streams the LLM response directly in chunks.

            This method calls the LLM Client's async_stream method and yields each chunk
            as soon as it is received. The output is returned directly to the client without
            further processing or wrapping.
            """
            async for chunk in llm_client.async_stream(
                model="deepseek-chat",  # Ensure this model identifier is correct for your use case.
                messages=messages,
                temperature=0.9,
            ):
                # Optionally, print each chunk for debugging purposes.
                print(chunk, end="", flush=True)
                # Yield the chunk immediately.
                yield chunk

        # Return the StreamingResponse to the client.
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

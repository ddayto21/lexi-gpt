# app/api/routes.py
import os
import json
from fastapi import (
    FastAPI,
    APIRouter,
    Request,
    Response,
    Cookie,
    HTTPException,
    Depends,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse


import asyncio
import time


from app.schemas.api import (
    BookRequest,
    BookResponse,
)

from app.schemas.models import Book, Message, CompletionRequest, CompletionResponse


from app.clients.book_cache_client import BookCacheClient
from app.clients.llm_client import DeepSeekAPIClient


from app.services.profanity import contains_profanity


from app.services.semantic_search import (
    create_vector_embedding,
    calculate_similarity_scores,
    get_top_k_books,
)

from app.services.preprocessing import preprocess_book

from app.services.rag_pipeline import sse_response_generator


import json
import redis
import logging
import numpy as np
import torch

import httpx
import http.client

import logging
from openai import OpenAI, AsyncOpenAI


import os
from dotenv import load_dotenv

load_dotenv()

# app/api/routes.py
# Create a router instance to define API endpoints.
router = APIRouter()


DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

logger = logging.getLogger(__name__)


client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


@router.post("/completion")
async def chat_stream(req: dict):
    """
    Stream chat completions from the DeepSeek LLM to the client via Server-Sent Events (SSE).

    This endpoint accepts a POST request containing a list of messages, forwards them to the LLM API,
    and returns the generated completion in an SSE stream. The SSE events are formatted as plain text,
    with each event prefixed by "data:" and terminated by two newline characters.

    """
    logger.info("/completion")
    logger.debug(json.dumps(req, indent=4))

    try:
        stream = client.chat.completions.create(
            messages=req["messages"],
            model="deepseek-chat",
            max_tokens=500,
            stream=True,
            temperature=1.3,
        )
    except Exception as e:
        logger.error("Error creating completion stream: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to create completion stream: %s" % e
        )

    def event_generator():
        """
        Generator function that iterates over the streaming response from the LLM API,
        formats each chunk as an SSE event, and yields the encoded event to the client.

        If an error occurs while processing a chunk, an SSE event with an error message is
        yielded and the generator terminates.
        """
        try:
            for chunk in stream:
                try:

                    # Yield the chunk's delta content; if missing, yield an empty string.
                    text = chunk.choices[0].delta.content or ""
                    sse_event = f"data: {text}\n\n"
                    print("Yielding sse_event", repr(sse_event))

                    yield sse_event.encode("utf-8")
                except Exception as inner_e:
                    logger.error("Error processing chunk: %s", inner_e)

                    error_data = json.dumps({"error": "Error during streaming"})
                    yield f"data: {error_data}\n\n".encode("utf-8")
                    break
        except Exception as gen_e:
            logger.error("Error in event generator: %s", gen_e)
            error_data = json.dumps({"error": "Error during streaming"})
            yield f"data: {error_data}\n\n".encode("utf-8")

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# -----------------------------------------------------------------------------
# Route: Search Books
# This endpoint processes user queries to find relevant books using semantic similarity.
# It leverages embeddings to understand the meaning behind the query and retrieves the most relevant books.
# -----------------------------------------------------------------------------
@router.post("/search_books")
async def search_books(
    request: Request,
    payload: BookRequest,
):
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
        print("Top Books:")
        print(top_books)
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

        print("prompt")
        print(llm_prompt)

        # 8. Prepare LLM Client & Streaming
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

        # 8. Define a single streaming generator that yields chunks and then a final marker.
        # async def generate():
        #     async for chunk in llm_client.async_stream(
        #         model="deepseek-chat",
        #         messages=messages,
        #         temperature=0.7,
        #     ):
        #         print(chunk, end="", flush=True)
        #         # Yield each chunk prefixed with "data:" (SSE format).
        #         yield f"data: {chunk}\n\n"

        # 9. Return the StreamingResponse.
        # return StreamingResponse(generate(), media_type="text/event-stream")
        return StreamingResponse(
            sse_response_generator(llm_client, "deepseek-chat", messages, 0.7),
            media_type="text/event-stream",
        )

    except Exception as e:
        logging.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing your request."
        )

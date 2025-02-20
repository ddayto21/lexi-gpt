# app/api/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import logging
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)


client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


class SSEPayload(BaseModel):
    content: str


class SSEErrorPayload(BaseModel):
    error: str


@router.post("/chat")
async def completion(req: dict):
    """Handles streaming chat completion requests to the DeepSeek LLM.

    This endpoint proxies chat messages to the DeepSeek API and streams the LLM's
    response back to the client using Server-Sent Events (SSE).

    The request body must be a JSON object with a "messages" key containing an array
    of message objects (each with "role" and "content" keys). A system prompt is
    injected to instruct the model to provide book recommendations in a predefined format.

    :param req: The chat messages (dict).
    :return: An SSE stream of text events.
    :raises HTTPException: If an error occurs during the DeepSeek API interaction.
    """
    logger.info("/chat")

    # Defensive check: ensure `messages` key is present and is a list
    if "messages" not in req or not isinstance(req["messages"], list):
        error_detail = "Request must include 'messages' as a list."
        logger.error(error_detail)
        raise HTTPException(status_code=400, detail=error_detail)

    try:
        stream = client.chat.completions.create(
            messages=req["messages"],
            model="deepseek-chat",
            max_tokens=500,
            stream=True,
            temperature=0.3,
        )
    except Exception as e:

        def error_generator(e):
            error_payload = SSEErrorPayload(
                error=f"Failed to create completion stream: {e}"
            )
            yield f"data: {error_payload.json()}\n\n".encode("utf-8")

        return StreamingResponse(
            error_generator(e), media_type="text/event-stream", status_code=200
        )

    def event_generator():
        """
        Generator function that yields SSE events from the LLM's streaming response.

        This function iterates through the chunks received from the DeepSeek API,
        formats each chunk as an SSE event (JSON payload with "content" key), and yields it.
        Error handling is included to catch issues during chunk processing or within the
        generator itself, sending error messages back to the client as JSON in SSE events.
        """

        try:
            for chunk in stream:
                try:
                    # Crate payload using pydantic model
                    text = chunk.choices[0].delta.content or ""
                    payload = SSEPayload(content=text)
                    yield f"data: {payload.json()}\n\n".encode("utf-8")

                except Exception as inner_e:
                    error_payload = SSEErrorPayload(error="Error during streaming")
                    yield f"data: {error_payload.json()}\n\n".encode("utf-8")
                    logger.error("Error during streaming: %s", inner_e)

                    break  # Stop processing further chunks on error
        except Exception as gen_e:
            error_payload = SSEErrorPayload(error="Error during streaming")
            yield f"data: {error_payload.json()}\n\n".encode("utf-8")
            logger.error("Error during streaming: %s", gen_e)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

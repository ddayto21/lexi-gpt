# app/api/chat.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import logging
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from app.schemas.chat import ChatRequest, ChatMessage


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
async def chat(req: ChatRequest):
    """Handles streaming chat completion requests to the DeepSeek LLM.

    This endpoint proxies chat messages to the DeepSeek API and streams the LLM's
    response back to the client using Server-Sent Events (SSE). Every event is
    properly prefixed with "data:" and terminated with two newlines.

    :param req: The chat messages (dict).
    :return: An SSE stream of text events.
    :raises HTTPException: If an error occurs during the DeepSeek API interaction.
    """
    logger.info("/chat")
    logger.info(req.model_dump_json(indent=2))

    # Prepend the system prompt to the client messages.
    system_prompt = {
        "role": "system",
        "content": "Please provide only 3 recommendations. If you do not have a good recommendation, please mention that.",
    }
    # Insert the system prompt at the beginning of the messages list.
    req.messages.insert(0, system_prompt)

    try:
        stream = client.chat.completions.create(
            messages=req.messages,
            model="deepseek-chat",
            max_tokens=300,
            stream=True,
            temperature=0.3,
        )
    except Exception as e:

        def error_generator(e):
            error_payload = SSEErrorPayload(
                error=f"Failed to create completion stream: {e}"
            )
            sse_error_event = f"data: {error_payload.json()}\n\n"
            yield sse_error_event.encode("utf-8")

        return StreamingResponse(
            error_generator(e), media_type="text/event-stream", status_code=200
        )

    def event_generator():
        """
        Generator function that yields SSE events from the LLM's streaming response.
        Each event is prefixed with "data:" and terminated with two newlines.
        Verbose logging is added to help debug the raw chunks and SSE formatting.
        """

        try:
            for chunk in stream:
                try:
                    logger.debug("Received chunk: %s", chunk)
                    # Log the full chunk structure for inspection.
                    if hasattr(chunk, "choices"):
                        logger.debug("Chunk choices: %s", chunk.choices)
                    else:
                        logger.debug("Chunk has no 'choices' attribute.")

                    # Extract delta content; if missing, default to empty string.
                    text = chunk.choices[0].delta.content or ""
                    logger.debug("Extracted text from chunk: '%s'", text)
                    payload = SSEPayload(content=text)
                    sse_event = f"data: {payload.json()}\n\n"
                    logger.debug("Formatted SSE event: %s", sse_event)
                    yield sse_event.encode("utf-8")
                except Exception as inner_e:
                    logger.error("Error processing chunk: %s", inner_e)
                    error_payload = SSEErrorPayload(error="Error during streaming")
                    sse_error_event = f"data: {error_payload.json()}\n\n"
                    logger.debug("Yielding SSE error event: %s", sse_error_event)
                    yield sse_error_event.encode("utf-8")
                    break  # Stop processing further chunks on error
        except Exception as gen_e:
            logger.error("Error in event generator: %s", gen_e)
            error_payload = SSEErrorPayload(error="Error during streaming")
            sse_error_event = f"data: {error_payload.json()}\n\n"
            yield sse_error_event.encode("utf-8")

    return StreamingResponse(event_generator(), media_type="text/event-stream")

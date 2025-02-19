from fastapi import (
    APIRouter,
    HTTPException,
)

from fastapi.responses import StreamingResponse
import json
import logging

from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)


client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


@router.post("/completion")
async def completion(req: dict):
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

# app/api/chat.py
from fastapi import APIRouter, HTTPException
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
    logger.info("/completion")
    # logger.debug(json.dumps(req, indent=4))
    # logger.info(json.dumps(req, indent=4))

    # Defensive check: ensure `messages` key is present and is a list
    if "messages" not in req or not isinstance(req["messages"], list):
        error_detail = "Request must include 'messages' as a list."
        logger.error(error_detail)
        raise HTTPException(status_code=400, detail=error_detail)

    # Inject system prompt into the conversation
    # system_prompt = {
    #     "role": "system",
    #     "content": (
    #         "book recommendations in the following format:\n\n"
    #         "1. [Book Title 1]\n"
    #         "* Summary: [Brief summary of the book]\n"
    #         "* Explanation: [Why I'm recommending this book based on your preferences]\n\n"
    #         "2. [Book Title 2]\n"
    #         "* Summary: [Brief summary of the book]\n"
    #         "* Explanation: [Why I'm recommending this book based on your preferences]\n\n"
    #         "3. [Book Title 3]\n"
    #         "* Summary: [Brief summary of the book]\n"
    #         "* Explanation: [Why I'm recommending this book based on your preferences]\n"
    #     ),
    # }

    # # Log messages before insertion
    # logger.debug(
    #     "Messages before system prompt insertion:\n%s",
    #     json.dumps(req["messages"], indent=4),
    # )

    # try:
    #     req["messages"].insert(0, system_prompt)
    # except Exception as insert_error:
    #     logger.error("Error inserting system prompt: %s", insert_error)
    #     raise HTTPException(
    #         status_code=400, detail=f"Failed to insert system prompt: {insert_error}"
    #     )

    # Log messages after insertion
    # logger.debug(
    #     "Messages after system prompt insertion:\n%s",
    #     json.dumps(req["messages"], indent=4),
    # )

    try:
        stream = client.chat.completions.create(
            messages=req["messages"],
            model="deepseek-chat",
            max_tokens=500,
            stream=True,
            temperature=1.3,
        )
    except Exception as e:
        # Return error as JSON in the SSE stream.  Client should handle this.
        # Return error as JSON in the SSE stream.  Client should handle this.
        def error_generator(e):
            error_data = json.dumps(
                {"error": f"Failed to create completion stream: {e}"}
            )
            yield f"data: {error_data}\n\n".encode("utf-8")

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
                    # Yield the chunk's delta content; if missing, yield an empty string.
                    text = chunk.choices[0].delta.content or ""
                    sse_event = f"data: {text}\n\n"

                    yield sse_event.encode("utf-8")
                except Exception as inner_e:
                    logger.error("Error processing chunk: %s", inner_e)

                    error_data = json.dumps({"error": "Error during streaming"})
                    yield f"data: {error_data}\n\n".encode("utf-8")
                    break  # Stop processing further chunks on error
        except Exception as gen_e:
            logger.error("Error in event generator: %s", gen_e)
            error_data = json.dumps({"error": "Error during streaming"})
            yield f"data: {error_data}\n\n".encode("utf-8")

    return StreamingResponse(event_generator(), media_type="text/event-stream")

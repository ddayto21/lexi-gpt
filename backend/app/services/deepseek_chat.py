import httpx
import json
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration: load API key from an environment variable.
API_KEY = os.getenv("DEEPSEEK_API_KEY")

BASE_URL = "https://api.deepseek.com/chat/completions"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}


async def deepseek_chat(
    messages: list, model: str = "deepseek-chat", stream: bool = True
) -> AsyncGenerator[str, None]:
    """
    Interact with DeepSeek's chat model asynchronously via streaming.

    Sends a POST request with a message history to the DeepSeek API,
    and streams the response line-by-line. Each response chunk is expected
    to be a JSON string that contains a "choices" array. This function extracts
    the "content" field from the first choice's "delta" object and yields it.

    Args:
        messages (list): The conversation history, including system and user messages.
        model (str): The DeepSeek model to use (e.g. "deepseek-chat").
        stream (bool): Whether to stream the response.

    Yields:
        str: The generated text content from the DeepSeek API.
    """
    payload = {"model": model, "messages": messages, "stream": stream}

    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream(
            "POST", BASE_URL, headers=HEADERS, json=payload
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    print("Received line:", line)  # Debug output
                    if line.startswith("data:"):
                        line = line[len("data:") :].strip()
                    try:
                        data = json.loads(line)
                        # Extract the "content" from the delta of the first choice.
                        choices = data.get("choices", [])

                        if choices:
                            content = choices[0].get("delta", {}).get("content", "")
                            if content:
                                print("Extracted content:", content)  # Debug output
                                yield content
                    except json.JSONDecodeError:
                        # Skip malformed JSON lines.
                        print("Failed to decode JSON:", line)  # Debug output
                        continue

import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

import httpx  # For making asynchronous HTTP requests
import asyncio  # For running asynchronous code
import json  # For parsing JSON responses
import requests  # For making synchronous HTTP requests

from typing import AsyncGenerator, Generator, List, Dict, Optional

import logging

# Configure module-level logger.
logger = logging.getLogger(__name__)


# Ensure environment variables are loaded.
load_dotenv()


# -----------------------------------------------------------------------------
# A client designed to interact with the DeepSeek API.
# It supports both asynchronous and synchronous streaming of model responses.
# -----------------------------------------------------------------------------
class DeepSeekAPIClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com/v1/chat/completions",
        client: Optional[httpx.AsyncClient] = None,
        timeout: Optional[httpx.Timeout] = None,
    ):

        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")

        if not self.api_key:
            raise ValueError(
                "API key not provided or set in DEEPSEEK_API_KEY environment variable"
            )
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        self.client = client  # Allows dependency injection for testing.

    def get_token_balance(self) -> dict:
        """
        Query the available token balance from the DeepSeek API.

        Returns:
            dict: A dictionary containing the token balance information.
        """

        balance_url = "https://api.deepseek.com/user/balance"

        try:
            response = requests.get(balance_url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error querying token balance: {e}")
            return {"error": str(e)}

    async def async_stream(
        self, model: str, messages: List[Dict], temperature: float
    ) -> AsyncGenerator[str, None]:
        """
        Asynchronously streams responses from the DeepSeek API.

        Sends a POST request with the specified model, messages, and temperature parameters,
        then yields each received chunk formatted as a Server-Sent Event (SSE) string.
        Finally, it yields a final SSE message indicating completion.

        Args:
            model (str): The DeepSeek model identifier (e.g., "deepseek-chat").
            messages (List[Dict]): Conversation history messages.
            temperature (float): Controls the randomness of the model's output.

        Yields:
            str: SSE-formatted text chunks, ending with 'data: {"done": true}\n\n' to signal completion.
        """
        client = self.client or httpx.AsyncClient(http2=True, timeout=None)
        try:
            async with client:
                async with client.stream(
                    "POST",
                    self.base_url,
                    headers=self.headers,
                    json={
                        "model": model,
                        "messages": messages,
                        "max_tokens": 1000,
                        "temperature": temperature,
                        "stream": True,
                    },
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                json_data = json.loads(line[6:])
                                chunk = json_data["choices"][0]["delta"].get(
                                    "content", ""
                                )
                                if chunk:
                                    yield f"data: {chunk}\n\n"
                            except json.JSONDecodeError:
                                logger.warning(
                                    "Failed to parse JSON from line: %s", line
                                )
                                continue
                    # Signal end of stream.
                    yield 'data: {"done": true}\n\n'
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error in async_stream: %s", e)
            raise
        except httpx.TimeoutException as e:
            logger.error("Timeout in async_stream: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error in async_stream: %s", e)
            raise

    def sync_stream(
        self, model: str, messages: List[Dict], temperature: float
    ) -> Generator[str, None, None]:
        """
        Synchronous generator that streams responses from DeepSeek.
        Yields:
            str: Chunks of generated text as they arrive.
        """
        # Make a POST request with streaming enabled using the synchronous requests library.
        with requests.post(
            self.base_url,
            headers=self.headers,
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "stream": True,  # Request a streaming response.
            },
            stream=True,
        ) as response:
            response.raise_for_status()  # Raise an error if the request fails.
            # Iterate over each line in the streaming response.
            for line in response.iter_lines():
                if line:
                    # Convert bytes to string.
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data: "):
                        try:
                            # Parse the JSON data in the line.
                            json_data = json.loads(decoded_line[6:])
                            #  Extract the text content from the response payload.
                            chunk = json_data["choices"][0]["delta"].get("content", "")
                            if chunk:
                                yield chunk  # Yield the chunk.
                        except json.JSONDecodeError:
                            # Skip any lines that are not valid JSON.
                            continue


# -----------------------------------------------------------------------------
# Helper function to read a multi-line prompt.
# The user can type multiple lines. When finished, they type '/send' on a new line.
# -----------------------------------------------------------------------------
def read_multiline_prompt() -> str:
    """
    Read multi-line input from the user until '/send' is entered on a new line.
    Returns:
        The full prompt as a single string.
    """
    print("Enter your prompt (type '/send' on a new line when finished):")
    lines = []
    while True:
        line = input()
        # When user types '/send', end the input collection.
        if line.strip() == "/send":
            break
        lines.append(line)
    return "\n".join(lines)

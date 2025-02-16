import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

import httpx  # For making asynchronous HTTP requests
import asyncio  # For running asynchronous code


from typing import AsyncGenerator, Generator, List, Dict, Optional

import json  # For parsing JSON responses
import requests  # For making synchronous HTTP requests


# -----------------------------------------------------------------------------
# A client designed to interact with the DeepSeek API.
# This client can stream responses either asynchronously or synchronously.
# -----------------------------------------------------------------------------
class DeepSeekAPIClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com/v1/chat/completions",
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

    async def async_stream(
        self, model: str, messages: List[Dict], temperature: float
    ) -> AsyncGenerator[str, None]:
        """Async generator that streams responses from the DeepSeek API.

        Yields:
            str: Chunks of generated text as they arrive.
        """
        # Create an asynchronous HTTP client.
        async with httpx.AsyncClient() as client:
            # Open a streaming response from the LLM provider API.
            async with client.stream(
                "POST",
                self.base_url,
                headers=self.headers,
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": True,  # Ask the API to stream the response.
                },
            ) as response:
                response.raise_for_status()  # Raise an error if the request was unsuccessful.
                # Process each line in the streaming response.
                async for line in response.aiter_lines():
                    # Check if the line starts with "data: ", which indicates a valid data line.
                    if line.startswith("data: "):
                        try:
                            # Parse the JSON data after "data: "
                            json_data = json.loads(line[6:])
                            # Extract the content from the first choice's delta.
                            chunk = json_data["choices"][0]["delta"].get("content", "")
                            if chunk:
                                yield chunk  # Yield this chunk to the caller.
                        except json.JSONDecodeError:
                            # If the line is not valid JSON, skip it.
                            continue

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
# Main program entry point.
# This section handles command-line arguments and prompts the user for a prompt.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import sys

    def parse_args():
        """
        Parse command-line arguments.
        The user can optionally specify the model, temperature, and async mode.
        """
        parser = argparse.ArgumentParser(
            description="DeepSeek CLI Client - Chat with DeepSeek models"
        )
        parser.add_argument(
            "--model",
            type=str,
            default="deepseek-chat",
            help="Model to use (default: deepseek-chat)",
        )
        parser.add_argument(
            "--temperature",
            type=float,
            default=0.7,
            help="Temperature parameter (default: 0.7)",
        )
        parser.add_argument(
            "--async-mode",
            action="store_true",
            help="Use asynchronous mode (requires Python 3.7+)",
        )
        return parser.parse_args()

    # Load environment variables from the .env file.
    load_dotenv()
    args = parse_args()

    # Prompt the user to enter a prompt interactively in the terminal.
    prompt_input = input("Enter your prompt: ")
    # Build the messages list expected by the API.
    messages = [{"role": "user", "content": prompt_input}]

    # Create an instance of the DeepSeekAPIClient.
    # The API key is loaded from the environment if not provided.
    client = DeepSeekAPIClient()

    try:
        if args.async_mode:
            # If the user selected async mode, run the asynchronous streaming function.
            async def run_async():
                try:
                    # Iterate over the response chunks as they stream in.
                    async for chunk in client.async_stream(
                        model=args.model,
                        messages=messages,
                        temperature=args.temperature,
                    ):
                        # Print each chunk without adding a new line.
                        print(chunk, end="", flush=True)
                    print()  # Print a newline after the streaming is complete.
                except httpx.HTTPStatusError as e:
                    print(
                        f"\nHTTP error occurred: {e.response.status_code} {e.response.reason_phrase}"
                    )
                except Exception as e:
                    print(f"\nAn error occurred: {str(e)}")

            # Run the asynchronous function.
            asyncio.run(run_async())
        else:
            # If not in async mode, use the synchronous streaming method.
            try:
                for chunk in client.sync_stream(
                    model=args.model, messages=messages, temperature=args.temperature
                ):
                    # Print each chunk as it arrives.
                    print(chunk, end="", flush=True)
                # Newline after complete streaming.
                print()
            except requests.exceptions.HTTPError as e:
                print(
                    f"\nHTTP error occurred: {e.response.status_code} {e.response.reason_phrase}"
                )
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, handle the interruption gracefully.
        print("\n\nOperation interrupted by user")
        sys.exit(0)

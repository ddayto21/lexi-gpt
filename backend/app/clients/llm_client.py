# app/clients/llm_client.py

from typing import List, Dict, Any
from ollama import AsyncClient
import os


class LLMClient:
    """
    LLMClient handles asynchronous LLM tasks using Ollama’s AsyncClient.
    This version removes the extra ThreadPoolExecutor and transformer pipelines,
    so it is leaner and has less overhead.
    """

    def __init__(self):
        # Initialize a single reusable AsyncClient instance.
        self.client = AsyncClient()

    async def extract_keywords(self, query: str) -> str:
        """
        Extracts relevant keywords from a user query using an external LLM.
        The assistant is instructed to extract key terms as a comma-separated string.
        """
        prompt = (
            "You are a helpful assistant that extracts relevant keywords from user queries. "
            "When given a query, extract the key terms that best represent the main ideas and "
            "return them as a single, comma-separated string. Do not include any additional text."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
        response = await self.client.chat(model="llama3.2", messages=messages)
        return response.message.content

    async def enhance_book_descriptions(self, books_data: list) -> list:
        """
        Enhances book descriptions using an external LLM.

        This method could be implemented similarly to extract_keywords by formulating a prompt
        that instructs the LLM to enhance or rewrite book descriptions.
        For now, it simply returns the original list.
        """
        # For demonstration, we simply return the input data.
        # You could add similar logic as in extract_keywords if needed.
        return books_data

    async def close(self):
        """
        Closes the asynchronous client if a close method exists.
        """
        if hasattr(self.client, "aclose"):
            await self.client.aclose()
        else:
            # If no explicit close is available, do nothing.
            pass

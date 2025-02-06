import httpx
from typing import Dict, Any

BASE_URL = "https://openlibrary.org"


class OpenLibraryAPI:
    """
    Optimized OpenLibrary API client.

    Reuses a single AsyncClient instance for fast connection pooling,
    minimizing latency by avoiding repeated client instantiation.
    """

    SEARCH_ENDPOINT = "/search.json?q={query}&limit=5"

    def __init__(self):
        self.base_url = BASE_URL
        # Create a single reusable AsyncClient with a fixed timeout.
        self.client = httpx.AsyncClient(timeout=5)

    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """
        Fetch data from the given URL using the reusable AsyncClient.
        Returns the JSON response if successful, or an empty dict on error.
        """
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return {}

    async def search(self, query: str) -> Dict[str, Any]:
        """
        Searches for books using the query string.
        """
        url = f"{self.base_url}{self.SEARCH_ENDPOINT.format(query=query)}"
        return await self.fetch_data(url)

    async def close(self):
        """
        Closes the reusable AsyncClient.
        """
        await self.client.aclose()

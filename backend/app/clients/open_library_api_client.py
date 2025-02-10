import httpx
from typing import Dict, Any
import urllib.parse

BASE_URL = "https://openlibrary.org"


class OpenLibraryAPI:
    """
    Optimized OpenLibrary API client.

    Reuses a single AsyncClient instance for fast connection pooling,
    minimizing latency by avoiding repeated client instantiation.
    """

    SEARCH_ENDPOINT = "/search.json?q={query}&limit=5"
    SUBJECTS_ENDPOINT = "/subjects/{query}.json?details=true"

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

    async def search_subjects(self, query: str) -> Dict[str, Any]:
        """
        Searches for works on one or more subjects using the search endpoint.

        Splits the query by commas and uses an "OR" query to find works matching any subject.

        For example:
            Input: "juvenile fiction, juvenile literature"
            Constructs: subject:("juvenile fiction" OR "juvenile literature")
            Final URL: https://openlibrary.org/search.json?q=subject:(%22juvenile+fiction%22+OR+%22juvenile+literature%22)
        """
        print("query: ", query)
        # Split the query into individual subjects and trim whitespace.
        terms = [term.strip() for term in query.split(",") if term.strip()]
        if not terms:
            return {}
        # Create a query string using OR logic.
        or_query = " OR ".join(f'"{term}"' for term in terms)
        full_query = f"subject:({or_query})"
        encoded_query = urllib.parse.quote(full_query)
        url = f"{self.base_url}/search.json?q={encoded_query}"
        print("url: ", url)
        return await self.fetch_data(url)

    async def close(self):
        """
        Closes the reusable AsyncClient.
        """
        await self.client.aclose()

import httpx
from typing import Dict, Any

BASE_URL = "https://openlibrary.org"

class OpenLibraryAPI:
    """
    Optimized OpenLibrary API client.
    """
    SEARCH_ENDPOINT = "/search.json?q={query}&limit=5"

    def __init__(self):
        self.base_url = BASE_URL

    async def fetch_data(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Supports two usage modes:
          - Called with one argument: fetch_data(url)
            -> Creates a temporary AsyncClient.
          - Called with two arguments: fetch_data(client, url)
            -> Uses the provided AsyncClient.
        """
        if len(args) == 1:
            url = args[0]
            client = None
        elif len(args) == 2:
            client, url = args
        else:
            raise ValueError("fetch_data expects either 1 or 2 arguments: (url) or (client, url)")

        if client is None:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, timeout=5)
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPError:
                    return {}
        else:
            try:
                response = await client.get(url, timeout=5)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {}

    async def search(self, query: str) -> Dict[str, Any]:
        """
        Search for books by query.
        """
        url = self.base_url + self.SEARCH_ENDPOINT.format(query=query)
        return await self.fetch_data(url)

    async def close(self):


        pass

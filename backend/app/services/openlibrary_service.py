import asyncio
import httpx
import json
from typing import Dict, Any

BASE_URL = "https://openlibrary.org"


class OpenLibraryAPI:
    """
    Service for querying Open Library APIs asynchronously.
    """

    ENDPOINTS = {
        "book_search": "/search.json?q={query}",
        "authors": "/search/authors.json?q={query}",
        "subjects": "/subjects/{query}.json",
        "covers": "/covers/{query}",
        "inside_search": "/search/inside.json?q={query}",
        "works": "/works/{query}.json",
        "editions": "/editions/{query}.json",
    }

    def __init__(self):
        """Initializes the Open Library API service."""
        self.base_url = BASE_URL

    async def fetch_data(self, client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
        """
        Makes an asynchronous request to an Open Library API endpoint.
        :param client: httpx.AsyncClient session
        :param url: Full API request URL
        :return: JSON response data or an empty dictionary on failure
        """
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Request failed for {url}: {str(e)}")
            return {}

    async def search(self, query: str) -> Dict[str, Any]:
        """
        Searches Open Library APIs concurrently and returns aggregated results.
        :param query: User's search query
        :return: Dictionary containing search results from various endpoints
        """
        async with httpx.AsyncClient() as client:
            # Construct URLs for each API endpoint
            urls = {
                key: self.base_url + endpoint.format(query=query)
                for key, endpoint in self.ENDPOINTS.items()
            }

            # Fetch data concurrently
            results = await asyncio.gather(
                *[self.fetch_data(client, url) for url in urls.values()]
            )

            return {
                "book_search": results[0].get("docs", []),
                "authors": results[1].get("docs", []),
                "subjects": results[2],
                "covers": results[3],
                "inside_search": results[4],
                "works": results[5],
                "editions": results[6],
            }


# Example Usage
if __name__ == "__main__":

    async def main():
        openlibrary_service = OpenLibraryAPI()
        query = "Harry Potter"
        results = await openlibrary_service.search(query)
        print(json.dumps(results, indent=2))

    asyncio.run(main())

import asyncio
import httpx
import json
from typing import Dict, Any, Optional

BASE_URL = "https://openlibrary.org"


class OpenLibraryAPI:
    """
    Service for querying Open Library APIs asynchronously with enhanced search capabilities.
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

    async def search(
        self,
        query: str,
        ddc: Optional[str] = None,
        lcc: Optional[str] = None,
        birth_date: Optional[int] = None,
        subject: Optional[str] = None,
        exclude_subject: Optional[str] = None,
        ebook_access: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Searches Open Library APIs with advanced query filtering.

        :param query: User's search query.
        :param ddc: Dewey Decimal Classification filter (e.g., "ddc:200*").
        :param lcc: Library of Congress Classification filter (e.g., "lcc:A*").
        :param birth_date: Search for authors born in a specific year.
        :param subject: Search for books by subject.
        :param exclude_subject: Exclude books that have a specific subject.
        :param ebook_access: Filter books based on availability (e.g., "no_ebook", "borrowable", "public").
        :return: Dictionary containing search results from various endpoints.
        """

        # Build enhanced query string
        query_filters = [f"{query}"]
        if ddc:
            query_filters.append(f"ddc:{ddc}")
        if lcc:
            query_filters.append(f"lcc:{lcc}")
        if birth_date:
            query_filters.append(f"birth_date:{birth_date}")
        if subject:
            query_filters.append(f"subject:{subject}")
        if exclude_subject:
            query_filters.append(f"-subject_key:{exclude_subject}")
        if ebook_access:
            query_filters.append(f"ebook_access:{ebook_access}")

        enhanced_query = " AND ".join(query_filters)

        async with httpx.AsyncClient() as client:
            # Construct URLs for each API endpoint with enhanced query
            urls = {
                key: self.base_url + endpoint.format(query=enhanced_query)
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
        results = await openlibrary_service.search(
            query, ddc="200*", birth_date=1965, subject="fantasy", ebook_access="public"
        )
        print(json.dumps(results, indent=2))

    asyncio.run(main())

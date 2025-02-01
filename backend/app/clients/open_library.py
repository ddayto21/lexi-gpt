import asyncio
import json
from typing import Dict, Any, Optional
import httpx

BASE_URL = "https://openlibrary.org"


class OpenLibraryAPI:
    """
    Asynchronous client for fetching and filtering data from Open Library.
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
        self.base_url = BASE_URL

    async def fetch_data(self, client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
        """
        Sends an HTTP GET to the given URL, returning parsed JSON or {} on error.
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
        limit: int = 5,
        birth_date: Optional[int] = None,
        subject: Optional[str] = None,
        exclude_subject: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Runs a broad search with the base 'query' plus optional filters:
        - birth_date for author birth year
        - subject/exclude_subject to filter by topics

        Returns data from several endpoints in a single dictionary.
        """
        # Builds a combined query string for Open Library's search syntax.
        query_filters = [query]
        if birth_date:
            query_filters.append(f"birth_date:{birth_date}")
        if subject:
            query_filters.append(f"subject:{subject}")
        if exclude_subject:
            query_filters.append(f"-subject_key:{exclude_subject}")
        # Uses "AND" syntax to refine the search with multiple filters.
        enhanced_query = " AND ".join(query_filters)

        async with httpx.AsyncClient() as client:
            # Construct URLs for each endpoint; each uses the enhanced query.
            urls = {
                key: self.base_url + endpoint.format(query=enhanced_query)
                for key, endpoint in self.ENDPOINTS.items()
            }

            # Append a limit for the book_search endpoint.
            if "book_search" in urls:
                urls["book_search"] += f"&limit={limit}"
            # Fetch all endpoints in parallel.
            tasks = [self.fetch_data(client, url) for url in urls.values()]
            results = await asyncio.gather(*tasks)

            # Return the relevant parts from each endpoint's JSON.
            return {
                "book_search": results[0].get("docs", []),
                "authors": results[1].get("docs", []),
                "subjects": results[2],
                "covers": results[3],
                "inside_search": results[4],
                "works": results[5],
                "editions": results[6],
            }
            

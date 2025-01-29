import asyncio
import json
from typing import Dict, Any, Optional
import httpx

BASE_URL = "https://openlibrary.org"


class OpenLibraryAPI:
    """
    Service for querying Open Library APIs asynchronously with advanced/optional filters.
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
        Makes an async request to an Open Library endpoint and returns JSON data or {} on failure.
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
        Searches Open Library with optional filters (DDC, LCC, birth_date, etc.),
        returning a dict with results from each endpoint.
        """
        query_filters = [query]
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
            urls = {
                key: self.base_url + endpoint.format(query=enhanced_query)
                for key, endpoint in self.ENDPOINTS.items()
            }
            tasks = [self.fetch_data(client, url) for url in urls.values()]
            results = await asyncio.gather(*tasks)

            # Order of results matches order of URLs
            return {
                "book_search": results[0].get("docs", []),
                "authors": results[1].get("docs", []),
                "subjects": results[2],
                "covers": results[3],
                "inside_search": results[4],
                "works": results[5],
                "editions": results[6],
            }

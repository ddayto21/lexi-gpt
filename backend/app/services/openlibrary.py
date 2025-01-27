import httpx


async def fetch_books(query: str):
    url = f"https://openlibrary.org/search.json?q={query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch books: {response.text}")
        # Return top 3 results
        return response.json()["docs"][:3]
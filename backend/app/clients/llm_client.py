import httpx

class LLMClient:
    def __init__(self, refine_endpoint: str, enhance_endpoint: str):
        self.refine_endpoint = refine_endpoint
        self.enhance_endpoint = enhance_endpoint
        self.client = httpx.AsyncClient()

    async def refine_query(self, query: str) -> str:
        response = await self.client.post(self.refine_endpoint, json={"query": query})
        response.raise_for_status()
        data = response.json()
        return data.get("refined_query", query)

    async def enhance_book_descriptions(self, books_data: list) -> list:
        response = await self.client.post(self.enhance_endpoint, json={"books": books_data})
        response.raise_for_status()
        data = response.json()
        return data.get("enhanced_books", books_data)

    async def close(self):
        await self.client.aclose()
import pytest
import asyncio
from app.clients.llm_client import LLMClient

@pytest.mark.asyncio
async def test_local_llm_client():
    client = LLMClient()
    
    original_query = "The Cat and The Hat"
    refined_query, enhanced_books = await client.process_query(original_query)

    # By default, LLMClient removes "the" and "and" from queries
    # => "Cat Hat"
    assert refined_query == "cat hat", f"Expected 'cat hat', got '{refined_query}'"
    assert isinstance(enhanced_books, list), "enhanced_books should be a list"
    assert len(enhanced_books) > 0, "We expect at least one dummy book"
    assert "title" in enhanced_books[0], "Expected a 'title' field in the dummy book data"

    await client.close()
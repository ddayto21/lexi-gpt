import pytest
import pytest_asyncio
import httpx
from asgi_lifespan import LifespanManager
from app.main import app

@pytest_asyncio.fixture
async def async_test_client():
    """
    Creates an AsyncClient that runs the app's lifespan events.
    """
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client


@pytest.mark.asyncio
async def test_search_books_normal(async_test_client):
    """
    Tests a normal query to /search_books, expecting 200 and some recommendations.
    """
    payload = {"query": "fantasy novel"}
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    data = resp.json()
    assert "recommendations" in data, "Expected key 'recommendations' in response"
    recs = data["recommendations"]
    assert isinstance(recs, list), "Expected 'recommendations' to be a list"

    if recs:
        first = recs[0]
        assert "title" in first
        assert "authors" in first
        assert "description" in first

@pytest.mark.asyncio
async def test_search_books_profanity(async_test_client):
    """
    If the query contains profanity, we expect HTTP 403.
    """
    payload = {"query": "shit novel"}
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}"

@pytest.mark.asyncio
async def test_search_books_caching(async_test_client):
    """
    Tests caching by calling the same query twice and ensuring
    the second response is identical (assuming the route uses Redis).
    """
    query_str = "historical romance"
    payload = {"query": query_str}

    # First call
    first_resp = await async_test_client.post("/search_books", json=payload)
    assert first_resp.status_code == 200
    first_data = first_resp.json()

    # Second call
    second_resp = await async_test_client.post("/search_books", json=payload)
    assert second_resp.status_code == 200
    second_data = second_resp.json()

    assert first_data == second_data, "Expected identical responses from cache"

@pytest.mark.asyncio
async def test_search_books_empty_query(async_test_client):
    """
    If the user sends an empty query, the route should still return 200 with minimal results.
    """
    payload = {"query": ""}
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert "recommendations" in data
    recs = data["recommendations"]
    assert isinstance(recs, list), "Expected a list, even if empty"

@pytest.mark.asyncio
async def test_search_books_specific(async_test_client):
    """
    A more specific query to see if results appear correct.
    """
    payload = {"query": "mystery novel in London"}
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    recs = data["recommendations"]
    assert isinstance(recs, list)
    if recs:
        first = recs[0]
        assert "title" in first
        assert "authors" in first
        assert "description" in first
import pytest
import pytest_asyncio
import asyncio
import httpx
import json
from httpx import ASGITransport, AsyncClient

from app.main import app

@pytest_asyncio.fixture
async def async_test_client():
    """
    In-process test client that manually calls on_startup / on_shutdown,
    ensuring LLMClient, Redis, etc. are initialized.
    """
    # 1) Manually call startup events
    for handler in app.router.on_startup:
        if asyncio.iscoroutinefunction(handler):
            await handler()
        else:
            handler()

    # 2) Create an in-process test client using ASGITransport

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # 3) Manually call shutdown events
    for handler in app.router.on_shutdown:
        if asyncio.iscoroutinefunction(handler):
            await handler()
        else:
            handler()

@pytest.mark.asyncio
async def test_search_books_normal(async_test_client):
    """
    Tests a normal query to /search_books, expecting 200 and some recommendations.
    """
    payload = {"query": "fantasy novel"}
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    data = resp.json()
    # The route returns { "recommendations": [ ... ] }
    assert "recommendations" in data, "Expected key 'recommendations' in response"
    recs = data["recommendations"]
    assert isinstance(recs, list), "Expected 'recommendations' to be a list"

    if recs:
        # We do a minimal structural check on the first item
        first = recs[0]
        assert "title" in first, "Missing 'title' in book result"
        assert "authors" in first, "Missing 'authors' in book result"
        assert "description" in first, "Missing 'description' in book result"

@pytest.mark.asyncio
async def test_search_books_profanity(async_test_client):
    """
    If the query contains profanity, we expect HTTP 403.
    """
    payload = {"query": "shit novel"}  # assuming your 'contains_profanity' catches "shit"
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 403, f"Expected 403 for profanity, got {resp.status_code}"

@pytest.mark.asyncio
async def test_search_books_caching(async_test_client):
    """
    Tests caching by calling the same query twice and ensuring
    the second response is identical (assuming your route uses redis).
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

    # If your caching is correct, the results might be identical.
    # We do a basic assertion:
    assert first_data == second_data, "Expected identical responses from cache"

@pytest.mark.asyncio
async def test_search_books_empty_query(async_test_client):
    """
    If the user sends an empty query, route should still return 200 with minimal results.
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
    The exact results can vary, but we check structure.
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
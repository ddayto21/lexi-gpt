# tests/integration/test_integration_search_books.py

import pytest
import pytest_asyncio
import time
import httpx
from pprint import pprint


@pytest.fixture(scope="session")
def base_url():
    """
    The base URL where your FastAPI app is running.
    Adjust the host/port as needed.
    """
    return "http://localhost:8000"


@pytest_asyncio.fixture
async def async_client():
    """
    Provides an httpx.AsyncClient instance that automatically
    closes at test completion.
    """
    # Increase timeouts for all operations (connect, read, write)
    # e.g. 10 seconds total
    timeout = httpx.Timeout(20.0, read=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        yield client


@pytest.mark.asyncio
async def test_basic_query(base_url, async_client):
    """
    Tests a simple query (e.g. 'mystery'), ensuring the API responds quickly
    and returns the 'recommendations' field.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books/", json={"query": "mystery"}
    )
    elapsed = time.monotonic() - start

    print(f"[test_basic_query] API call took {elapsed:.2f} seconds")

    assert response.status_code == 200
    data = response.json()

    assert "recommendations" in data


@pytest.mark.asyncio
async def test_complex_query(base_url, async_client):
    """
    Tests a more complex query with multiple descriptors.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books/",
        json={"query": "fantasy magic with a strong female lead, published after 2000"},
    )
    elapsed = time.monotonic() - start

    print(f"[test_complex_query] API call took {elapsed:.2f} seconds")

    assert response.status_code == 200
    data = response.json()
    print(data)
    assert "recommendations" in data


@pytest.mark.asyncio
async def test_profanity_query(base_url, async_client):
    """
    Expects a 403 if profanity is detected in the query.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books/", json={"query": "badword"}
    )
    elapsed = time.monotonic() - start

    print(f"[test_profanity_query] API call took {elapsed:.2f} seconds")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_no_results(base_url, async_client):
    """
    Tests a query that should yield zero or minimal results.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books/", json={"query": "jibberish123xyz"}
    )
    elapsed = time.monotonic() - start

    print(f"[test_no_results] API call took {elapsed:.2f} seconds")

    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

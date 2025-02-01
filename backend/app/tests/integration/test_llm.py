import os
import pytest
import pytest_asyncio
import httpx

@pytest.fixture(scope="session")
def base_url():
    """
    Base URL where the FastAPI app is running.
    Uses API_URL environment variable if set, otherwise defaults to localhost.
    """
    return os.getenv("API_URL", "http://localhost:8000")

@pytest_asyncio.fixture
async def async_client():
    """
    Provides an httpx.AsyncClient instance that will be closed automatically.
    """
    async with httpx.AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_llm_refine_valid_query(base_url, async_client):
    """
    Tests that the /llm/refine endpoint returns a valid refined query
    when provided with a proper API key and query parameter.
    """
    api_key = os.getenv("INTERNAL_API_KEY")
    url = f"{base_url}/llm/refine"
    payload = {"query": "some test query"}
    response = await async_client.post(url, json=payload, headers={"X-API-Key": api_key})
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    expected = {"refined_query": "some test query refined"}
    # Note: In our route handler, we currently return f"{query} refined".
    assert data == expected, f"Expected {expected}, got {data}"

@pytest.mark.asyncio
async def test_llm_refine_missing_api_key(base_url, async_client):
    """
    Tests that a request to /llm/refine without the API key is forbidden.
    """
    url = f"{base_url}/llm/refine?query=some%20test%20query"
    response = await async_client.post(url)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"

@pytest.mark.asyncio
async def test_llm_enhance_valid_books(base_url, async_client):
    """
    Tests that the /llm/enhance endpoint returns enhanced book data when provided
    with a valid API key and a list of books.
    """
    api_key = os.getenv("INTERNAL_API_KEY")
    url = f"{base_url}/llm/enhance"
    # Use a sample payload (a bare list) that fits the expected schema.
    payload = [
        {
            "title": "Sample Book",
            "authors": ["Author One"],
            "description": "A brief description"
        }
    ]
    response = await async_client.post(url, json=payload, headers={"X-API-Key": api_key})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    # Given the endpoint returns {"enhanced_books": books},
    # we expect the response to wrap the payload under "enhanced_books".
    expected = {"enhanced_books": payload}
    assert data == expected, f"Expected {expected}, got {data}"

@pytest.mark.asyncio
async def test_llm_enhance_missing_api_key(base_url, async_client):
    """
    Tests that a request to /llm/enhance without an API key returns 403.
    """
    url = f"{base_url}/llm/enhance"
    # In this test, we send the payload as a dictionary with key "books" because it
    # demonstrates another common usage pattern. Adjust according to your endpoint.
    payload = {
        "books": [
            {
                "title": "Sample Book",
                "authors": ["Author One"],
                "description": "A brief description"
            }
        ]
    }
    response = await async_client.post(url, json=payload)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
import os
import time
import pytest
import pytest_asyncio
import httpx
from pydantic import BaseModel, create_model

import json

@pytest.fixture(scope="session")
def base_url():
    """
    The base URL where the FastAPI app is running.
    Uses API_URL from environment variables, defaults to localhost.
    """
    url = os.getenv("API_URL", "http://localhost:8000")
    print(f"Using API base URL: {url}")
    return url


@pytest_asyncio.fixture
async def async_client():
    """
    Provides an httpx.AsyncClient instance with increased timeouts.
    """
    timeout = httpx.Timeout(20.0, read=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        yield client


@pytest.mark.asyncio
async def test_complex_query_generate_model(base_url, async_client):
    """
    Calls the /search_books endpoint and uses the response structure
    to dynamically generate a Pydantic model.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books",
        json={"query": "fantasy magic with a strong female lead, published after 2000"},
    )
    elapsed = time.monotonic() - start
    print(f"[test_complex_query] API call took {elapsed:.2f} seconds")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "recommendations" in data

    # Option 1: Generate a dynamic model using create_model.
    # For each key in the response, infer its type and mark it as required.
    fields = {k: (type(v), ...) for k, v in data.items()}
    DynamicResponseModel = create_model("DynamicResponseModel", **fields)

    # Validate the response by parsing it with the new model.
    model_instance = DynamicResponseModel(**data)
    print("Dynamic Model Instance:", model_instance)

    # Option 2: Print the JSON schema of the generated model for future reference.
    schema = DynamicResponseModel.model_json_schema()
    schema_json = json.dumps(schema, indent=2)
    print("Dynamic Model Schema:")
    print(schema_json)

@pytest.mark.asyncio
async def test_basic_query(base_url, async_client):
    """
    Tests a simple query (e.g. 'mystery') ensuring a 200 response and the presence
    of the 'recommendations' field.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books", json={"query": "mystery"}
    )
    elapsed = time.monotonic() - start
    print(f"[test_basic_query] API call took {elapsed:.2f} seconds")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    print(data)

    assert "recommendations" in data


@pytest.mark.asyncio
async def test_complex_query(base_url, async_client):
    """
    Tests a more complex query with multiple descriptors.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books",
        json={"query": "fantasy magic with a strong female lead, published after 2000"},
    )
    elapsed = time.monotonic() - start
    print(f"[test_complex_query] API call took {elapsed:.2f} seconds")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "recommendations" in data


@pytest.mark.asyncio
async def test_profanity_query(base_url, async_client):
    """
    Expects a 403 response if profanity is detected in the query.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books", json={"query": "badword"}
    )
    elapsed = time.monotonic() - start
    print(f"[test_profanity_query] API call took {elapsed:.2f} seconds")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


@pytest.mark.asyncio
async def test_no_results(base_url, async_client):
    """
    Tests a query that should yield zero or minimal results.
    """
    start = time.monotonic()
    response = await async_client.post(
        f"{base_url}/search_books", json={"query": "jibberish123xyz"}
    )
    elapsed = time.monotonic() - start
    print(f"[test_no_results] API call took {elapsed:.2f} seconds")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

import os
import time
import pytest
import pytest_asyncio
import httpx
from pydantic import BaseModel, create_model
import json

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_URL", "http://localhost:8000")

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_basic_query(base_url, async_client):
    response = await async_client.post(
        f"{base_url}/search_books", json={"query": "mystery"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data

@pytest.mark.asyncio
async def test_profanity_query(base_url, async_client):
    response = await async_client.post(
        f"{base_url}/search_books", json={"query": "badword"}
    )
    assert response.status_code == 403
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
async def test_root(async_test_client):
    """
    Verify GET / returns 200 and the expected JSON:
      {"message": "Welcome to the Book Search API"}.
    """
    response = await async_test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Welcome to the Book Search API"}


@pytest.mark.asyncio
async def test_redis_healthcheck(async_test_client):
    """
    Calls GET /healthcheck/redis to confirm that:
     - The app's startup logic has run and set app.state.book_cache.
     - Redis is reachable.
    """
    response = await async_test_client.get("/healthcheck/redis")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data == {"status": "ok"}

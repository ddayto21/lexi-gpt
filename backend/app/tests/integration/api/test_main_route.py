# tests/test_main_services.py

import pytest
import pytest_asyncio
import httpx
import asyncio
from app.main import app

@pytest_asyncio.fixture
async def async_test_client():
    """
    Creates an AsyncClient with app=app in an ASGITransport.
    Manually calls on_event('startup') and on_event('shutdown').
    This ensures older FastAPI versions can still run the startup 
    and set 'app.state.book_cache' etc.
    """
    # 1) Manually call the startup event(s)
    # In older FastAPI, these handlers live in app.router.on_startup
    # or app.lifespan_context might exist. We'll do the older approach:
    for handler in app.router.on_startup:
        if asyncio.iscoroutinefunction(handler):
            await handler()
        else: 
            handler()

    # 2) Create an in-process test client
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # 3) Manually call the shutdown event(s)
    for handler in app.router.on_shutdown:
        if asyncio.iscoroutinefunction(handler):
            await handler()
        else:
            handler()

@pytest.mark.asyncio
async def test_root(async_test_client):
    """
    Verify GET / returns 200 and the expected JSON:
      {"message": "Welcome to the Book Search API"}.
    Also ensures the on_event('startup') logic has run.
    """
    response = await async_test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Welcome to the Book Search API"}

@pytest.mark.asyncio
async def test_redis_healthcheck(async_test_client):
    """
    Calls GET /healthcheck/redis to confirm that:
     - The app's startup logic ran
     - Redis is actually reachable (no mocking)
    """
    response = await async_test_client.get("/healthcheck/redis")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data == {"status": "ok"}
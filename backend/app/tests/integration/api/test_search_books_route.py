import pytest
import pytest_asyncio
import httpx
from asgi_lifespan import LifespanManager
from app.main import app

@pytest_asyncio.fixture
async def async_test_client():
    """
    Creates an AsyncClient that runs the app's lifespan events.
    Ensures app state is properly initialized before running tests.
    """
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client

@pytest.mark.asyncio
async def test_search_books_normal(async_test_client):
    """
    Tests a normal query to /search_books, expecting 200 and valid book list.
    """
    payload = {"query": "fantasy novel"}
    resp = await async_test_client.post("/search_books", json=payload)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    books = resp.json()
    assert isinstance(books, list), "Expected response to be a list of books"

    if books:
        first = books[0]
        assert "title" in first, "Expected 'title' in book recommendation"
        assert "author" in first, "Expected 'author' in book recommendation"
        assert "year" in first, "Expected 'year' in book recommendation"
        assert "book_id" in first, "Expected 'book_id' in book recommendation"
        assert "subjects" in first, "Expected 'subjects' in book recommendation"


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
async def test_search_books_missing_model(async_test_client):
    """
    If the model is not initialized, the request should return a 500 error.
    """
    # Temporarily remove model from app state
    model_backup = app.state.model
    del app.state.model

    payload = {"query": "mystery book"}
    resp = await async_test_client.post("/search_books", json=payload)
    
    # Restore the model
    app.state.model = model_backup

    assert resp.status_code == 500, f"Expected 500, got {resp.status_code}"
    assert "detail" in resp.json(), "Expected 'detail' key in response"
    assert resp.json()["detail"] == "Server error: Model not initialized."

@pytest.mark.asyncio
async def test_search_books_missing_embeddings(async_test_client):
    """
    If embeddings or metadata are missing, the request should return a 500 error.
    """
    # Temporarily remove embeddings and metadata from app state
    embeddings_backup = app.state.document_embeddings
    metadata_backup = app.state.books_metadata
    del app.state.document_embeddings
    del app.state.books_metadata

    payload = {"query": "science fiction"}
    resp = await async_test_client.post("/search_books", json=payload)

    # Restore embeddings and metadata
    app.state.document_embeddings = embeddings_backup
    app.state.books_metadata = metadata_backup

    assert resp.status_code == 500, f"Expected 500, got {resp.status_code}"
    assert "detail" in resp.json(), "Expected 'detail' key in response"
    assert resp.json()["detail"] == "Server error: Book data not available."

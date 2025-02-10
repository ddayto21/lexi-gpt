# tests/test_book_cache_client.py

import pytest
import time
from app.clients.book_cache_client import BookCacheClient

@pytest.fixture(scope="module")
def cache_client():
    """
    Creates a BookCacheClient connected to a real local Redis.
    Requires redis-server running on localhost:6379.
    """
    client = BookCacheClient()  # default host/port/db
    # Optionally check connectivity
    client.redis.ping()
    yield client
    # Cleanup if needed; e.g. flush the db
    # client.redis.flushdb()  # Uncomment if you want to clear after tests


def test_key_normalization(cache_client):
    """
    Test that the same query, with different spacing/casing,
    maps to the same Redis key.
    """
    normalized1 = cache_client._normalize_key("  The Cat  ")
    normalized2 = cache_client._normalize_key("the cat")
    assert normalized1 == normalized2 == "the cat"


def test_set_and_get_books(cache_client):
    """
    Test storing and retrieving a list of books.
    """
    query = " Mystery   "  # intentionally spaced
    books_data = [{"title": "The Hound of the Baskervilles"}, {"title": "Murder on the Orient Express"}]

    # Ensure key doesn't exist initially
    cache_client.invalidate(query)

    # Confirm TTL is -2 => Key doesn't exist
    assert cache_client.ttl(query) == -2

    # Now set the books with default TTL
    cache_client.set_books(query, books_data)
    # TTL should be > 0 now
    current_ttl = cache_client.ttl(query)
    assert current_ttl > 0, f"Expected a positive TTL after set, got {current_ttl}"

    # Retrieve them
    retrieved = cache_client.get_books(query)
    assert retrieved == books_data, "Expected to retrieve the same books that were set"


def test_custom_ttl(cache_client):
    """
    Test that we can override the default TTL.
    """
    query = "Short TTL Query"
    books_data = [{"title": "Short Lived Book"}]
    cache_client.invalidate(query)

    custom_ttl = 2  # 2 seconds
    cache_client.set_books(query, books_data, ttl=custom_ttl)

    # Immediately check that TTL <= custom_ttl
    current_ttl = cache_client.ttl(query)
    assert 0 < current_ttl <= custom_ttl, f"Expected TTL to be in (0, {custom_ttl}] but got {current_ttl}"

    # Sleep to see expiration
    time.sleep(custom_ttl + 1)
    # Key should be gone
    assert cache_client.get_books(query) is None, "Expected key to expire after custom TTL"


def test_invalidate(cache_client):
    """
    Ensure we can manually invalidate (delete) a cache entry.
    """
    query = "to-delete"
    books = [{"title": "A Book to Remove"}]

    cache_client.set_books(query, books)
    assert cache_client.get_books(query) is not None, "Key should exist initially"

    # Invalidate
    cache_client.invalidate(query)
    assert cache_client.get_books(query) is None, "Key should be removed after invalidate()"
import pytest
import asyncio
from app.services.openlibrary_service import OpenLibraryAPI


@pytest.mark.asyncio
async def test_search_books_valid_query():
    """Test fetching books with a valid search query."""
    service = OpenLibraryAPI()
    query = "The Lord of the Rings"
    results = await service.search(query)

    assert isinstance(results, dict)
    assert "book_search" in results
    assert isinstance(results["book_search"], list)
    assert len(results["book_search"]) > 0
    assert "title" in results["book_search"][0]


@pytest.mark.asyncio
async def test_search_books_empty_query():
    """Test fetching books with an empty search query (should return empty results)."""
    service = OpenLibraryAPI()
    query = ""
    results = await service.search(query)

    assert isinstance(results, dict)
    assert len(results["book_search"]) == 0  # Should return no results


@pytest.mark.asyncio
async def test_search_books_unlikely_query():
    """Test searching for an unlikely query (should return no results)."""
    service = OpenLibraryAPI()
    query = "asdkjfhalskdjfhqpowieurzxcvmnb"  # Random unlikely string
    results = await service.search(query)

    assert isinstance(results, dict)
    assert len(results["book_search"]) == 0  # Should return no results


@pytest.mark.asyncio
async def test_search_authors_valid_query():
    """Test fetching authors with a valid search query."""
    service = OpenLibraryAPI()
    query = "J.K. Rowling"
    results = await service.search(query)

    assert "authors" in results
    assert isinstance(results["authors"], list)
    assert len(results["authors"]) > 0
    assert "name" in results["authors"][0]  # Ensure author name exists


@pytest.mark.asyncio
async def test_search_books_special_characters():
    """Test searching with special characters (should handle gracefully)."""
    service = OpenLibraryAPI()
    query = "!@#$%^&*()_+"
    results = await service.search(query)

    assert isinstance(results, dict)
    assert len(results["book_search"]) == 0  # Expect no results for random symbols

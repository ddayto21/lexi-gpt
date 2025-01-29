import pytest
import httpx
import asyncio
from pprint import pprint

from app.services.openlibrary import OpenLibraryAPI


@pytest.mark.asyncio
async def test_fetch_data_valid_request():
    """Test fetching data from a valid Open Library API endpoint."""
    service = OpenLibraryAPI()
    async with httpx.AsyncClient() as client:
        url = f"{service.base_url}/search.json?q=Harry Potter&limit=1"
        response = await service.fetch_data(client, url)

    assert isinstance(response, dict)
    assert "docs" in response
    assert isinstance(response["docs"], list)
    assert len(response["docs"]) > 0
    assert "title" in response["docs"][0]


@pytest.mark.asyncio
async def test_search_books_valid_query():
    """Test fetching books with a valid search query."""
    pprint("test_search_books_valid_query")
    service = OpenLibraryAPI()
    query = "The Lord of the Rings"
    results = await service.search(query)

    assert isinstance(results, dict)
    assert "book_search" in results
    assert isinstance(results["book_search"], list)
    assert len(results["book_search"]) > 0
    assert "title" in results["book_search"][0]


@pytest.mark.asyncio
async def test_search_books_by_subject_fantasy():
    """Test searching books by the 'fantasy' subject."""
    pprint("test_search_books_by_subject_fantasy")
    service = OpenLibraryAPI()
    results = await service.search(query="", subject="fantasy")
    pprint(results.keys())
    
    for key in results.keys():
        pprint(key)

    assert isinstance(results, dict)
    assert "book_search" in results
    assert isinstance(results["book_search"], list)
    assert len(results["book_search"]) > 0
    assert "title" in results["book_search"][0]

    # assert "fantasy" in results["subjects"]["name"].lower()
    assert 1 == 1


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

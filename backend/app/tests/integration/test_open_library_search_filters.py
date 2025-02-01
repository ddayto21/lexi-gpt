import pytest
import pytest_asyncio
import httpx
import urllib.parse

from app.clients.open_library import OpenLibraryAPI

@pytest.fixture(scope="session")
def base_url():
    return "https://openlibrary.org"

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_search_by_title(async_client):
    """
    Test searching for books by title.
    Example URL: /search.json?title=the+lord+of+the+rings
    """
    service = OpenLibraryAPI()
    title = "the lord of the rings"
    encoded_title = urllib.parse.quote(title)
    url = f"{service.base_url}/search.json?title={encoded_title}"
    data = await service.fetch_data(async_client, url)

    assert isinstance(data, dict)
    assert "docs" in data, "Missing 'docs' key in response"
    assert isinstance(data["docs"], list), "'docs' is not a list"
    assert len(data["docs"]) > 0, "No documents found for title search"
    assert "title" in data["docs"][0], "Document missing 'title' field"

@pytest.mark.asyncio
async def test_search_by_author_sort(async_client):
    """
    Test searching by author and sorting the results.
    Example URL: /search.json?author=tolkien&sort=new
    """
    service = OpenLibraryAPI()
    author = "tolkien"
    url = f"{service.base_url}/search.json?author={urllib.parse.quote(author)}&sort=new"
    data = await service.fetch_data(async_client, url)

    assert isinstance(data, dict)
    assert "docs" in data, "Missing 'docs' key in response"
    assert len(data["docs"]) > 0, "No documents found for author search"
    # Check that at least one document contains an author name.
    assert "author_name" in data["docs"][0], "Document missing 'author_name' field"

@pytest.mark.asyncio
async def test_search_with_language(async_client):
    """
    Test searching with the language parameter.
    Example URL: /search.json?q=harry+potter&lang=fr&limit=1
    """
    service = OpenLibraryAPI()
    query = "harry potter"
    url = f"{service.base_url}/search.json?q={urllib.parse.quote(query)}&lang=fr&limit=1"
    data = await service.fetch_data(async_client, url)

    assert isinstance(data, dict)
    assert "docs" in data, "Missing 'docs' key in response"
    # Even if no French editions are found, docs should be a list.
    assert isinstance(data["docs"], list), "'docs' is not a list"

@pytest.mark.asyncio
async def test_search_page_parameter(async_client):
    """
    Test pagination using the page parameter.
    Example URL: /search.json?q=the+lord+of+the+rings&page=2&limit=1
    """
    service = OpenLibraryAPI()
    query = "the lord of the rings"
    url = f"{service.base_url}/search.json?q={urllib.parse.quote(query)}&page=2&limit=1"
    data = await service.fetch_data(async_client, url)

    assert isinstance(data, dict)
    # The 'start' field should be greater than 0 when page=2.
    assert data.get("start", 0) > 0, "Expected 'start' to be greater than 0 for page 2"

@pytest.mark.asyncio
async def test_search_with_editions(async_client):
    """
    Test fetching edition information using specific fields.
    Example URL:
      /search.json?q=crime+and+punishment&fields=key,title,author_name,editions,editions.key,editions.title,editions.ebook_access,editions.language
    """
    service = OpenLibraryAPI()
    query = "crime and punishment"
    fields = "key,title,author_name,editions,editions.key,editions.title,editions.ebook_access,editions.language"
    encoded_fields = urllib.parse.quote(fields)
    url = f"{service.base_url}/search.json?q={urllib.parse.quote(query)}&fields={encoded_fields}&limit=1"
    data = await service.fetch_data(async_client, url)

    assert isinstance(data, dict)
    assert "docs" in data, "Missing 'docs' key in response"
    assert len(data["docs"]) > 0, "No documents found for editions test"
    
    doc = data["docs"][0]
    # If editions data is present, verify its structure.
    if "editions" in doc:
        editions = doc["editions"]
        assert isinstance(editions, dict), "'editions' is not a dict"
        assert "docs" in editions, "Missing 'docs' key in editions"
        assert isinstance(editions["docs"], list), "Editions 'docs' is not a list"

@pytest.mark.asyncio
async def test_search_with_offset_and_limit(async_client):
    """
    Test pagination using offset and limit parameters.
    Example URL: /search.json?q=harry+potter&offset=10&limit=5
    """
    service = OpenLibraryAPI()
    query = "harry potter"
    url = f"{service.base_url}/search.json?q={urllib.parse.quote(query)}&offset=10&limit=5"
    data = await service.fetch_data(async_client, url)

    assert isinstance(data, dict)
    # Check that docs is a list and that the limit of results is as expected.
    assert "docs" in data, "Missing 'docs' key in response"
    assert isinstance(data["docs"], list), "'docs' is not a list"
    assert len(data["docs"]) <= 5, "Returned more documents than the limit"
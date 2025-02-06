import pytest
import pytest_asyncio
import urllib.parse

from app.clients.open_library_api_client import OpenLibraryAPI


@pytest_asyncio.fixture
async def open_library_client():
    """
    Fixture to provide a reusable OpenLibraryAPI instance.
    Closes the client after all tests in the module have run.
    """
    client = OpenLibraryAPI()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_search_valid_query(open_library_client):
    """
    Tests that a valid query returns a non-empty dictionary with a 'docs' key.
    """
    query = "harry potter"
    # URL encoding is handled inside the client.
    data = await open_library_client.search(query)
    print(data)
    
    # Validate basic structure of the response.
    assert isinstance(data, dict), "Response should be a dict."
    assert "docs" in data, "Response missing 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."
    assert len(data["docs"]) > 0, "Expected at least one document in 'docs'."

    # Optionally, check that the first document contains a title.
    first_doc = data["docs"][0]
    assert "title" in first_doc, "First document should contain a 'title'."


@pytest.mark.asyncio
async def test_search_empty_query_returns_no_results(open_library_client):
    """
    Tests that an empty or unlikely query returns an empty docs array.
    """
    query = "asdfghjklqwertyuiop"
    data = await open_library_client.search(query)

    assert isinstance(data, dict), "Response should be a dict."
    assert "docs" in data, "Response missing 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."

    # For a random string, we expect no results.
    assert len(data["docs"]) == 0, "Expected no documents for an unlikely query."


@pytest.mark.asyncio
async def test_search_query_with_special_characters(open_library_client):
    """
    Tests that queries with spaces and punctuation are handled correctly.
    """
    query = "the lord of the rings: return of the king"
    # Ensure the query is properly URL-encoded internally.
    data = await open_library_client.search(query)

    assert isinstance(data, dict), "Response should be a dict."
    assert "docs" in data, "Response missing 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."
    # We expect some results even if not many.
    assert (
        len(data["docs"]) > 0
    ), "Expected at least one document for a valid query with special characters."

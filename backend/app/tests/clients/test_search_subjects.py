import pytest
import pytest_asyncio
import urllib.parse

from app.clients.open_library_api_client import OpenLibraryAPI


@pytest_asyncio.fixture
async def open_library_client():
    """
    Fixture to provide a reusable OpenLibraryAPI instance.
    Closes the client after each test to avoid event loop issues.
    """
    client = OpenLibraryAPI()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_search_subjects_valid_query(open_library_client):
    """
    Test that a valid subject query returns a properly structured response
    using the search endpoint.

    For example, a query of "love" should be translated into a subject query and
    return a search result with keys like 'docs' and 'numFound'.
    """
    subject_query = "love"
    data = await open_library_client.search_subjects(subject_query)
    # print("Response data:", data.keys())

    # Validate that the response is a dictionary with common search keys.
    assert isinstance(data, dict), "Response should be a dictionary."
    assert "docs" in data, "Response should include 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."
    assert "numFound" in data, "Response should include 'numFound' key."
    assert isinstance(data["numFound"], int), "'numFound' should be an integer."
    # Optionally, if docs are present, check that at least one document has a title.
    if data["docs"]:
        first_doc = data["docs"][0]
        assert "title" in first_doc, "First document should contain a 'title'."


@pytest.mark.asyncio
async def test_search_subjects_multiple_subjects(open_library_client):
    """
    Test that a subject query with multiple comma-separated terms returns a valid response.

    For example, a query of "juvenile fiction, juvenile literature" should be translated
    into an OR query (e.g. subject:( "juvenile fiction" OR "juvenile literature" ))
    and return a search result with keys like 'docs' and 'numFound'.
    """
    subject_query = "juvenile fiction, juvenile literature"
    data = await open_library_client.search_subjects(subject_query)
    # print("Response data:", data)

    # Validate that the response is a dictionary with common search keys.
    assert isinstance(data, dict), "Response should be a dictionary."
    assert "docs" in data, "Response should include 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."
    assert "numFound" in data, "Response should include 'numFound' key."
    assert isinstance(data["numFound"], int), "'numFound' should be an integer."

    # Optionally, if there are results, verify at least one document contains a title.
    if data["docs"]:
        first_doc = data["docs"][0]
        assert "title" in first_doc, "First document should contain a 'title'."


@pytest.mark.asyncio
async def test_search_subjects_empty_query(open_library_client):
    """
    Test that an empty subject query returns an empty dictionary.
    """
    subject_query = ""
    data = await open_library_client.search_subjects(subject_query)
    # Our implementation returns {} when there are no valid terms.
    assert data == {}, "Expected empty dict for an empty query."


@pytest.mark.asyncio
async def test_search_subjects_unlikely_query(open_library_client):
    """
    Test that an unlikely subject query returns no works.
    """
    subject_query = "asldkfjasldkfjasldkfj"
    data = await open_library_client.search_subjects(subject_query)

    assert isinstance(data, dict), "Response should be a dictionary."
    assert "docs" in data, "Response should include 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."
    # Expect no works if the subject is unlikely.
    assert (
        data["numFound"] == 0 or len(data["docs"]) == 0
    ), "Expected no documents for an unlikely subject query."


@pytest.mark.asyncio
async def test_search_subjects_query_with_multiple_terms(open_library_client):
    """
    Test that a query with multiple comma-separated terms is transformed into an OR query.

    For example:
      Input: "juvenile fiction, juvenile literature"
      Should build a query like:
      subject:("juvenile fiction" OR "juvenile literature")
    """
    subject_query = "juvenile fiction, juvenile literature"
    data = await open_library_client.search_subjects(subject_query)

    assert isinstance(data, dict), "Response should be a dictionary."
    assert "docs" in data, "Response should include 'docs' key."
    assert isinstance(data["docs"], list), "'docs' should be a list."
    # We expect that a valid subject query returns some results.
    assert (
        data["numFound"] > 0 or len(data["docs"]) > 0
    ), "Expected some results for a valid multi-term query."

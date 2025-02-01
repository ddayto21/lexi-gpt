import pytest
import pytest_asyncio
import httpx
import urllib.parse
import json

from app.clients.open_library import OpenLibraryAPI
from app.schemas.open_library_api_schema import OpenLibraryResponse

@pytest.mark.asyncio
async def test_open_library_response_model():
    """
    Tests that the response from OpenLibrary's /search.json endpoint conforms
    to the OpenLibraryResponse model.
    """
    service = OpenLibraryAPI()
    query = "Harry Potter"
    encoded_query = urllib.parse.quote(query)
    url = f"{service.base_url}/search.json?q={encoded_query}&limit=1"
    
    async with httpx.AsyncClient() as client:
        response_data = await service.fetch_data(client, url)
    
    # Parse and validate the response using the refined model with Pydantic V2's model_validate.
    parsed_response = OpenLibraryResponse.model_validate(response_data)
    
    # Basic assertions using the typed model:
    assert isinstance(parsed_response.numFound, int)
    assert isinstance(parsed_response.start, int)
    assert isinstance(parsed_response.numFoundExact, bool)
    assert isinstance(parsed_response.num_found, int)
    assert isinstance(parsed_response.documentation_url, str)
    assert isinstance(parsed_response.q, str)
    # offset is defined as Optional[Any] (typically None) – check if it is None or valid.
    assert parsed_response.offset is None or parsed_response.offset is not None
    assert isinstance(parsed_response.docs, list)
    assert len(parsed_response.docs) > 0

    print("Parsed OpenLibraryResponse:", parsed_response)
    # Use model_json_schema to get the JSON Schema and pretty-print it
    schema = parsed_response.model_json_schema()
    print("Model Schema:", json.dumps(schema, indent=2))
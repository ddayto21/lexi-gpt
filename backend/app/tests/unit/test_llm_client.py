import pytest
import asyncio
from app.clients.llm_client import LLMClient


@pytest.mark.asyncio
async def test_local_llm_client():
    client = LLMClient()

    original_query = "The Cat and The Hat"
    refined_query, enhanced_books = await client.process_query(original_query)

    # By default, LLMClient removes "the" and "and" from queries
    # => "Cat Hat"
    assert refined_query == "cat hat", f"Expected 'cat hat', got '{refined_query}'"
    assert isinstance(enhanced_books, list), "enhanced_books should be a list"
    assert len(enhanced_books) > 0, "We expect at least one dummy book"
    assert (
        "title" in enhanced_books[0]
    ), "Expected a 'title' field in the dummy book data"

    await client.close()



@pytest.mark.asyncio
async def test_basic_nlp_cleanup():
    client = LLMClient()
    input_text = "   Hello World!  "
    cleaned = client._basic_nlp_cleanup(input_text)
    assert cleaned == "hello world!", f"Expected 'hello world!', got '{cleaned}'"
    await client.close()


@pytest.mark.asyncio
async def test_extract_entities_and_intent():
    client = LLMClient()
    # Input text that contains a location.
    text = "I am traveling to Paris next summer."
    result = client._extract_entities_and_intent(text)

    # Assert that the places list is not empty and that 'paris' is extracted.
    assert isinstance(result, dict)
    assert "places" in result
    assert isinstance(result["places"], list)
    assert (
        "paris" in result["places"]
    ), f"Expected 'paris' to be in extracted places: {result['places']}"

    # Since genre detection is model‐dependent, at least verify that genres is a list.
    assert "genres" in result
    assert isinstance(result["genres"], list)
    await client.close()


def dummy_text_generator(prompt, max_length, num_return_sequences):
    """
    A dummy text generator function to simulate a fallback scenario.
    Returns an empty generated_text to force fallback logic.
    """
    return [{"generated_text": ""}]


def test_refine_query_fallback(monkeypatch):
    """
    Test that _refine_query() uses the fallback when the text generator returns an empty string.
    """
    client = LLMClient()
    # Override the text generator pipeline with our dummy function.
    monkeypatch.setattr(client, "text_generator", dummy_text_generator)

    extracted = {"genres": ["mystery"], "places": ["paris"]}
    original_text = "mystery novel"
    refined = client._refine_query(original_text, extracted)

    # The fallback builds a query as:
    # "subject:mystery place:paris mystery novel"
    expected = "subject:mystery place:paris mystery novel"
    assert (
        refined == expected
    ), f"Expected fallback refined query '{expected}', got '{refined}'"


@pytest.mark.asyncio
async def test_process_query():
    """
    Test the full process_query() pipeline.
    Note: Since the pipelines use real models, the exact refined query is unpredictable.
    Here we check that a non-empty refined query is returned and that enhanced_books is a list.
    If at least one book is returned, it should contain a 'title' key.
    """
    client = LLMClient()
    query = "I want a mystery novel set in Paris."
    refined_query, enhanced_books = await client.process_query(query)

    # Check that refined_query is a non-empty string.
    assert isinstance(refined_query, str), "refined_query should be a string"
    assert refined_query.strip() != "", "refined_query should not be empty"

    # Check that enhanced_books is a list.
    assert isinstance(enhanced_books, list), "enhanced_books should be a list"

    # If enhanced_books is non-empty, verify at least one expected key in the first book.
    if enhanced_books:
        # This assumes the OpenLibrary API returns a dict with a 'title' field.
        assert (
            "title" in enhanced_books[0]
        ), "Expected a 'title' key in the first book record"

    await client.close()

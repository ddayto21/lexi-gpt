import pytest
import asyncio
from app.clients.llm_client import LLMClient

@pytest.mark.asyncio
async def test_basic_nlp_cleanup():
    """
    Ensures _basic_nlp_cleanup() removes stopwords, lowercases, etc.
    """
    client = LLMClient()
    input_text = "   Hello World!  "
    cleaned = client._basic_nlp_cleanup(input_text)
    # "the" and "and" are in STOPWORDS by default, but "hello" and "world!" remain
    # We only expect them to be lowercased and stripped, punctuation is untouched here
    assert cleaned == "hello world!", f"Expected 'hello world!', got '{cleaned}'"
    await client.close()

@pytest.mark.asyncio
async def test_local_llm_client():
    """
    Checks the end-to-end process_query flow with a short, simple input.
    The query "The Cat and The Hat" should remove 'the' and 'and' -> 'cat hat'.
    The refined query might remain 'cat hat' if the LLM does not add extra keywords.
    """
    client = LLMClient()
    original_query = "The Cat and The Hat"

    refined_query, enhanced_books = await client.process_query(original_query)

    # Confirm that stopwords are removed
    assert refined_query == "cat hat", f"Expected 'cat hat', got '{refined_query}'"
    assert isinstance(enhanced_books, list), "enhanced_books should be a list"
    # We expect the OpenLibrary API to return at least one result
    assert len(enhanced_books) > 0, "Expected at least one book result"
    # Check the first result has a title (typical for OpenLibrary 'docs' entries)
    assert "title" in enhanced_books[0], "Expected a 'title' field in the first book record"

    await client.close()

@pytest.mark.asyncio
async def test_extract_entities_and_intent():
    """
    Verifies that entity extraction (NER) and zero-shot classification
    are invoked successfully and return expected structure.
    """
    client = LLMClient()
    text = "I am traveling to Paris next summer."

    # We call the underlying method that runs actual pipelines in worker threads
    result = await client._extract_entities_and_intent(text)

    assert isinstance(result, dict), "Expected a dictionary from _extract_entities_and_intent"
    assert "places" in result, "Result dict should contain 'places'"
    assert "genres" in result, "Result dict should contain 'genres'"

    # We expect "paris" to be extracted as a place
    places = result["places"]
    assert "paris" in places, f"Expected 'paris' in places; got {places}"

    # Genre detection is model-dependent; just ensure it returns a list
    genres = result["genres"]
    assert isinstance(genres, list), f"Expected genres to be a list; got {type(genres)}"

    await client.close()

@pytest.mark.asyncio
async def test_refine_query_with_real_generation():
    """
    Tests the _refine_query method using the real T5 text generation model.
    Because the output of a generative model can vary, we only check for
    general properties (non-empty or fallback).
    """
    client = LLMClient()
    original_text = "mystery novel set in Istanbul"
    extracted = {"genres": ["mystery"], "places": ["istanbul"]}

    # We call the actual _refine_query method which triggers text generation.
    refined_query = await client._refine_query(original_text, extracted)

    # If the model's output is valid, it might incorporate "mystery" and "istanbul".
    # Or it might fallback to: "subject:mystery place:istanbul mystery novel set in istanbul"
    # Because we are not mocking, let's check for general correctness:
    assert isinstance(refined_query, str), "Refined query should be a string"
    assert refined_query.strip() != "", "Refined query should not be empty"

    # If we got the fallback, it will start with 'subject:mystery place:istanbul'
    # or if generation was successful, it might be something else. Let's just confirm 
    # it doesn't contain the debugging text from the prompt (which triggers fallback).
    assert "Detected Place(s):" not in refined_query, (
        "We should not see the raw debugging text in the final refined query"
    )
    assert "Original Query:" not in refined_query, (
        "We should not see the raw debugging text in the final refined query"
    )

    await client.close()

@pytest.mark.asyncio
async def test_process_query():
    """
    Tests the full pipeline integration with a more explicit query. 
    Since these are real calls to the pipeline and OpenLibrary,
    the result is partly non-deterministic. We only confirm
    that we get a refined query string and a non-empty docs list (most likely).
    """
    client = LLMClient()
    query = "I want a fantasy novel set in Tokyo."

    refined_query, enhanced_books = await client.process_query(query)

    # Validate the refined query
    assert isinstance(refined_query, str), "Refined query should be a string"
    assert refined_query.strip() != "", "Refined query should not be empty"

    # Validate the returned books
    assert isinstance(enhanced_books, list), "enhanced_books should be a list"
    if enhanced_books:
        # At least check the first item for a title
        assert "title" in enhanced_books[0], "Expected the first book to have a 'title'"

    await client.close()
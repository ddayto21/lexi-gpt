import pytest
import asyncio
from app.clients.llm_client import LLMClient


def fuzzy_contains(expected: str, extracted: set) -> bool:
    """
    Returns True if expected (lowercase) appears as a substring in any of the extracted keywords.
    """
    expected = expected.lower()
    return any(expected in keyword for keyword in extracted)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query, expected_keywords",
    [
        (
            "I need a fantasy novel with dragons and magic",
            {"fantasy", "dragons", "magic"},
        ),
        (
            "I'm searching for a mystery thriller with a detective protagonist",
            {"mystery", "thriller", "detective"},
        ),
        (
            "Looking for a romance novel that explores love and loss",
            {"romance", "love", "loss"},
        ),
        (
            "I want an autobiography about perseverance and success",
            {"autobiography", "perseverance", "success"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_extract_keywords(query, expected_keywords):
    client = LLMClient()
    # Call the external LLM to extract keywords from the query.
    keywords_str = await client.extract_keywords(query)
    print("Original Query:", query)
    print("Extracted keywords:", keywords_str)

    # Normalize: split the returned comma-separated string into a set of lowercase keywords.
    extracted_keywords = {k.strip().lower() for k in keywords_str.split(",")}

    # Verify that each expected keyword is (fuzzily) present.
    missing = {
        exp for exp in expected_keywords if not fuzzy_contains(exp, extracted_keywords)
    }
    assert not missing, f"Missing expected keywords: {missing}"

    await client.close()

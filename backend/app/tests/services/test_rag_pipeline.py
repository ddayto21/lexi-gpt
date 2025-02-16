# tests/services/test_rag_pipeline.py

import pytest
import re

from app.services.rag_pipeline import (
    generate_book_summaries,
    construct_model_prompt,
    construct_messages,
)


def normalize_whitespace(text: str) -> str:
    """
    Collapse multiple whitespace characters into a single space and trim the string.
    """
    return re.sub(r"\s+", " ", text).strip()


def normalize_messages(messages: list) -> list:
    """Return a copy of messages with normalized 'content' fields."""
    return [
        {**msg, "content": normalize_whitespace(msg.get("content", ""))}
        for msg in messages
    ]


def test_generate_book_summaries(retrieved_context_fixture, summaries_fixture):
    """
    When given a list of books, generate_book_summaries should return a list of summaries extracted
    using the preprocess_book function.
    """

    output = generate_book_summaries(retrieved_context_fixture)
    print(output)
    assert output == summaries_fixture


def test_construct_model_prompt(query_fixture, summaries_fixture):
    """
    Test that construct_model_prompt returns a properly formatted prompt string including:
      - The user query,
      - A numbered list of book summaries,
      - Numbered instructions for generating recommendations.
    Whitespace differences are ignored.
    """
    query = query_fixture
    summaries = summaries_fixture

    expected = (
        "User query: 'anime similar to hunter hunter'.\n"
        "\n"
        "Retrieved book details:\n"
        "1. hunter x hunter by yoshihiro togashi (1998). Keywords: magic, hunter, graphic novel\n"
        "2. wild by erin hunter (2003). Keywords: cat, fantasy, fantasy fiction\n"
        "3. inuyasha by rumiko takahashi (1998). Keywords: good evil, magic, teenage girl\n"
        "4. long shadow by erin hunter (2008). Keywords: cat, fantasy, fantasy fiction\n"
        "5. forest secret by erin hunter (2003). Keywords: cat, fantasy, fantasy fiction\n"
        "\n"
        "Instructions:\n"
        "- Provide a JSON array of book recommendations.\n"
        "- Each recommendation must be an object with the following keys:\n"
        "    • title: the book title\n"
        "    • description: a clear, friendly explanation of why the book is relevant to the query\n"
        "- If none of the retrieved books match the query, generate your own recommendations.\n"
        "- Output strictly the JSON array without any additional text."
    )

    output = construct_model_prompt(query, summaries)
    assert normalize_whitespace(output) == normalize_whitespace(expected)


def test_construct_messages(query_fixture, summaries_fixture):
    """
    Test that construct_messages returns a list of two messages:
      1. A system message setting the tone.
      2. A user message containing the prompt from construct_model_prompt.
    Whitespace differences are ignored.
    """
    query = query_fixture
    summaries = summaries_fixture

    prompt = construct_model_prompt(query, summaries)
    expected = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that provides clear and accurate book recommendations and explanations. "
                "Respond in a friendly, concise, and professional manner."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    output = construct_messages(prompt)
    normalized_expected = normalize_messages(expected)
    normalized_output = normalize_messages(output)
    assert normalized_output == normalized_expected

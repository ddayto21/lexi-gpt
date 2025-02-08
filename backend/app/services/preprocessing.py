"""
Module: preprocessing.py
Description: Provides functions for normalizing text and preprocessing raw book metadata
             for embedding generation.
"""

import re
import logging
import spacy

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load spaCy model (ensure it's installed with: poetry run python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")


def normalize_text(text: str) -> str:
    """
    Normalize text by converting to lowercase, removing special characters and extra whitespace,
    then tokenizing, lemmatizing, and removing stopwords using spaCy.

    Args:
        text (str): Input text.

    Returns:
        str: Normalized text.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = " ".join(text.split())
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(tokens)


def subjects_to_string(subjects) -> str:
    """
    Convert subjects to a comma-separated string after normalizing each subject.
    Handles both string and list types.

    Args:
        subjects (str or list): Subjects as a comma-separated string or a list.

    Returns:
        str: Normalized subjects as a single string.
    """
    if isinstance(subjects, str):
        subjects_list = [s.strip() for s in subjects.split(",")]
    elif isinstance(subjects, list):
        subjects_list = subjects
    else:
        subjects_list = []
    
    normalized_subjects = [
        normalize_text(subject) for subject in subjects_list if isinstance(subject, str)
    ]
    return ", ".join(normalized_subjects)


def preprocess_book(book: dict) -> dict:
    """
    Preprocess a single book record by normalizing its core fields:
      - title
      - author
      - subjects
      - year

    Args:
        book (dict): Raw book metadata.

    Returns:
        dict: Dictionary containing normalized book data.
    """
    normalized_book = {}

    normalized_book["title"] = normalize_text(book.get("title", ""))

    # Normalize author; join multiple authors if provided.
    authors = book.get("author", [])
    if isinstance(authors, list):
        normalized_book["author"] = normalize_text(", ".join(authors))
    elif isinstance(authors, str):
        normalized_book["author"] = normalize_text(authors)
    else:
        normalized_book["author"] = ""

    # Process subjects field
    subjects = book.get("subjects", "")
    if isinstance(subjects, str):
        subjects_list = [s.strip() for s in subjects.split(",")]
    elif isinstance(subjects, list):
        subjects_list = subjects
    else:
        subjects_list = []
    normalized_book["subjects"] = subjects_to_string(subjects_list)

    # Process year (convert to string)
    year = book.get("year")
    normalized_book["year"] = str(year) if year is not None else ""

    # Retain book_id unchanged
    normalized_book["book_id"] = book.get("book_id", "")

    return normalized_book


def create_embedding_input(book: dict) -> str:
    """
    Combine normalized book fields into a single text string for embedding generation.

    Args:
        book (dict): Normalized book record.

    Returns:
        str: Textual representation used as input for the embedding model.
    """
    return (
        f"Title: {book['title']}. "
        f"Author: {book['author']}. "
        f"Subjects: {book['subjects']}. "
        f"Year: {book['year']}."
    )
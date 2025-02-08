"""
Module: preprocess_books.py
Description: Provides functions for normalizing text and preprocessing raw book metadata 
             for embedding generation. This module reads a JSON file containing raw book data 
             (grouped by subject), normalizes key fields (title, author, subjects, year), 
             and writes the preprocessed metadata to an output file.
"""

import json
import logging
import re
from pathlib import Path
import spacy

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Load the spaCy model (ensure you have run: poetry run python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")


def normalize_text(text: str) -> str:
    """
    Normalize input text using spaCy by converting to lowercase, removing non-alphanumeric 
    characters and extra whitespace, then tokenizing, lemmatizing, and removing stopwords.
    
    Args:
        text (str): Raw input text.
    
    Returns:
        str: Normalized text.
    """
    if not isinstance(text, str):
        return ""
    # Lowercase and remove any characters that are not letters or digits.
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = " ".join(text.split())
    
    # Use spaCy to tokenize, lemmatize, and remove stopwords.
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return " ".join(tokens)


def normalize_subjects(subjects) -> str:
    """
    Normalize the subjects field. Accepts either a comma-separated string or a list of subject strings.
    
    Args:
        subjects (str or list): The subjects as a string or list.
    
    Returns:
        str: A comma-separated string of normalized subjects.
    """
    if isinstance(subjects, str):
        # Split a comma-separated string into a list.
        subjects_list = [s.strip() for s in subjects.split(",")]
    elif isinstance(subjects, list):
        subjects_list = subjects
    else:
        subjects_list = []
    
    # Normalize each subject using the shared normalization function.
    normalized_list = [normalize_text(subject) for subject in subjects_list if isinstance(subject, str)]
    return ", ".join(normalized_list)


def preprocess_book_record(book: dict) -> dict:
    """
    Preprocess a single book record. This function supports multiple input formats:
      - If the key 'work_id' is present, the record is assumed to come from the raw metadata file.
      - If the key 'book_id' is present, the record is assumed to already be in a standardized format.
    
    The following fields are processed:
      - book_id: extracted from 'work_id' or 'book_id'
      - title: normalized text
      - author: if the record has an 'author' field (a string or list) it is normalized; 
                if it has an 'authors' field (list of dict or strings), the first author is used.
      - subjects: normalized subjects field (using comma separation)
      - year: converted to string (from 'year' or 'first_publish_year')
    
    Args:
        book (dict): Raw book metadata.
    
    Returns:
        dict: Preprocessed book record with normalized fields.
    """
    processed = {}
    
    # Book ID: try "book_id" first, otherwise use "work_id"
    processed["book_id"] = book.get("book_id") or book.get("work_id", "")
    
    # Normalize title
    title = book.get("title", "")
    processed["title"] = normalize_text(title)
    
    # Process author information.
    if "author" in book:
        authors = book.get("author", "")
        if isinstance(authors, list):
            # Join multiple authors into a single string.
            author_text = ", ".join(authors)
        elif isinstance(authors, str):
            author_text = authors
        else:
            author_text = ""
    elif "authors" in book:
        authors = book.get("authors", [])
        if authors:
            # Use the first available author.
            first_author = authors[0]
            if isinstance(first_author, dict):
                author_text = first_author.get("name", "")
            elif isinstance(first_author, str):
                author_text = first_author
            else:
                author_text = ""
        else:
            author_text = ""
    else:
        author_text = ""
    processed["author"] = normalize_text(author_text)
    
    # Normalize subjects
    subjects = book.get("subjects", "")
    processed["subjects"] = normalize_subjects(subjects)
    
    # Process publication year
    year = book.get("year") or book.get("first_publish_year")
    processed["year"] = str(year) if year is not None else ""
    
    return processed


def generate_embedding_input(book: dict) -> str:
    """
    Generate a single string that combines normalized book fields into a format suitable for 
    embedding generation.
    
    Args:
        book (dict): Preprocessed book record.
    
    Returns:
        str: A string containing book information.
    """
    return (
        f"Title: {book.get('title', '')}. "
        f"Author: {book.get('author', '')}. "
        f"Subjects: {book.get('subjects', '')}. "
        f"Year: {book.get('year', '')}."
    )


def load_and_preprocess_books(file_path: str) -> list:
    """
    Load raw book metadata from a JSON file and preprocess each record.
    The JSON file is expected to be a dictionary mapping subject categories to lists of books.
    
    Args:
        file_path (str): Path to the raw metadata JSON file.
    
    Returns:
        list: A list of preprocessed book records.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        logging.error(f"Error loading raw data from {file_path}: {e}")
        return []
    
    preprocessed_books = []
    
    # Iterate over each subject category and its associated list of books.
    for subject, books in raw_data.items():
        logging.info(f"Processing subject category: {subject}")
        for book in books:
            if not isinstance(book, dict):
                logging.warning(f"Skipping invalid book record for subject '{subject}': {book}")
                continue
            processed_book = preprocess_book_record(book)
            preprocessed_books.append(processed_book)
    
    return preprocessed_books


def main():
    """
    Main function to run the book metadata preprocessing pipeline.
    It loads raw book data, preprocesses each record, prints the preprocessed data,
    and writes the output to a JSON file.
    """
    # Adjust the base and data directories according to your project structure.
    BASE_DIR = Path(__file__).resolve().parent.parent  
    DATA_DIR = BASE_DIR / "app" / "data" / "book_metadata"

    input_file = DATA_DIR / "subject_metadata.json"
    output_file = DATA_DIR / "book_metadata_preprocessed.json"
    
    logging.info(f"Loading raw book data from {input_file}")
    books_metadata = load_and_preprocess_books(str(input_file))
    
    # (Optional) Print embedding-ready inputs for each book.
    # for book in books_metadata:
    #     print(generate_embedding_input(book))
    
    # Print preprocessed metadata for inspection.
    print(json.dumps(books_metadata, indent=4))
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(books_metadata, f, indent=4)
        logging.info(f"Preprocessed book metadata saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving preprocessed book metadata: {e}")


if __name__ == "__main__":
    main()
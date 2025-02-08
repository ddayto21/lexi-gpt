import json
import re
import logging
from pathlib import Path

import spacy
from sentence_transformers import SentenceTransformer


# Dataset size:  5121

# Configure logging with a clear format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Determine the project’s base directory (adjust .parent count as needed)
BASE_DIR = Path(__file__).resolve().parent.parent  # adjust if necessary
DATA_DIR = BASE_DIR / "app" / "data" / "book_metadata"

# Define file paths using relative paths
VECTOR_DATA_FILE = DATA_DIR / "vector_data.json"
EMBEDDING_INPUTS_FILE = DATA_DIR / "embedding_inputs.json"
PREPROCESSED_OUTPUT_FILE = DATA_DIR / "preprocessed_vector_data.json"
BOOKS_METADATA_FILE = DATA_DIR / "books_metadata.json"
EMBEDDINGS_OUTPUT_FILE = DATA_DIR / "embedding_outputs.json"

# poetry run python -m spacy download en_core_web_sm

# Load the spaCy model for text normalization
nlp = spacy.load("en_core_web_sm")


def normalize_text(text: str) -> str:
    """
    Normalize text by converting to lowercase, removing special characters and extra whitespace,
    then tokenize, lemmatize, and remove stopwords using spaCy.
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
    Preprocess a single book record by normalizing its core fields: title, author, subjects, and year.

    Args:
        book (dict): The raw book metadata.

    Returns:
        dict: A dictionary containing normalized values.
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

    # Process subjects
    subjects = book.get("subjects", "")
    if isinstance(subjects, str):
        subjects_list = [s.strip() for s in subjects.split(",")]
    elif isinstance(subjects, list):
        subjects_list = subjects
    else:
        subjects_list = []
    normalized_book["subjects"] = subjects_to_string(subjects_list)

    # Process year
    year = book.get("year")
    normalized_book["year"] = str(year) if year is not None else ""

    # Retain book_id as is
    normalized_book["book_id"] = book.get("book_id", "")

    return normalized_book


def create_embedding_input(book: dict) -> str:
    """
    Combines the normalized fields into a single text string for the document embedding input.
    """
    return (
        f"Title: {book['title']}. "
        f"Author: {book['author']}. "
        f"Subjects: {book['subjects']}. "
        f"Year: {book['year']}."
    )


def preprocess_main():
    """
    Preprocess the raw vector data to generate:
      - A file with preprocessed book metadata.
      - A separate file with combined text (embedding inputs).

    These files are saved as JSON.
    """
    try:
        with open(VECTOR_DATA_FILE, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    except Exception as e:
        logging.error(f"Error loading dataset from {VECTOR_DATA_FILE}: {e}")
        return

    preprocessed_books = []
    embedding_inputs = []

    for book in dataset:
        preprocessed = preprocess_book(book)
        preprocessed_books.append(preprocessed)
        embedding_inputs.append(create_embedding_input(preprocessed))

    logging.info(f"Preprocessed {len(preprocessed_books)} books.")

    # Save embedding inputs and preprocessed metadata to files
    try:
        with open(EMBEDDING_INPUTS_FILE, "w", encoding="utf-8") as f:
            json.dump(embedding_inputs, f, indent=4)
        logging.info(f"Saved embedding inputs to {EMBEDDING_INPUTS_FILE}")
    except Exception as e:
        logging.error(f"Error saving embedding inputs: {e}")

    try:
        with open(PREPROCESSED_OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(preprocessed_books, f, indent=4)
        logging.info(f"Saved preprocessed book data to {PREPROCESSED_OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Error saving preprocessed book data: {e}")


def create_vector_embeddings(books: list) -> list:
    """
    Generate vector embeddings for a list of books using a pre-trained SentenceTransformer model.
    """
    model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
    embeddings = model.encode(books)
    return embeddings


def add_embedding_input_to_book_metadata():
    """
    Integrate the embedding input text into each preprocessed book record and save
    the combined records as the final books metadata file.
    """
    try:
        with open(PREPROCESSED_OUTPUT_FILE, "r", encoding="utf-8") as f:
            preprocessed_books = json.load(f)
        with open(EMBEDDING_INPUTS_FILE, "r", encoding="utf-8") as f:
            embedding_inputs = json.load(f)
    except Exception as e:
        logging.error(f"Error loading preprocessed files: {e}")
        return

    if len(preprocessed_books) != len(embedding_inputs):
        logging.error(
            "Mismatch in the number of preprocessed books and embedding inputs."
        )
        return

    for i, book in enumerate(preprocessed_books):
        book["embedding_input"] = embedding_inputs[i]

    try:
        with open(BOOKS_METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(preprocessed_books, f, indent=4)
        logging.info(f"Saved combined book metadata to {BOOKS_METADATA_FILE}")
    except Exception as e:
        logging.error(f"Error saving combined book metadata: {e}")


def main_create_embeddings():
    """
    Generate vector embeddings from the embedding input text and save them as JSON.
    """
    try:
        with open(EMBEDDING_INPUTS_FILE, "r", encoding="utf-8") as f:
            embedding_inputs = json.load(f)
    except Exception as e:
        logging.error(
            f"Error loading embedding inputs from {EMBEDDING_INPUTS_FILE}: {e}"
        )
        return

    # Initialize the embedding model (you may choose another model if desired)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vector_embeddings = model.encode(embedding_inputs)

    try:
        with open(EMBEDDINGS_OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(vector_embeddings.tolist(), f, indent=4)
        logging.info(f"Saved vector embeddings to {EMBEDDINGS_OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Error saving vector embeddings: {e}")


def main():
    """
    Main execution flow for generating embeddings:
      1. Preprocess raw vector data to generate embedding inputs.
      2. Integrate embedding inputs into book metadata.
      3. Generate and save vector embeddings.
    """
    logging.info("Starting preprocessing pipeline...")
    preprocess_main()
    add_embedding_input_to_book_metadata()
    main_create_embeddings()
    logging.info("Pipeline execution completed.")


if __name__ == "__main__":
    main()

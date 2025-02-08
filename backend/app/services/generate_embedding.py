"""
Module: generate_embeddings.py
Description: Pipeline for generating book embeddings. This script preprocesses raw data,
             integrates textual embedding inputs into book metadata, and generates vector embeddings
             using a pre-trained SentenceTransformer model.
"""

import json
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Import preprocessing functions from preprocessing.py
from backend.app.services.preprocess_books import preprocess_book, create_embedding_input

# Configure logging with a clear format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Determine project base directory using relative paths (adjust the number of parents as needed)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data" / "book_metadata"

# Define file paths using relative paths
VECTOR_DATA_FILE = DATA_DIR / "vector_data.json"
EMBEDDING_INPUTS_FILE = DATA_DIR / "embedding_inputs.json"
PREPROCESSED_OUTPUT_FILE = DATA_DIR / "preprocessed_vector_data.json"
BOOKS_METADATA_FILE = DATA_DIR / "books_metadata.json"
EMBEDDINGS_OUTPUT_FILE = DATA_DIR / "embedding_outputs.json"


def preprocess_main():
    """
    Preprocess the raw vector data to generate:
      - Preprocessed book metadata.
      - Combined text inputs for embedding generation.
    
    Both outputs are saved as JSON files.
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

    # Save embedding inputs
    try:
        with open(EMBEDDING_INPUTS_FILE, "w", encoding="utf-8") as f:
            json.dump(embedding_inputs, f, indent=4)
        logging.info(f"Saved embedding inputs to {EMBEDDING_INPUTS_FILE}")
    except Exception as e:
        logging.error(f"Error saving embedding inputs: {e}")

    # Save preprocessed book metadata
    try:
        with open(PREPROCESSED_OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(preprocessed_books, f, indent=4)
        logging.info(f"Saved preprocessed book data to {PREPROCESSED_OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"Error saving preprocessed book data: {e}")


def add_embedding_input_to_book_metadata():
    """
    Integrate the textual embedding input into each preprocessed book record and save the final
    combined book metadata.
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
        logging.error("Mismatch in the number of preprocessed books and embedding inputs.")
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
    Generate vector embeddings from the textual embedding inputs and save them as JSON.
    """
    try:
        with open(EMBEDDING_INPUTS_FILE, "r", encoding="utf-8") as f:
            embedding_inputs = json.load(f)
    except Exception as e:
        logging.error(f"Error loading embedding inputs from {EMBEDDING_INPUTS_FILE}: {e}")
        return

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
      1. Preprocess raw data to create embedding inputs.
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
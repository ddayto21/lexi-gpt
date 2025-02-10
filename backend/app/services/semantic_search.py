import json
import logging

import numpy as np
import pandas as pd

import torch
from sentence_transformers import SentenceTransformer, util

from typing import List, Dict, Any, Optional

from pathlib import Path
from app.pipelines.load import (
    load_book_embeddings,
    load_book_metadata,
    save_book_embeddings,
)


def create_vector_embedding(
    model: SentenceTransformer, text: str, device: str = "cpu"
) -> np.ndarray:
    """
    Generate a vector embedding for a given text using a SentenceTransformer model.

    Args:
        model (SentenceTransformer): A SentenceTransformer model instance.
        text (str): Input text to embed.
        device (str): Device to use for encoding (e.g., "cpu" or "cuda").

    Returns:
        np.ndarray: Vector embedding for the input text.
    """
    print("[*] Creating vector embedding for the input text...")

    processed_text = text.lower()
    # Encode the text using the model
    with torch.no_grad():
        embeddings = model.encode([processed_text], device=device).astype("float32")
    return embeddings


def create_book_embeddings(
    model: SentenceTransformer, book_metadata: List[Dict[str, Any]], device: str = "cpu"
):
    """
    Generate vector embeddings for each record in the book corpus and save them as a JSON file.
    """

    return np.vstack(
        [
            create_vector_embedding(model, book["embedding_input"], device)
            for book in book_metadata
        ]
    )


def calculate_similarity_scores(
    query_embedding: np.ndarray, document_embeddings: np.ndarray
) -> torch.Tensor:
    """
    Calculate cosine similarity scores between a search query embedding and document embeddings.
    Returns:
        torch.Tensor: Cosine similarity scores as a tensor.
    """
    # Compute cosine similarities using pre-trained SentenceTransformer model
    similarities = util.cos_sim(query_embedding, document_embeddings)
    return similarities


def get_top_k_books(
    similarity_tensor: torch.Tensor, books_metadata: list, k: int = 5
) -> list:
    """
    Retrieve the top-k books based on similarity scores.

    Args:
        similarity_tensor (torch.Tensor): Cosine similarity scores (shape: [1, num_books]).
        books_metadata (list): List of book metadata dictionaries.
        k (int): Number of top results to retrieve.

    Returns:
        list: List of top-k book metadata dictionaries.
    """
    # Convert the tensor to a numpy array for easier processing
    scores_array = similarity_tensor[0].cpu().numpy()
    # Get indices of the top-k highest scores
    top_indices = np.argsort(scores_array)[::-1][:k]
    logging.info(f"Top indices: {top_indices}")
    # Map the indices back to the stored metadata
    return [books_metadata[i] for i in top_indices]


def main():
    """
    Main function to load data, compute similarities, and display top related books.
    """
    # Initialize the SentenceTransformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    device = "cpu" if not torch.cuda.is_available() else "cuda"

    # Load book embeddings and metadata
    book_embeddings = load_book_embeddings(BOOK_EMBEDDINGS_FILE)
    book_metadata = load_book_metadata(BOOK_METADATA_FILE)

    #  Explicitly check if book_embeddings is empty
    if book_embeddings is not None and book_embeddings.size > 0:
        logging.info("Loaded book embeddings...")

    else:
        logging.info("Cannot load book embeddings, generating new vectors...")

        logging.info("Encoding book embeddings for corpus...")
        book_embeddings = create_book_embeddings(model, book_metadata, device)

        print("Book embeddings:", book_embeddings)
        print("Book embeddings shape:", book_embeddings.shape)
        print("Book embeddings type:", type(book_embeddings))

        logging.info("Saving book embeddings...")
        save_book_embeddings(book_embeddings, BOOK_EMBEDDINGS_FILE)

    # Define the search query
    search_query = "I am looking for a book that contains information about maximizing my potential and doubling my income by learning valuable skills"
    logging.info("Processing search query...")

    # Encode search query iinto vector embedding
    query_embedding = create_vector_embedding(model, search_query, device)

    # Compute similarity scores between query and document embeddings
    similarity_tensor = calculate_similarity_scores(query_embedding, book_embeddings)
    logging.info(f"Similarity tensor: {similarity_tensor}")

    # Retrieve and display the top related books
    top_books = get_top_k_books(similarity_tensor, book_metadata, k=5)
    logging.info("Top related books:")

    for idx, book in enumerate(top_books, start=1):
        logging.info(f"{idx}. {book['title']} by {book['author']}")


if __name__ == "__main__":
    # Configure logging for detailed output
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Determine the base directory of project.
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Construct file paths relative to the base directory.
    BOOK_EMBEDDINGS_FILE = (
        BASE_DIR / "app" / "data" / "book_metadata" / "book_embeddings.json"
    )
    BOOK_METADATA_FILE = (
        BASE_DIR / "app" / "data" / "book_metadata" / "book_metadata.json"
    )

    print(f"Embeddings file path: {BOOK_EMBEDDINGS_FILE}")
    print(f"Book metadata file path: {BOOK_METADATA_FILE}")

    main()

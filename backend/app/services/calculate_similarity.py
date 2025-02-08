import json
import logging
import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from pathlib import Path


def load_book_embeddings(file_path: str) -> np.ndarray:
    """
    Load book embeddings from a JSON file as a NumPy array.

    Args:
        file_path (str): Path to the JSON file containing embeddings.

    Returns:
        np.ndarray: Array of embeddings cast to float32.
    """
    try:
        df = pd.read_json(file_path)
        logging.info(f"Loaded embeddings with shape {df.shape}")
        return df.to_numpy().astype("float32")
    except Exception as e:
        logging.error(f"Error loading embeddings from {file_path}: {e}")
        raise


def load_books_metadata(file_path: str) -> list:
    """
    Load book metadata from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing book metadata.

    Returns:
        list: List of book metadata dictionaries.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        logging.info(f"Loaded metadata for {len(metadata)} books.")
        return metadata
    except Exception as e:
        logging.error(f"Error loading books metadata from {file_path}: {e}")
        raise


def calculate_similarity_scores(
    search_query: str, embeddings_array: np.ndarray
) -> torch.Tensor:
    """
    Calculate cosine similarity scores between a search query and the book embeddings.

    Args:
        search_query (str): The user’s search query.
        embeddings_array (np.ndarray): NumPy array of precomputed book embeddings.

    Returns:
        torch.Tensor: Cosine similarity scores as a tensor.
    """
    # Lowercase the query to ensure consistency
    search_query_processed = search_query.lower()
    # Encode the query and cast to float32 for consistency with embeddings
    search_query_embedding = model.encode([search_query_processed]).astype("float32")
    # Compute cosine similarities using the SentenceTransformer utility
    similarities = util.cos_sim(search_query_embedding, embeddings_array)
    return similarities


def get_top_k_books(
    similarities: torch.Tensor, books_metadata: list, k: int = 5
) -> list:
    """
    Retrieve the top-k books based on similarity scores.

    Args:
        similarities (torch.Tensor): Cosine similarity scores (shape: [1, num_books]).
        books_metadata (list): List of book metadata dictionaries.
        k (int): Number of top results to retrieve.

    Returns:
        list: List of top-k book metadata dictionaries.
    """
    # Convert the tensor to a numpy array for easier processing
    scores = similarities[0].cpu().numpy()
    # Get indices of the top-k highest scores
    top_indices = np.argsort(scores)[::-1][:k]
    logging.info(f"Top indices: {top_indices}")
    # Map the indices back to the stored metadata
    return [books_metadata[i] for i in top_indices]


def main():
    """
    Main function to load data, compute similarities, and display top related books.
    """
    # Load embeddings and metadata
    embeddings_array = load_book_embeddings(EMBEDDINGS_FILE)
    books_metadata = load_books_metadata(BOOKS_METADATA_FILE)

    # Define the search query
    search_query = (
        "I am looking for an anime book with a genius mastermind protagonist "
        "that is cunning and manipulative"
    )
    logging.info("Processing search query...")

    # Compute similarity scores
    similarity_tensor = calculate_similarity_scores(search_query, embeddings_array)
    logging.info(f"Similarity tensor: {similarity_tensor}")

    # Retrieve and display the top related books
    top_books = get_top_k_books(similarity_tensor, books_metadata, k=5)
    logging.info("Top related books:")
    for idx, book in enumerate(top_books, start=1):
        logging.info(f"{idx}. {book['title']} by {book['author']}")


if __name__ == "__main__":
    # Configure logging for detailed output
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Determine the base directory of your project.
    # Adjust the number of .parent calls as needed.
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Construct file paths relative to the base directory.
    EMBEDDINGS_FILE = (
        BASE_DIR / "app" / "data" / "book_metadata" / "embedding_outputs.json"
    )
    BOOKS_METADATA_FILE = (
        BASE_DIR / "app" / "data" / "book_metadata" / "books_metadata.json"
    )

    print(f"Embeddings file path: {EMBEDDINGS_FILE}")
    print(f"Books metadata file path: {BOOKS_METADATA_FILE}")
    # Initialize the SentenceTransformer model globally
    model = SentenceTransformer("all-MiniLM-L6-v2")

    main()

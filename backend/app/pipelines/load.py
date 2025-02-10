import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

import numpy as np
import pandas as pd


def load_json_file(filepath: str) -> Dict[str, Any]:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load JSON file {filepath}: {e}")
        return {}


def save_subjects_metadata(subjects: List[str], filepath: Path) -> None:
    """
    Saves a list of subjects to a JSON file.
    """
    try:
        with filepath.open("w", encoding="utf-8") as file:
            json.dump({"subjects": subjects}, file, indent=4)
        logging.info(f"Subjects successfully saved to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save subjects to {filepath}: {e}")


def save_book_metadata(books: List[Dict[str, Any]], filepath: Path) -> None:
    """
    Stores a list of book metadata to a JSON file.

    """
    try:
        with filepath.open("w", encoding="utf-8") as file:
            json.dump(books, file, indent=4)
        logging.info(f"Books successfully saved to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save books to {filepath}: {e}")


def save_book_embeddings(vector_embeddings: np.ndarray, filepath: Path) -> None:
    """
    Stores vector embeddings for book corpus into a JSON file.

    """
    try:
        with filepath.open("w", encoding="utf-8") as file:
            json.dump(vector_embeddings.tolist(), file, indent=4)
        logging.info(f"Vector embeddings saved to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save vector embeddings to {filepath}: {e}")


def load_book_embeddings(filepath: str) -> np.ndarray:
    """
    Load book embeddings from a JSON file as a NumPy array.

    Args:
        file_path (str): Path to the JSON file containing embeddings.

    Returns:
        np.ndarray: Array of embeddings cast to float32.
    """
    try:
        df = pd.read_json(filepath)
        logging.info(f"Loaded embeddings with shape {df.shape}")
        return df.to_numpy().astype("float32")
    except Exception as e:
        logging.error(f"Error loading embeddings from {filepath}: {e}")


def load_book_metadata(filepath: str) -> list:
    """
    Load book metadata from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing book metadata.

    Returns:
        list: List of book metadata dictionaries.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        logging.info(f"Loaded metadata for {len(metadata)} books.")
        return metadata
    except Exception as e:
        logging.error(f"Error loading books metadata from {filepath}: {e}")

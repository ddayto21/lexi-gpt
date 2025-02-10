"""
Module: extract.py
Description: Provides functions for extracting book metadata from Open Library's API and web pages.
"""

import requests
import json
import logging
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List, Dict, Any, Optional

from app.pipelines.load import (
    save_subjects_metadata,
    load_json_file,
    save_book_metadata,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"

# Set project base directory using relative paths (adjust the number of parents as needed)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "app" / "data" / "book_metadata"

# Define file paths using relative paths
SUBJECTS_FILE = DATA_DIR / "subjects.json"
BOOKS_FILE = DATA_DIR / "books.json"


def extract_subjects(
    url: str = f"{OPEN_LIBRARY_BASE_URL}/subjects",
) -> List[str]:
    """
    Fetches a list of book subjects from Open Library's subject page.
    """
    logging.info(f"Fetching subjects from {url}")

    try:
        with requests.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve subjects from {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    subjects = {
        a_tag.get_text(strip=True)
        for a_tag in soup.find_all("a", href=True)
        if a_tag["href"].startswith("/subjects/") and a_tag.get_text(strip=True)
    }

    logging.info(f"Successfully scraped {len(subjects)} unique subjects.")
    return sorted(subjects)


def extract_books(
    subject: str, limit: int = 100, offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Retrieves books categorized under a specific subject from Open Library.

    Returns:
        List[Dict[str, Any]]: A list of book metadata.
    """
    formatted_subject = subject.lower().replace(" ", "_")
    url = f"{OPEN_LIBRARY_BASE_URL}/subjects/{formatted_subject}.json?limit={limit}&offset={offset}"

    logging.info(f"Fetching books for subject: {subject} ({url})")

    try:
        with requests.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve books for subject {subject}: {e}")
        return []

    books = [
        {
            "work_id": work.get("key", "").replace("/works/", ""),
            "title": work.get("title", "Unknown Title"),
            "authors": [
                author.get("name", "Unknown") for author in work.get("authors", [])
            ],
            "subjects": work.get("subject", []),
            "first_publish_year": work.get("first_publish_year", "N/A"),
            "description": (
                work.get("description", {}).get("value", "No description available")
                if isinstance(work.get("description"), dict)
                else work.get("description", "No description available")
            ),
        }
        for work in data.get("works", [])
    ]

    logging.info(f"Retrieved {len(books)} books for subject '{subject}'.")
    return books


def fetch_book_metadata(work_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves metadata for a specific book using its work ID.

    Args:
        work_id (str): The Open Library work ID.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing book metadata, or None if the request fails.
    """
    url = f"{OPEN_LIBRARY_BASE_URL}/works/{work_id}.json"

    logging.info(f"Fetching metadata for work ID: {work_id}")

    try:
        with requests.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch metadata for work {work_id}: {e}")
        return None

    metadata = {
        "key": data.get("key"),
        "title": data.get("title"),
        "subtitle": data.get("subtitle"),
        "description": (
            data.get("description", {}).get("value")
            if isinstance(data.get("description"), dict)
            else data.get("description")
        ),
        "subjects": data.get("subjects", []),
        "authors": data.get("authors", []),
        "covers": data.get("covers", []),
        "created": (
            data.get("created", {}).get("value")
            if isinstance(data.get("created"), dict)
            else data.get("created")
        ),
    }

    return metadata


if __name__ == "__main__":
    logging.info("Starting book metadata collection pipeline...")

    # Step 1: Check if subjects file already exists before scraping
    subjects_data = load_json_file(SUBJECTS_FILE)
    subjects = subjects_data.get("subjects", [])
    if subjects:

        logging.info(
            f"Subject data found. Skipping subject extraction. ({len(subjects)} subjects)"
        )

    else:
        logging.info("Subjects data not found. Fetching subjects from Open Library...")
        subjects = extract_subjects()
        if subjects:
            save_subjects_metadata(subjects, SUBJECTS_FILE)
        else:
            logging.warning("No subjects found, skipping subject save.")

    # Step 2: Fetch books for each subject and save results
    if subjects:
        books_data = {}
        for subject in subjects:
            books = extract_books(subject, limit=100)
            books_data[subject] = books

        save_book_metadata(books_data, BOOKS_FILE)

    logging.info("Book metadata collection pipeline completed successfully.")

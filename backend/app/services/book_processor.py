# app/services/book_processor.py

from typing import List, Dict
from app.schemas.search_books import Book

def process_results(results: Dict) -> List[Book]:
    """
    Convert OpenLibrary docs into Book schema (title, authors, description).
    """
    book_docs = results.get("docs", [])
    books_data = []
    for doc in book_docs:
        title = doc.get("title", "Untitled")
        # For "authors", combine "author_name" if it exists, else fallback
        authors = doc.get("author_name", [])
        # Some doc fields might have a "first_sentence" or "description" 
        # but often these are missing or nested. Use a fallback:
        description = doc.get("first_sentence") or ""

        # You might need to handle "description" as a dict 
        # doc.get("first_sentence", {}).get("value", "")
        
        books_data.append(Book(
            title=title, 
            authors=authors, 
            description=description
        ))
    return books_data
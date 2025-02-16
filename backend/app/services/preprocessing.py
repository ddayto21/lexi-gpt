# app/services/preprocessing.py


def preprocess_book(book: dict) -> str:
    """
    Optimizes book details into a concise summary containing only the essential information.

    Args:
        book (dict): A dictionary with book details (e.g., title, author, year, subjects).

    Returns:
        str: A concise, formatted summary string.
    """
    title = book.get("title", "Unknown Title").strip()
    author = book.get("author", "Unknown Author").strip()
    year = book.get("year", "Unknown Year").strip()

    # Assume subjects is a comma-separated string; split it and take the top 3 keywords.
    subjects = book.get("subjects", "")
    keywords = ", ".join([s.strip() for s in subjects.split(",") if s.strip()][:3])

    return f"{title} by {author} ({year}). Keywords: {keywords}"

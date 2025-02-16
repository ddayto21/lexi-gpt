# app/services/preprocessing.py


# Preprocess book details
def preprocess_book(book: dict) -> str:
    # Extract and format only the necessary details
    title = book.get("title", "Unknown Title")
    author = book.get("author", "Unknown Author")
    year = book.get("year", "Unknown Year")
    # Assume subjects is a comma-separated string; split, filter, and join the most relevant ones.
    subjects = book.get("subjects", "")
    # For simplicity, take the first three keywords after splitting
    keywords = ", ".join(subject.strip() for subject in subjects.split(",")[:3])
    return f"{title} by {author} ({year}). Keywords: {keywords}"

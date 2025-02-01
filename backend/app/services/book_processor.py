from typing import List, Dict


def process_results(results: Dict) -> List[Dict]:
    """
    Process OpenLibrary API results by extracting relevant book data.
    Assumes the raw data contains a key 'book_search' with docs.
    """
    book_docs = results.get("book_search", [])
    books_data = []
    for doc in book_docs:
        title = doc.get("title", "Untitled")
        authors = doc.get("author_name", [])
        first_sentence = doc.get("first_sentence", "")

        description = (
            first_sentence.get("value", "")
            if isinstance(first_sentence, dict)
            else first_sentence
        )
        books_data.append(
            {"title": title, "authors": authors, "description": description}
        )
    return books_data

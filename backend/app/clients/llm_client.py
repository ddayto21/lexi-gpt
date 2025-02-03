# app/clients/llm_client.py

import re
from typing import List, Dict, Any
from app.clients.open_library import OpenLibraryAPI

class LLMClient:
    """
    1. Removes stopwords (basic text cleanup).
    2. Extracts keywords (genre, place, etc.) from the user's query (Step 1: Query Understanding).
    3. Uses OpenLibraryAPI to search for relevant books (Step 2: Query Generation).
       - e.g., "mystery novel set in Paris" -> "subject:mystery place:paris"
    4. (Step 3, Summaries) is not fully implemented here, focusing on step 1 & 2 for now.
    """

    STOPWORDS = {"the", "is", "of", "and", "a", "in", "set"}

    # A simple genre dictionary to detect some common genres
    GENRES = {
        "mystery": "mystery",
        "romance": "romance",
        "fantasy": "fantasy",
        "science-fiction": "science fiction",
        "sci-fi": "science fiction",
        "thriller": "thriller",
        "horror": "horror",
        "historical": "historical",
        "novel": "novel"
    }

    # A naive place dictionary for demonstration
    PLACES = {
        "paris": "paris",
        "istanbul": "istanbul",
        "rome": "rome",
        "tokyo": "tokyo"
    }

    def __init__(self):
        # We’ll make direct calls to OpenLibraryAPI
        self.open_library = OpenLibraryAPI()

    def _basic_nlp_cleanup(self, text: str) -> List[str]:
        """
        1) Lowercases
        2) Splits on whitespace
        3) Removes a small set of stopwords
        Returns a list of tokens
        """
        tokens = text.lower().split()
        filtered = [t for t in tokens if t not in self.STOPWORDS]
        return filtered

    def _extract_keywords(self, tokens: List[str]) -> Dict[str, Any]:
        """
        Extracts simple fields from tokens: genre(s), place(s), etc.

        e.g. "mystery novel set in paris" -> 
            genre: "mystery", "novel"
            place: "paris"
        """
        found_genres = []
        found_places = []
        leftover_tokens = []

        for t in tokens:
            if t in self.GENRES:
                found_genres.append(self.GENRES[t])  # e.g. 'mystery'
            elif t in self.PLACES:
                found_places.append(self.PLACES[t])  # e.g. 'paris'
            else:
                leftover_tokens.append(t)

        return {
            "genres": list(set(found_genres)),  # deduplicate
            "places": list(set(found_places)),
            "leftover": leftover_tokens
        }

    def _build_openlibrary_query(self, keywords: Dict[str, Any]) -> str:
        """
        Builds a final search string for Open Library based on extracted keywords.
        For instance:
          subject:mystery place:paris leftover tokens -> "subject:mystery place:paris leftover1 leftover2"
        """
        parts = []

        # Add each found genre as subject
        if keywords["genres"]:
            for g in keywords["genres"]:
                parts.append(f"subject:{g}")

        # Add each found place
        if keywords["places"]:
            for p in keywords["places"]:
                parts.append(f"place:{p}")

        # Add leftover tokens at the end
        if keywords["leftover"]:
            parts.extend(keywords["leftover"])

        # Join them with spaces. 
        # Example: "subject:mystery place:paris novel"
        return " ".join(parts)

    async def process_query(self, user_query: str):
        """
        Step 1: Parse & Extract Keywords
        Step 2: Build an OpenLibrary query
        Step 2 (cont’d): Use the OpenLibraryAPI to fetch relevant books
        Step 3: Summarize each book (placeholder - focusing on Step 2 for now).
        """
        # 1. Basic cleanup
        tokens = self._basic_nlp_cleanup(user_query)

        # 2. Extract keywords
        extracted = self._extract_keywords(tokens)
        # e.g. {"genres":["mystery"], "places":["paris"], "leftover":["novel"]}

        # 3. Build final OL query
        refined_query = self._build_openlibrary_query(extracted)
        # e.g. "subject:mystery place:paris novel"

        # 4. Fetch data from OpenLibrary
        search_results = await self.open_library.search(refined_query)
        # search_results -> a dict with "docs" etc.

        # For demonstration, just returning the raw search results under 'enhanced_books'.
        # Step 3 (Summaries) could parse these and produce a summary.
        enhanced_books = search_results.get("docs", [])

        # Return the "refined" OL query plus the raw docs as "enhanced_books"
        return refined_query, enhanced_books

    async def close(self):
        """
        No external client or resource to close here, but we keep this 
        to maintain consistency if other code awaits LLMClient.close().
        """
        pass
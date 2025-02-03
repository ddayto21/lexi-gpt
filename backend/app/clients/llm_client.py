# app/clients/llm_client.py

import re
from typing import List, Dict, Any
from app.clients.open_library import OpenLibraryAPI
from transformers import pipeline

class LLMClient:
    """
    This client implements a pipeline to process a user's query into a refined
    search string by integrating several pre-trained models:
      1. Preprocessing: Normalize the input text.
      2. Entity Extraction: Use a NER pipeline to extract locations (and other entities if needed).
      3. Intent & Genre Detection: Use a zero-shot classifier to detect likely genres.
      4. Query Refinement: Use a text-generation pipeline to expand/refine the query.
    """

    # A simple set of stopwords used for additional cleanup.
    STOPWORDS = {"the", "is", "of", "and", "a", "in", "set"}

    # A list of candidate genre labels for the classifier.
    GENRE_CANDIDATES = [
        "mystery",
        "romance",
        "fantasy",
        "science fiction",
        "thriller",
        "horror",
        "historical",
        "novel",
        "biography",
        "non-fiction",
        "self-help",
        "young adult",
        "children",
        "poetry",
        "drama",
        "adventure"
    ]

    def __init__(self):
        # Initialize the OpenLibrary API client.
        self.open_library = OpenLibraryAPI()
        
        # Load Hugging Face pipelines.
        # NER pipeline to extract location-related entities.
        self.ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
        
        # Zero-shot classification to detect genres from the query.
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        
        # Text-to-text generation for query expansion/refinement.
        # Here, T5 is used; you could replace it with another generation model if desired.
        self.text_generator = pipeline("text2text-generation", model="t5-small")

    def _basic_nlp_cleanup(self, text: str) -> str:
        """
        Normalize the input text by stripping extra whitespace, lowercasing,
        and removing stopwords.
        """
        text = text.strip().lower()
        tokens = text.split()
        filtered_tokens = [t for t in tokens if t not in self.STOPWORDS]
        return " ".join(filtered_tokens)

    def _extract_entities_and_intent(self, text: str) -> Dict[str, Any]:
        """
        Uses the NER pipeline to extract location-related entities and
        the zero-shot classifier to determine likely genres (intent).
        Returns a dict with potential genres and places.
        """
        # Run NER to extract entities (we filter for location-related entities)
        ner_results = self.ner_pipeline(text)
        places = []
        for entity in ner_results:
            # The 'entity_group' can be LOC or GPE (geo-political entity)
            if entity["entity_group"] in ["LOC", "GPE"]:
                places.append(entity["word"].lower())
        places = list(set(places))  # deduplicate

        # Run zero-shot classification on the original text for genre detection.
        classification = self.classifier(text, candidate_labels=self.GENRE_CANDIDATES)
        # Pick the top label if its score is high enough (threshold can be tuned)
        top_genre = classification["labels"][0] if classification["scores"][0] > 0.5 else None
        genres = [top_genre] if top_genre else []

        return {
            "genres": genres,
            "places": places
        }

    def _refine_query(self, original_text: str, extracted: Dict[str, Any]) -> str:
        """
        Combines the original text with the extracted entities and genres,
        and then uses a text-generation model to expand the query into a refined search string.
        If the generated output contains extra debugging text, the method falls back
        to simply returning the cleaned original query plus any extracted keywords.
        """
        # Build a prompt that informs the model what to do.
        prompt = (
            f"Refine the following book search query by including additional relevant keywords "
            f"based on the detected genre and location. \n\n"
            f"Original Query: '{original_text}'\n"
            f"Detected Genre(s): {', '.join(extracted.get('genres', [])) if extracted.get('genres') else 'None'}\n"
            f"Detected Place(s): {', '.join(extracted.get('places', [])) if extracted.get('places') else 'None'}\n\n"
            f"Refined Query:"
        )
        # Generate the refined query.
        generated = self.text_generator(prompt, max_length=50, num_return_sequences=1)
        refined = generated[0]['generated_text'].strip()

        # If the generated text contains extra debugging info, fallback to a simple approach.
        if not refined or "Detected Place(s):" in refined or "Original Query:" in refined:
            parts = []
            for genre in extracted.get("genres", []):
                parts.append(f"subject:{genre}")
            for place in extracted.get("places", []):
                parts.append(f"place:{place}")
            parts.append(original_text)
            refined = " ".join(parts)

        return refined

    async def process_query(self, user_query: str):
        """
        Pipeline Flow:
          1. Preprocess the query.
          2. Extract entities (locations) and intent (genre).
          3. Use the extracted info to refine and expand the query.
          4. Use the refined query to fetch data from the OpenLibrary API.
        Returns a tuple of (refined_query, enhanced_books).
        """
        # 1. Preprocessing: Normalize the input text.
        cleaned_text = self._basic_nlp_cleanup(user_query)
        
        # 2. Entity Extraction & Intent Detection:
        extracted = self._extract_entities_and_intent(cleaned_text)
        
        # 3. Query Refinement:
        refined_query = self._refine_query(cleaned_text, extracted)
        
        # 4. Fetch data from OpenLibrary using the refined query.
        search_results = await self.open_library.search(refined_query)
        enhanced_books = search_results.get("docs", [])

        return refined_query, enhanced_books

    async def close(self):
        """
        Placeholder for closing any resources. Currently, there are no
        persistent connections to close.
        """
        pass
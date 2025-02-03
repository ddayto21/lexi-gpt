# app/clients/llm_client.py

import re
from typing import List, Dict, Any
from app.clients.open_library import OpenLibraryAPI
from transformers import pipeline

from app.services.llm_worker import LLMWorker

class LLMClient:
    """
    Offloads CPU-bound LLM pipeline tasks to a ThreadPoolExecutor 
    so the FastAPI event loop stays responsive.
    """

    # A simple set of stopwords used for additional cleanup.
    STOPWORDS = {"the", "is", "of", "and", "a", "in", "set"}

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
        "adventure",
    ]

    def __init__(self):
        # Initialize the OpenLibrary API client.
        self.open_library = OpenLibraryAPI()

        # Load Hugging Face pipelines.
        self.ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.text_generator = pipeline("text2text-generation", model="t5-small")

        # Create a worker that uses a ThreadPoolExecutor to offload inference.
        # Increase max_workers for more concurrency (CPU/GPU resource permitting).
        self.worker = LLMWorker(max_workers=2)

    def _basic_nlp_cleanup(self, text: str) -> str:
        """
        Normalize the input text by stripping extra whitespace, lowercasing,
        and removing stopwords.
        """
        text = text.strip().lower()
        tokens = text.split()
        filtered_tokens = [t for t in tokens if t not in self.STOPWORDS]
        return " ".join(filtered_tokens)

    def _pipeline_ner(self, text: str) -> List[dict]:
        """
        Synchronous call to the NER pipeline, intended to be run in a thread.
        """
        return self.ner_pipeline(text)

    def _pipeline_zero_shot(self, text: str) -> dict:
        """
        Synchronous call to the zero-shot classifier.
        """
        return self.classifier(text, candidate_labels=self.GENRE_CANDIDATES)

    def _pipeline_text_generation(self, prompt: str) -> str:
        """
        Synchronous call to the text generator, returning just the generated text.
        """
        generated = self.text_generator(prompt, max_length=50, num_return_sequences=1)
        return generated[0]["generated_text"].strip()

    async def _extract_entities_and_intent(self, text: str) -> Dict[str, Any]:
        """
        Asynchronously runs the NER pipeline and zero-shot classifier in separate threads.
        """
        # Run NER in a thread
        ner_results = await self.worker.run_inference(self._pipeline_ner, text)
        places = []
        for entity in ner_results:
            # The 'entity_group' can be LOC or GPE (geo-political entity)
            if entity["entity_group"] in ["LOC", "GPE"]:
                places.append(entity["word"].lower())
        places = list(set(places))

        # Run zero-shot classification in a thread
        classification = await self.worker.run_inference(self._pipeline_zero_shot, text)
        top_genre = classification["labels"][0] if classification["scores"][0] > 0.5 else None
        genres = [top_genre] if top_genre else []

        return {"genres": genres, "places": places}

    async def _refine_query(self, original_text: str, extracted: Dict[str, Any]) -> str:
        """
        Asynchronously run text generation in a thread.
        """
        prompt = (
            f"Refine the following book search query by including additional relevant keywords "
            f"based on the detected genre and location.\n\n"
            f"Original Query: '{original_text}'\n"
            f"Detected Genre(s): {', '.join(extracted.get('genres', [])) if extracted.get('genres') else 'None'}\n"
            f"Detected Place(s): {', '.join(extracted.get('places', [])) if extracted.get('places') else 'None'}\n\n"
            f"Refined Query:"
        )

        # Offload text generation
        refined = await self.worker.run_inference(self._pipeline_text_generation, prompt)

        # If generation is invalid, do a fallback
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
        # 1. Clean the query
        cleaned_text = self._basic_nlp_cleanup(user_query)
        # 2. Extract
        extracted = await self._extract_entities_and_intent(cleaned_text)
        # 3. Refine
        refined_query = await self._refine_query(cleaned_text, extracted)
        # 4. Search books (this call is already async)
        search_results = await self.open_library.search(refined_query)
        enhanced_books = search_results.get("docs", [])
        return refined_query, enhanced_books

    async def close(self):
        """
        Clean up the thread pool when the app shuts down.
        """
        self.worker.shutdown()
        # No persistent huggingface resources to close, but you can do other cleanup as needed.
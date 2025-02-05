# app/clients/llm_client.py

import re
from typing import List, Dict, Any
from app.clients.open_library import OpenLibraryAPI
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

from app.services.llm_worker import LLMWorker

class LLMClient:
    """
    Offloads CPU-bound LLM pipeline tasks to a ThreadPoolExecutor 
    so the FastAPI event loop stays responsive.

    Now includes a 'generate_queries()' method that uses a local HF model 
    to create multiple related queries, each on a new line.
    """

    STOPWORDS = {"the", "is", "of", "and", "a", "in", "set"}
    GENRE_CANDIDATES = [
        "mystery","romance","fantasy","science fiction","thriller","horror",
        "historical","novel","biography","non-fiction","self-help","young adult",
        "children","poetry","drama","adventure",
    ]

    def __init__(self):
        # Initialize the OpenLibrary API client.
        self.open_library = OpenLibraryAPI()

        # Existing pipelines for NER, zero-shot classification, T5 text generation:
        self.ner_pipeline = pipeline(
            "ner", model="dslim/bert-base-NER", aggregation_strategy="simple"
        )
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
        self.text_generator = pipeline(
            "text2text-generation", model="t5-small"
        )

        # ---- NEW: local text-generation pipeline (e.g. Falcon, GPT-Neo, etc.) ----
        # For demonstration, we assume you have the model "tiiuae/falcon-7b-instruct" locally
        # (downloaded, with enough GPU VRAM). Adjust if you want a smaller model or different approach.
        model_name = "tiiuae/falcon-7b-instruct"  # or another open-source model
        print(f"Loading local generation model: {model_name} ...")
        self.local_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.local_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto"  # uses GPU if available; otherwise CPU
        )
        self.multiple_queries_pipeline = pipeline(
            "text-generation",
            model=self.local_model,
            tokenizer=self.local_tokenizer,
            max_length=200,
            temperature=0.7,
        )
        # ---------------------------------------------------------------------------

        # A worker that uses a ThreadPoolExecutor for CPU/GPU-bound tasks:
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
        """ Synchronous call to the NER pipeline. """
        return self.ner_pipeline(text)

    def _pipeline_zero_shot(self, text: str) -> dict:
        """ Synchronous call to the zero-shot classifier. """
        return self.classifier(text, candidate_labels=self.GENRE_CANDIDATES)

    def _pipeline_text_generation(self, prompt: str) -> str:
        """ Synchronous call to the T5 text generator. """
        generated = self.text_generator(prompt, max_length=50, num_return_sequences=1)
        return generated[0]["generated_text"].strip()

    # ---------------------------------------------------------------------------
    # New local generation logic for multiple queries:
    def _pipeline_multi_query_generation(self, prompt: str) -> str:
        """
        Synchronous call to the local text-generation pipeline (Falcon, GPT-Neo, etc.).
        Returns the raw 'generated_text' from the pipeline's first sequence.
        """
        output = self.multiple_queries_pipeline(prompt, num_return_sequences=1)
        return output[0]["generated_text"]  # raw text

    def generate_queries_sync(self, user_query: str, num_queries: int = 4) -> List[str]:
        """
        *Synchronously* generate multiple queries from the local model pipeline,
        each on a new line, by replicating the 'prompt + newline splitting' logic.
        If you want to run this in a thread pool, see 'generate_queries()' async below.
        """
        prompt = (
            f"You are a helpful assistant that generates {num_queries} distinct search queries "
            f"for the following user request:\n\n"
            f"User Query: '{user_query}'\n\n"
            f"Please list each query on its own line.\n"
            f"Queries:\n"
        )
        raw_output = self._pipeline_multi_query_generation(prompt)
        lines = raw_output.splitlines()
        filtered = []
        found_queries_section = False
        for line in lines:
            if "Queries:" in line:
                found_queries_section = True
                continue
            if found_queries_section:
                line = line.strip()
                if line:
                    filtered.append(line)

        if not filtered:
            filtered = lines
        final_queries = filtered[:num_queries]
        return final_queries

    async def generate_queries(self, user_query: str, num_queries: int = 4) -> List[str]:
        """
        *Asynchronously* generate multiple queries by offloading to the worker.
        """
        prompt = (
            f"You are a helpful assistant that generates {num_queries} distinct search queries "
            f"for the following user request:\n\n"
            f"User Query: '{user_query}'\n\n"
            f"Please list each query on its own line.\n"
            f"Queries:\n"
        )

        def sync_func(prompt: str) -> str:
            # We just call _pipeline_multi_query_generation inside a small helper
            return self._pipeline_multi_query_generation(prompt)

        # 1) run the local text generation in a background thread
        raw_output = await self.worker.run_inference(sync_func, prompt)

        # 2) do the naive line splitting logic
        lines = raw_output.splitlines()
        filtered = []
        found_queries_section = False
        for line in lines:
            if "Queries:" in line:
                found_queries_section = True
                continue
            if found_queries_section:
                line = line.strip()
                if line:
                    filtered.append(line)

        if not filtered:
            filtered = lines
        final_queries = filtered[:num_queries]
        return final_queries
    # ---------------------------------------------------------------------------

    async def _extract_entities_and_intent(self, text: str) -> Dict[str, Any]:
        """Asynchronously runs the NER pipeline and zero-shot classifier."""
        ner_results = await self.worker.run_inference(self._pipeline_ner, text)
        places = []
        for entity in ner_results:
            if entity["entity_group"] in ["LOC", "GPE"]:
                places.append(entity["word"].lower())
        places = list(set(places))

        classification = await self.worker.run_inference(self._pipeline_zero_shot, text)
        top_genre = classification["labels"][0] if classification["scores"][0] > 0.5 else None
        genres = [top_genre] if top_genre else []

        return {"genres": genres, "places": places}

    async def _refine_query(self, original_text: str, extracted: Dict[str, Any]) -> str:
        """Asynchronously run T5 text generation in a thread."""
        prompt = (
            f"Refine the following book search query by including additional relevant keywords "
            f"based on the detected genre and location.\n\n"
            f"Original Query: '{original_text}'\n"
            f"Detected Genre(s): {', '.join(extracted.get('genres', [])) or 'None'}\n"
            f"Detected Place(s): {', '.join(extracted.get('places', [])) or 'None'}\n\n"
            f"Refined Query:"
        )

        refined = await self.worker.run_inference(self._pipeline_text_generation, prompt)
        if not refined or "Detected Place(s):" in refined or "Original Query:" in refined:
            parts = []
            for genre in extracted.get("genres", []):
                parts.append(f"subject:{genre}")
            for place in extracted.get("places", []):
                parts.append(f"place:{place}")
            parts.append(original_text)
            refined = " ".join(parts)
        return refined

    # async def process_query(self, user_query: str):
    #     # 1. Cleanup
    #     cleaned_text = self._basic_nlp_cleanup(user_query)
    #     # 2. Extract
    #     extracted = await self._extract_entities_and_intent(cleaned_text)
    #     # 3. Refine
    #     refined_query = await self._refine_query(cleaned_text, extracted)
    #     # 4. Search books
    #     search_results = await self.open_library.search(refined_query)
    #     enhanced_books = search_results.get("docs", [])
    #     return refined_query, enhanced_books
    async def rewrite_query(self, original_query: str):
        """
        Rewrites the original query by generating multiple related queries.
        """
        # Decompose the query into several queries that are executed in parallel
        

    async def close(self):
        """Clean up resources."""
        self.worker.shutdown()
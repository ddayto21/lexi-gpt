import os
from pathlib import Path
from dotenv import load_dotenv

import asyncio
import logging
import multiprocessing
import signal

import torch

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


from app.api.routes import router
from app.clients.open_library_api_client import OpenLibraryAPI
from app.clients.llm_client import LLMClient
from app.clients.book_cache_client import BookCacheClient
from sentence_transformers import SentenceTransformer
from app.services.semantic_search import load_book_embeddings, load_books_metadata


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDINGS_FILE = BASE_DIR / "app" / "data" / "book_metadata" / "embedding_outputs.json"
BOOKS_METADATA_FILE = (
    BASE_DIR / "app" / "data" / "book_metadata" / "books_metadata.json"
)


# Ensure subprocesses terminate properly
def terminate_subprocesses():
    logging.info("Terminating active subprocesses...")
    for child in multiprocessing.active_children():
        logging.info(f"Terminating subprocess: {child.pid}")
        child.terminate()
        child.join()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for FastAPI."""
    logging.info("Starting application...")

    # Load pre-trained SentenceTransformer model
    try:
        app.state.model = SentenceTransformer("all-MiniLM-L6-v2")
        app.state.device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Model initialized using device: {app.state.device}")
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        app.state.model = None  # Avoids AttributeError in routes

    # Load embeddings & metadata
    try:
        app.state.document_embeddings = load_book_embeddings(str(EMBEDDINGS_FILE))
        app.state.books_metadata = load_books_metadata(str(BOOKS_METADATA_FILE))
        if app.state.document_embeddings is None or app.state.books_metadata is None:
            raise ValueError("Embeddings or metadata failed to load.")
        logging.info(f"Loaded {len(app.state.books_metadata)} books successfully.")
    except Exception as e:
        logging.error(f"Error loading book data: {e}")
        app.state.document_embeddings = None
        app.state.books_metadata = None

    yield  # Application runs here

    # Cleanup GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logging.info("Released CUDA memory.")

    logging.info("Application shutdown complete.")


# Create FastAPI instance
app = FastAPI(lifespan=lifespan, redirect_slashes=False)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://main.d2hvd5sv2imel0.amplifyapp.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Search API"}


@app.get("/healthcheck/redis")
async def redis_healthcheck(request: Request):
    """Checks if Redis is running and reachable."""
    book_cache = request.app.state.book_cache
    if book_cache is None:
        raise HTTPException(status_code=500, detail="Redis is unavailable")
    try:
        book_cache.redis.ping()
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Redis ping failed")


# Include API routes
app.include_router(router)


# Handle OS signals for graceful shutdown
def shutdown_handler(signal_received, frame):
    logging.info(f"Received shutdown signal: {signal_received}. Cleaning up...")
    terminate_subprocesses()
    os._exit(0)


signal.signal(signal.SIGINT, shutdown_handler)  # Handle CTRL+C
signal.signal(signal.SIGTERM, shutdown_handler)  # Handle termination requests

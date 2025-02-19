import os
import signal
import logging
import multiprocessing
from pathlib import Path
from contextlib import asynccontextmanager

import torch
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

from app.config import (
    FRONTEND_ORIGIN,
    BOOK_EMBEDDINGS_FILE,
    BOOK_METADATA_FILE,
    REDIS_URL,
)
from app.api import router as api_router
from app.clients.book_cache_client import BookCacheClient
from app.pipelines.load import load_book_embeddings, load_book_metadata
from app.session_middleware import SessionMiddleware


# Load environment variables early
load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Ensure subprocesses terminate properly
def terminate_subprocesses():
    logging.info("Terminating active subprocesses...")
    for child in multiprocessing.active_children():
        logging.info(f"Terminating subprocess: {child.pid}")
        child.terminate()
        child.join()


# Global resource initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for FastAPI."""
    logging.info("Starting application...")

    # Load pre-trained SentenceTransformer model on startup.
    try:
        app.state.model = SentenceTransformer("all-MiniLM-L6-v2")
        app.state.device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Model initialized using device: {app.state.device}")
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        app.state.model = None  # Avoids AttributeError in routes

    # Load embeddings & metadata or retrieve from cache if available.
    try:

        app.state.document_embeddings = load_book_embeddings(str(BOOK_EMBEDDINGS_FILE))
        app.state.books_metadata = load_book_metadata(str(BOOK_METADATA_FILE))
        if app.state.document_embeddings is None or app.state.books_metadata is None:
            raise ValueError("Embeddings or metadata failed to load.")
        logging.info(f"Loaded {len(app.state.books_metadata)} books successfully.")
    except Exception as e:
        logging.error(f"Error loading book data: {e}")
        app.state.document_embeddings = None
        app.state.books_metadata = None
    # Initialize Redis cache client
    try:
        app.state.book_cache = BookCacheClient()
        logging.info("Redis connection successful.")

    except Exception as e:
        logging.error(f"Failed to connect to Redis: {e}")
        app.state.book_cache = None

    yield  # Application runs here

    # Cleanup GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logging.info("Released CUDA memory.")

    logging.info("Application shutdown complete.")


# Create FastAPI instance
app = FastAPI(lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend domain to make requests
    allow_credentials=True,  # Ensure cookies are sent with requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
    max_age=600,  # Cache preflight response for 10 minutes
)

app.add_middleware(SessionMiddleware)
app.include_router(api_router)


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


# Handle OS signals for graceful shutdown
def shutdown_handler(signal_received, frame):
    logging.info(f"Received shutdown signal: {signal_received}. Cleaning up...")
    terminate_subprocesses()
    os._exit(0)


signal.signal(signal.SIGINT, shutdown_handler)  # Handle CTRL+C
signal.signal(signal.SIGTERM, shutdown_handler)  # Handle termination requests

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
BOOK_EMBEDDINGS_FILE = (
    BASE_DIR / "app" / "data" / "book_metadata" / "book_embeddings.json"
)
BOOK_METADATA_FILE = BASE_DIR / "app" / "data" / "book_metadata" / "book_metadata.json"
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from dotenv import load_dotenv

from app.api.routes import router
from app.clients.open_library_api_client import OpenLibraryAPI
from app.clients.llm_client import LLMClient
from app.clients.book_cache_client import BookCacheClient

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create and attach clients and cache.
    app.state.open_library_client = OpenLibraryAPI()
    app.state.llm_client = LLMClient()
    book_cache = BookCacheClient(default_ttl=3600)
    book_cache.redis.ping()
    app.state.book_cache = book_cache
    yield
    # Shutdown: close clients.
    await app.state.llm_client.close()
    await app.state.open_library_client.close()


app = FastAPI(lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://main.d2hvd5sv2imel0.amplifyapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Search API"}


@app.get("/healthcheck/redis")
async def redis_healthcheck(request: Request):
    book_cache = request.app.state.book_cache
    book_cache.redis.ping()
    return {"status": "ok"}


app.include_router(router)

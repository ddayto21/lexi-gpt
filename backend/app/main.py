# app/main.py

import os
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import public_router
from app.clients.open_library import OpenLibraryAPI
from app.clients.llm_client import LLMClient
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(redirect_slashes=False)

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


def get_redis_client():
    try:
        client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        client.ping()
        return client
    except redis.exceptions.ConnectionError:

        class DummyRedis:
            def get(self, key):
                return None

            def setex(self, key, ttl, value):
                pass

        return DummyRedis()


redis_client = get_redis_client()


@app.on_event("startup")
async def startup_event():
    app.state.open_library_client = OpenLibraryAPI()
    app.state.llm_client = LLMClient()
    app.state.redis_client = redis_client


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.llm_client.close()
    await app.state.open_library_client.close()


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Search API"}


app.include_router(public_router)

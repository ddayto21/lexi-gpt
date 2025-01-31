import os
from fastapi import FastAPI
from app.api.routes import public_router, internal_router
from app.clients.open_library import OpenLibraryAPI
from app.clients.llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Publically available endpoints
app.include_router(public_router)

# Internal endpoints that require an API key
app.include_router(internal_router)


@app.on_event("startup")
async def startup_event():
    llm_refine_endpoint = os.getenv("LLM_REFINE_ENDPOINT", "http://llm-service/refine")
    llm_enhance_endpoint = os.getenv(
        "LLM_ENHANCE_ENDPOINT", "http://llm-service/enhance"
    )
    app.state.open_library_client = OpenLibraryAPI()
    app.state.llm_client = LLMClient(llm_refine_endpoint, llm_enhance_endpoint)


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.llm_client.close()
    await app.state.open_library_client.close()

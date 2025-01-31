from fastapi import FastAPI
from app.api.routes import router as api_router
from app.clients.open_library import OpenLibraryAPI
from app.clients.llm_client import LLMClient

app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    # Pre-initialize external service clients
    app.state.open_library_client = OpenLibraryAPI()
    app.state.llm_client = LLMClient()
    
@app.on_event("shutdown")
async def shutdown_event():
    # Close external service clients if necessary
    await app.state.open_library_client.close()
    await app.state.llm_client.close()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.search_books import router as search_books_router

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(search_books_router)

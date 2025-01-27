from fastapi import FastAPI
from app.api.search_books import router as search_books_router

app = FastAPI()
app.include_router(search_books_router)

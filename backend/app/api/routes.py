from fastapi import APIRouter
from app.api.search_books import router as books_router


router = APIRouter()

router.include_router(books_router, prefix="/search_books", tags=["books"])

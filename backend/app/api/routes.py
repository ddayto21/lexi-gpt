from fastapi import APIRouter
from app.api.search_books import router as books_router
from app.api.health import router as health_router


router = APIRouter()

router.include_router(books_router, prefix="/search_books", tags=["books"])
router.include_router(health_router, prefix="/health", tags=["health"])

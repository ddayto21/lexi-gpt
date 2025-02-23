# app/api/__init__.py
from fastapi import APIRouter
from app.api.chat import router as chat_router
from app.api.books import router as books_router
from app.api.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, tags=["auth"])
router.include_router(chat_router, tags=["chat"])
router.include_router(books_router, tags=["books"])

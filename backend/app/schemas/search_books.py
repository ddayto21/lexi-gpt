from pydantic import BaseModel
from typing import List, Optional


class SearchBooksRequest(BaseModel):
    query: str


class Book(BaseModel):
    title: str
    authors: List[str]
    description: str


class SearchBooksResponse(BaseModel):
    recommendations: List[Book]
    message: Optional[str] = None


class Error(BaseModel):
    code: str
    message: str

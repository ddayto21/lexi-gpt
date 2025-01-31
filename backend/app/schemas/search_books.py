from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    title: str
    authors: List[str]
    description: str


class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    recommendations: List[Book]
    message: Optional[str] = None


class Error(BaseModel):
    code: str
    message: str

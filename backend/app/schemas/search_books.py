from pydantic import BaseModel, Field
from typing import List, Optional


class Book(BaseModel):
    title: str = Field(..., title="Book Title", description="The title of the book")
    author: Optional[str] = Field(
        None, title="Author", description="The author of the book"
    )
    subjects: Optional[List[str]] = Field(
        None, title="Subjects", description="List of subjects the book belongs to"
    )
    year: Optional[str] = Field(
        None, title="Publication Year", description="Year the book was published"
    )
    book_id: Optional[str] = Field(
        None, title="Book ID", description="Unique identifier for the book"
    )


class SearchRequest(BaseModel):
    query: str = Field(
        ..., title="Search Query", description="The query string for book search"
    )


class SearchResponse(BaseModel):
    recommendations: List[Book] = Field(
        ...,
        title="Recommended Books",
        description="List of recommended books based on search query",
    )
    message: Optional[str] = Field(
        None,
        title="Message",
        description="Optional message in case of errors or notifications",
    )


class Error(BaseModel):
    code: str
    message: str

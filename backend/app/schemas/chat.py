from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class ChatPart(BaseModel):
    """Represents a single part of a chat message."""

    type: str = "text"
    text: str


class ChatMessage(BaseModel):
    """Represents a single chat message."""

    id: Optional[str] = None
    role: str
    content: Optional[str] = None
    timestamp: Optional[str] = Field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    parts: Optional[List[ChatPart]] = []


class ChatRequest(BaseModel):
    """Represents the request body for the /chat endpoint."""

    messages: List[ChatMessage]

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ChatPart(BaseModel):
    """
    Represents a single part of a chat message.
    """

    type: str = Field(..., description="The type of message part (e.g. 'text').")
    text: str = Field(..., description="The content text of the message part.")


class ChatMessage(BaseModel):
    """
    Represents a single chat message.
    """

    id: Optional[str] = Field(None, description="Unique identifier for the message.")
    role: str = Field(
        ..., description="The role of the sender (e.g., 'user' or 'assistant')."
    )
    content: str = Field(..., description="The full text content of the message.")
    timestamp: Optional[datetime] = Field(
        None, description="Timestamp when the messsage was created."
    )
    parts: Optional[List[ChatPart]] = Field(
        default_factory=list,
        description="List of message parts for detailed content breakdown.",
    )


class ChatRequest(BaseModel):
    """
    Represents the request body for the /chat endpoint.
    """

    id: Optional[str] = Field(
        None, description="Unique identifier for the chat session."
    )
    messages: List[ChatMessage] = Field(
        ..., description="List of chat messages in the conversation."
    )

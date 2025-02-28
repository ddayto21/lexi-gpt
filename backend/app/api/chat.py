from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import logging
import os
import sys
import uuid
from openai import OpenAI, AsyncOpenAI
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel
from app.schemas.chat import ChatRequest, ChatMessage, ChatPart
import asyncio
from app.services.auth import verify_token
from fastapi import Depends


load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)


# Ensure API Key is set
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not API_KEY:
    raise ValueError(
        "Missing API Key. Set `DEEPSEEK_API_KEY` in environment variables."
    )

# client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")
client = AsyncOpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")


@router.post("/chat")
async def chat(req: ChatRequest):
    system_prompt = ChatMessage(
        role="system",
        content=(
            "You are LexiGPT, a warm and knowledgeable AI librarian. You specialize in book recommendations "
            "and personalized suggestions. You speak in a conversational and engaging way, occasionally "
            "using light humor when appropriate. Always make the user feel heard and valued. "
            "Never be robotic—respond naturally and empathetically."
            "Only give 3 recommendations at most."
            "If you don't have an appropriate recommendation, mention that you don't have enough information to know the answer."
        ),
        timestamp=datetime.utcnow().isoformat(),
        parts=[
            ChatPart(
                type="text",
                text="Only respond with 3 book recommendations.",
            )
        ],
    )

    # Insert system prompt at the beginning of the conversation history
    req.messages.insert(0, system_prompt)

    stream = await client.chat.completions.create(
        model="deepseek-chat",
        messages=req.messages,
        max_tokens=500,
        temperature=0.3,
        stream=True,
    )

    async def generator():
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    response_messages = generator()
    return StreamingResponse(response_messages, media_type="text/event-stream")


@router.get("/chat/messages")
async def get_messages(user=Depends(verify_token)):
    """Fetches messages for the authenticated user."""
    return {"messages": ["Message 1", "Message 2"], "user": user["email"]}

# app/api/auth.py
from fastapi import APIRouter, HTTPException, Request, Depends
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
from app.clients.cache_client import CacheClient, get_cache

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
async def chat(
    req: ChatRequest,
    user=Depends(verify_token),
    cache: CacheClient = Depends(get_cache),
):
    """Stream chat responses and store conversation history in Redis."""
    user_id = user["sub"]
    system_prompt = ChatMessage(
        role="system",
        content=(
            "You are LexiGPT, a warm and knowledgeable AI librarian. You specialize in book recommendations "
            "and personalized suggestions. You speak in a conversational and engaging way, occasionally "
            "using light humor when appropriate. Always make the user feel heard and valued. "
            "Never be robotic—respond naturally and empathetically."
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
    history_key = f"user:{user_id}:chat_history"
    # Last message is the user message
    user_message = req.messages[-1]
    full_response = ""

    async def generator():
        nonlocal full_response
        async for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            yield content
        # After streaming, save the conversation
        turn = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": user_message.content,
            "timestamp": user_message.timestamp,
        }
        cache.redis.lpush(history_key, json.dumps(turn))

        turn = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": full_response,
            "timestamp": datetime.utcnow().isoformat(),
        }
        cache.redis.lpush(history_key, json.dumps(turn))

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.get("/chat/messages")
async def get_messages(
    user=Depends(verify_token), cache: CacheClient = Depends(get_cache)
):
    """Fetch conversation history for the authenticated user."""
    user_id = user["sub"]
    history_key = f"user:{user_id}:chat_history"
    raw_history = cache.redis.lrange(history_key, 0, -1) or []
    messages = [json.loads(entry) for entry in raw_history]
    return {
        "messages": messages[::-1],
        "user": user["email"],
    }  # Reverse to chronological order

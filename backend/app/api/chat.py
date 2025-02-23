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
    stream = await client.chat.completions.create(
        model="deepseek-chat",
        messages=req.messages,
        max_tokens=300,
        temperature=0.3,
        stream=True,
    )

    async def generator():
        async for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    response_messages = generator()
    return StreamingResponse(response_messages, media_type="text/event-stream")

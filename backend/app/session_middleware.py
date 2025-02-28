# app/session_middleware.py

import os
import uuid
import jwt
import datetime
import secrets
from dotenv import load_dotenv
from fastapi import HTTPException, Response, Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

load_dotenv()

# Configuration
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
TOKEN_EXPIRATION_DAYS = 1
ENV = os.environ.get("ENV", "development")
FRONTEND_DOMAIN = os.environ.get("FRONTEND_DOMAIN", "localhost")

logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://main.d2hvd5sv2imel0.amplifyapp.com",
]


def create_session():
    """
    Generates a new session by creating a UUID and encoding it in a JWT.
    The payload always uses "sub" as the identifier.
    """
    session_id = str(uuid.uuid4())
    payload = {
        "sub": session_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=TOKEN_EXPIRATION_DAYS),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return session_id, token


def decode_session(token: str):
    """
    Decodes the JWT token and retrieves the "sub" field.
    """
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_data.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid session token payload")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")


def set_session_cookie(response: Response, token: str):
    """
    Sets the session cookie with attributes based on the environment.
    For local development, the domain attribute is omitted.
    """
    is_production = ENV == "production"
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=True if is_production else False,
        samesite="None" if is_production else "Lax",
        domain=FRONTEND_DOMAIN if is_production else None,
    )


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware that handles session management.
      - Validates the request's Origin header.
      - Attempts to decode an existing session token.
      - Creates a new session if the token is missing or invalid.
      - Stores the session identifier in request.state.session_id.
    """

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        logger.debug(f"Origin: {origin}")
        if origin and origin not in ALLOWED_ORIGINS:
            logger.warning(f"Blocked request from disallowed origin: {origin}")
            raise HTTPException(status_code=403, detail="Origin not allowed.")

        session_token = request.cookies.get("session_token")
        if session_token:
            try:
                user_id = decode_session(session_token)
            except Exception as e:
                logger.warning(f"Invalid or expired session token: {e}")
                user_id, new_token = create_session()
                request.state.session_id = user_id
                response = await call_next(request)
                response.delete_cookie("session_token")
                set_session_cookie(response, new_token)
                return response
        else:
            user_id, new_token = create_session()
            request.state.session_id = user_id
            response = await call_next(request)
            set_session_cookie(response, new_token)
            return response

        request.state.session_id = user_id
        return await call_next(request)

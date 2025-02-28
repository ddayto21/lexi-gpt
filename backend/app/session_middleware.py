# app/session_middleware.py

import uuid
import jwt
import datetime
import secrets
import os
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


def generate_secret_key():
    """Generates a secure random secret key."""
    return secrets.token_hex(32)


def create_session():
    """
    Generates a new session ID and returns an encoded JWT token.
    The payload contains a 'session_id' field used to track the session.
    """
    session_id = str(uuid.uuid4())
    payload = {
        "session_id": session_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=TOKEN_EXPIRATION_DAYS),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return session_id, token


def decode_session(token: str):
    """
    Decodes a JWT token to retrieve the session identifier.
    Returns the 'session_id' if available; otherwise, falls back to 'sub'.
    """
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        session_id = decoded_data.get("session_id") or decoded_data.get("sub")
        if not session_id:
            raise HTTPException(status_code=401, detail="Invalid session token payload")
        return session_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")


def set_session_cookie(response: Response, token: str):
    """
    Sets the session token in a cookie with attributes that depend on the environment.
    In production, uses secure settings (HTTPS, SameSite=None, and a domain restriction).
    """
    is_production = ENV == "production"
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=True if is_production else False,
        samesite="None" if is_production else "Lax",
        domain=FRONTEND_DOMAIN if is_production else "localhost",
    )


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware that manages sessions:
      - Validates the Origin header.
      - Checks for an existing session token in cookies.
      - If present, decodes it; if invalid or absent, creates a new session.
    The session identifier is then stored in request.state.session_id.
    """

    async def dispatch(self, request: Request, call_next):
        # Validate the Origin header for extra security.
        origin = request.headers.get("origin")
        logger.warning(f"Origin: {origin}")
        if origin and origin not in ALLOWED_ORIGINS:
            logger.warning(f"Blocked request from disallowed origin: {origin}")
            raise HTTPException(status_code=403, detail="Origin not allowed.")

        session_token = request.cookies.get("session_token")
        if session_token:
            try:
                session_id = decode_session(session_token)
            except Exception as e:
                logger.warning(f"Invalid or expired session token: {e}")
                # Token is invalid—create a new session and clear the bad cookie.
                session_id, new_token = create_session()
                request.state.session_id = session_id
                response = await call_next(request)
                response.delete_cookie("session_token")
                set_session_cookie(response, new_token)
                return response
        else:
            # No session token exists; create a new session.
            session_id, new_token = create_session()
            request.state.session_id = session_id
            response = await call_next(request)
            set_session_cookie(response, new_token)
            return response

        # Save the valid session identifier for downstream route handlers.
        request.state.session_id = session_id
        return await call_next(request)

# app/session_middleware.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.services.session_manager import (
    create_session,
    decode_session,
    set_session_cookie,
)

import logging

# Configure logging as needed
logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://main.d2hvd5sv2imel0.amplifyapp.com",
]


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Optionally, validate the Origin header for extra security
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
                # Instead of returning an immediate error, allow the request to proceed
                # while deleting the invalid cookie
                response = await call_next(request)
                response.delete_cookie("session_token")
                return response
        else:
            # No token present; create a new session.
            session_id, jwt_token = create_session()
            request.state.session_id = session_id
            response = await call_next(request)
            set_session_cookie(response, jwt_token)
            return response

        # Store session_id in request.state for later use in route handlers
        request.state.session_id = session_id
        return await call_next(request)

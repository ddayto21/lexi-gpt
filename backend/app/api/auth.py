# app/api/auth.py
from fastapi import APIRouter, HTTPException, Request, Depends, Response
from fastapi.responses import RedirectResponse
from app.clients.cache_client import CacheClient, get_cache
from app.services.auth import exchange_code_for_token
import os
import jwt
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ENV = os.environ.get("ENV", "development")
FRONTEND_DOMAIN = os.environ.get("FRONTEND_DOMAIN", "localhost")

ALGORITHM = "HS256"


@router.get("/auth/callback")
async def auth_callback(request: Request, cache: CacheClient = Depends(get_cache)):
    """Handles Google OAuth callback, exchanges code for token, caches user profile, and redirects to /callback."""
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_data = exchange_code_for_token(code)
    google_id_token = token_data.get("id_token")
    if not google_id_token:
        raise HTTPException(
            status_code=401, detail="Failed to retrieve Google ID token"
        )

    try:
        request_session = google_requests.Request()
        id_info = id_token.verify_oauth2_token(
            google_id_token, request_session, GOOGLE_CLIENT_ID
        )

        user_profile = {
            "sub": id_info["sub"],
            "email": id_info["email"],
            "name": id_info.get("name", ""),
            "picture": id_info.get("picture", ""),
        }
        print("user_profile", user_profile)

        redis_key = f"user:{user_profile['sub']}:profile"
        success = cache.set_hash(
            redis_key,
            {
                "email": user_profile["email"],
                "name": user_profile["name"],
                "picture": user_profile["picture"],
            },
        )
        if not success:
            print(f"Failed to cache profile for user {user_profile['sub']}")

        payload = {
            "sub": user_profile["sub"],
            "email": user_profile["email"],
            "name": user_profile["name"],
            "picture": user_profile["picture"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        }
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        is_production = ENV == "production"
        # Redirect to the frontend /callback route
        response = RedirectResponse(url="http://localhost:3000/chat")
        response.set_cookie(
            key="session_token",
            value=jwt_token,
            httponly=True,
            secure=True if is_production else False,
            samesite="None" if is_production else "Lax",
            # domain=FRONTEND_DOMAIN if is_production else "localhost",
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Invalid Google ID token: {str(e)}"
        )


@router.get("/auth/profile")
async def check_auth(request: Request, cache: CacheClient = Depends(get_cache)):
    """Check if user is authenticated and fetch their cached profile."""
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Here we assume the token contains "sub" (as set in auth_callback)
        profile = cache.get_hash(f"user:{decoded_token['sub']}:profile") or {}
        return {
            "message": "Authenticated",
            "user": decoded_token,
            "profile": profile,
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/auth/signout")
async def sign_out(response: Response):
    """
    Sign the user out by deleting the session cookie.
    Returns a JSON message.
    """
    response.delete_cookie("session_token")
    return {"message": "Signed out"}

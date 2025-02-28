# app/api/auth.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from app.clients.cache_client import CacheClient, get_cache
from app.services.auth import exchange_code_for_token
import os
import jwt
import datetime

from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"


@router.get("/auth/callback")
async def auth_callback(request: Request, cache: CacheClient = Depends(get_cache)):
    """Handles Google OAuth callback, exchanges code for token, and caches user profile.

    Args:
        request (Request): The incoming HTTP request with query params.
        cache (CacheClient): Injected Redis cache client for storing user profile.

    Raises:
        HTTPException: If auth code is missing, token retrieval fails, or cache is down.
    """
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_data = exchange_code_for_token(code)

    google_id_token = token_data.get("id_token")
    if not google_id_token:
        raise HTTPException(
            status_code=401, detail="Failed to retrieve Google ID token"
        )

    # Decode Google’s ID token (insecure for demo; verify in production)
    decoded_google_token = jwt.decode(
        google_id_token, options={"verify_signature": False}
    )

    # Extract user profile information from google
    user_profile = {
        "sub": decoded_google_token["sub"],  # Google User ID
        "email": decoded_google_token["email"],
        "name": decoded_google_token.get("name", ""),
    }
    print("user_profile", user_profile)

    # Store user profile data in cache
    redis_key = f"user: {user_profile['sub']}:profile"
    success = cache.set_hash(
        redis_key, {"email": user_profile["email"], "name": user_profile["name"]}
    )
    if not success:
        # Log the failure but don’t block auth—cache is optional for now
        print(f"Failed to cache profile for user {user_profile['sub']}")

    # Generate JWT payload for session token
    payload = {
        "sub": user_profile["sub"],
        "email": user_profile["email"],
        "name": user_profile["name"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }

    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Set JWT in HTTP-only cookie and redirect to chat
    response = RedirectResponse(url="http://localhost:3000/chat")
    response.set_cookie("token", jwt_token, httponly=True, secure=True, samesite="Lax")
    return response


@router.get("/api/auth/status")
async def check_auth(request: Request, cache: CacheClient = Depends(get_cache)):
    """Check if user is authenticated and fetch their cached profile.

    Args:
        request (Request): The incoming HTTP request with cookies.
        cache (CacheClient): Injected Redis cache client for profile retrieval.

    Returns:
        dict: Auth status and user data, including cached profile if available.
    """
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        profile = cache.get_hash(f"user:{decoded_token['sub']}:profile") or {}
        return {"message": "Authenticated", "user": decoded_token, "profile": profile}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

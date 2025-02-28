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
    """
    Handles Google OAuth callback: exchanges the code for a token,
    caches the user's profile, generates a JWT token (with "sub" as the unique identifier),
    and uses the session manager helper to set the session cookie.
    Finally, it redirects the user to the chat page.
    """
    # Step 1: Validate and extract authorization code
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    # Step 2: Exchange authorization code for access token
    token_response = exchange_code_for_token(code)
    google_id_token = token_response.get("id_token")
    if not google_id_token:
        raise HTTPException(
            status_code=401, detail="Failed to retrieve Google ID token"
        )

    try:
        # Step 3: Verify the Google Identify Token
        google_request = google_requests.Request()
        id_info = id_token.verify_oauth2_token(
            google_id_token, google_request, GOOGLE_CLIENT_ID
        )

        # Step 4: Extract user profile information
        user_profile = {
            "sub": id_info["sub"],
            "email": id_info["email"],
            "name": id_info.get("name", ""),
            "picture": id_info.get("picture", ""),
        }

        # Step 5: Cache the user profile information
        cache_key = f"user:{user_profile['sub']}:profile"

        if not cache.set_hash(cache_key, user_profile):
            print(f"Failed to cache profile for user: {user_profile}")

        # Step 6: Generate JWT token with expiration time
        payload = user_profile.copy()
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Step 7: Create redirect response, and set session cookie
        is_production = ENV == "production"
        response = RedirectResponse(url="http://localhost:3000/chat")
        response.set_cookie(
            key="session_token",
            value=jwt_token,
            httponly=True,
            secure=True if is_production else False,
            samesite="None" if is_production else "Lax",
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


@router.delete("/auth/cache")
async def delete_all_user_data(cache: CacheClient = Depends(get_cache)):
    """
    Deletes all user-related data from the cache (keys starting with "user:").
    WARNING: This endpoint is sensitive and should be secured in production.
    """
    try:
        keys_deleted = 0
        # Iterate over all keys matching the pattern "user:*"
        for key in cache.redis.scan_iter("user:*"):
            cache.redis.delete(key)
            keys_deleted += 1
        return {"message": f"Deleted {keys_deleted} user data keys from cache."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error clearing user cache: {str(e)}"
        )

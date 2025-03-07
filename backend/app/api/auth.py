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
import logging
from dotenv import load_dotenv

load_dotenv()

# Validate environment variables at startup
REQUIRED_ENV_VARS = ["JWT_SECRET_KEY", "GOOGLE_CLIENT_ID", "FRONTEND_DOMAIN"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ENV = os.environ.get("ENV", "development")
FRONTEND_DOMAIN = os.environ.get("FRONTEND_DOMAIN", "localhost")

ALGORITHM = "HS256"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get(
    "/auth/callback",
    response_class=RedirectResponse,
    summary="Handle Google OAuth callback",
    description="Exchanges OAuth code for tokens, caches user profile, sets session cookie, and redirects to chat.",
    responses={
        200: {"description": "Redirect to chat page with session cookie set"},
        400: {"description": "Missing authorization code"},
        401: {"description": "Invalid or failed token exchange"},
    },
)
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

    # Step 2: Exchange authorization code for an identity token
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


@router.get(
    "/auth/profile",
    summary="Fetch authenticated user profile",
    description="Verifies the session token and returns the user's profile from cache.",
    responses={
        200: {
            "description": "User profile data",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Authenticated",
                        "user": {"sub": "123"},
                        "profile": {"name": "User"},
                    }
                }
            },
        },
        401: {"description": "Unauthorized or invalid/expired token"},
    },
)
async def check_auth(request: Request, cache: CacheClient = Depends(get_cache)):
    """
    Check if the user is authenticated and fetch their cached profile.

    Args:
        request (Request): The incoming HTTP request with cookies.
        cache (CacheClient): Dependency-injected cache client.

    Returns:
        dict: Authentication status and user profile data.

    Raises:
        HTTPException: If token is missing, expired, or invalid.
    """
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in decoded_token:
            raise HTTPException(status_code=401, detail="Invalid token: missing sub")

        profile = cache.get_hash(f"user:{decoded_token['sub']}:profile") or {
            "sub": decoded_token["sub"],
            "email": decoded_token.get("email", ""),
            "name": decoded_token.get("name", ""),
            "picture": decoded_token.get("picture", ""),
        }
        return {"message": "Authenticated", "user": decoded_token, "profile": profile}
    except jwt.ExpiredSignatureError:
        logger.info("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get(
    "/auth/signout",
    summary="Sign out the user",
    description="Deletes the session cookie and clears user cache.",
    responses={
        200: {
            "description": "Signed out successfully",
            "content": {"application/json": {"example": {"message": "Signed out"}}},
        }
    },
)
async def sign_out(response: Response, cache: CacheClient = Depends(get_cache)):
    """
    Sign the user out by deleting the session cookie and clearing cached profile.

    Args:
        response (Response): The outgoing HTTP response to set cookies.
        cache (CacheClient): Dependency-injected cache client.

    Returns:
        dict: Confirmation message.
    """
    token = response.cookies.get("session_token")
    if token:
        try:
            decoded = jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
            )
            cache_key = f"user:{decoded['sub']}:profile"
            cache.redis.delete(cache_key)
        except jwt.InvalidTokenError:
            pass  # Ignore invalid token during sign-out
    response.delete_cookie("session_token")
    return {"message": "Signed out"}


@router.delete(
    "/auth/cache",
    summary="Delete all user data from cache",
    description="Clears all user-related cache entries. Requires authentication in production.",
    responses={
        200: {
            "description": "Cache cleared",
            "content": {
                "application/json": {
                    "example": {"message": "Deleted 5 user data keys from cache."}
                }
            },
        },
        401: {"description": "Unauthorized"},
        500: {"description": "Cache clearing error"},
    },
)
async def delete_all_user_data(
    request: Request, cache: CacheClient = Depends(get_cache)
):
    """
    Deletes all user-related data from the cache (keys starting with 'user:').

    Args:
        request (Request): The incoming HTTP request with cookies (for auth).
        cache (CacheClient): Dependency-injected cache client.

    Returns:
        dict: Number of keys deleted.

    Raises:
        HTTPException: If unauthorized or cache operation fails.
    """
    if ENV == "production":
        token = request.cookies.get("session_token")
        if not token or not jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]):
            raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        keys_deleted = 0
        for key in cache.redis.scan_iter("user:*"):
            cache.redis.delete(key)
            keys_deleted += 1
        logger.info(f"Deleted {keys_deleted} user cache keys")
        return {"message": f"Deleted {keys_deleted} user data keys from cache."}
    except Exception as e:
        logger.error(f"Cache deletion failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error clearing user cache: {str(e)}"
        )

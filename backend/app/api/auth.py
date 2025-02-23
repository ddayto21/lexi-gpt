from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
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
async def auth_callback(request: Request):
    """ " Handles Google OAuth callback and exchanges code for access token"""
    code = request.query_params.get("code")
    print("code: ", code)

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_data = exchange_code_for_token(code)

    google_id_token = token_data.get("id_token")
    if not google_id_token:
        raise HTTPException(
            status_code=401, detail="Failed to retrieve Google ID token"
        )

    decoded_google_token = jwt.decode(
        google_id_token, options={"verify_signature": False}
    )

    payload = {
        "sub": decoded_google_token["sub"],  # Google User ID
        "email": decoded_google_token["email"],
        "name": decoded_google_token.get("name", ""),
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=7),  # ✅ Expires in 7 days
    }

    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Store access token securely (in HTTP-only cookie)
    response = RedirectResponse(url="http://localhost:3000/chat")
    response.set_cookie("token", jwt_token, httponly=True, secure=True, samesite="Lax")
    return response


@router.get("/api/auth/status")
async def check_auth(request: Request):
    """Check if user is authenticated by verifying the JWT token in cookies."""
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": "Authenticated", "user": decoded_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

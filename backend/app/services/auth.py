from fastapi import HTTPException
import jwt
from fastapi import Header
import requests

import os
from dotenv import load_dotenv

load_dotenv()

# Validate environment variables
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

for var in [
    "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET",
    "GOOGLE_REDIRECT_URI",
    "JWT_SECRET_KEY",
]:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")


def exchange_code_for_token(code: str):
    """
    Exchanges an authorization code for tokens using Google OAuth 2.0 endpoint.

    Args:
        code (str): The authorization code received from the OAuth flow.

    Returns:
        dict: Token data including 'access_token' and 'id_token'.

    Raises:
        HTTPException: If token exchange failes or response is invalid.
    """

    token_uri = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_uri, data=payload)
        response.raise_for_status()

        token_data = response.json()
    except requests.Reques as e:
        raise HTTPException(status_code=500, detail=f"TOken request failed: {str(e)}")

    if "access_token" not in token_data:
        error_description = token_data.get("error_description", "Unknown error")

        raise HTTPException(
            status_code=401, detail=f"Failed to retrieve token: {error_description}"
        )

    return token_data


def verify_token(authorization: str = Header(None)):
    """
    Validates and decodes a JWT token from the Authorization header.

    Args:
        authorization (str, optional): The Authorization header (e.g., "Bearer <token>")

    Returns:
        dict: A decoded token payload containing user profile information.

    Raises:
        HTTPException: If token is missing, expired, or invalid.
    """

    # Step 1: Ensure Authorization header is present
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    try:
        # Step 2: Extract the JWT token from the Authorization header
        token = authorization.split(" ")[1]

        # Step 3: Decode JWT with signature verification
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")

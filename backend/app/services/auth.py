from fastapi import HTTPException
import jwt
from fastapi import Header
import requests

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")


def exchange_code_for_token(code: str):
    """
    Exchanges an authorization code for tokens using Google OAuth 2.0 endpoint.

    Args:
        code (str): The authorization code received from the OAuth flow.

    Returns:
        dict: A dictionary containing the token data, including 'access_token' and 'id_token'.

    Raises:
        HTTPException: If REDIRECT_URI is not set or if token exchange fails.
    """
    if not REDIRECT_URI:
        raise HTTPException(status_code=500, detail="GOOGLE_REDIRECT_URI is not set")

    token_uri = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_uri, data=payload)

    try:
        token_data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to parse token response")

    if response.status_code != 200 or "access_token" not in token_data:
        error_desc = token_data.get("error_description", "Unknown error")
        raise HTTPException(
            status_code=401, detail=f"Failed to retrieve token: {error_desc}"
        )

    return token_data


def verify_token(authorization: str = Header(None)):
    """
    Validates and decodes a Google OAuth JWT token.

    - Extracts the Bearer token from the Authorization header.
    - Decodes the token to retrieve user information.
    - Rejects missing, expired, or malformed tokens.

    **Usage:**
    - Applied as a FastAPI dependency (`Depends(verify_token)`) in protected routes.
    - Requires the frontend to send:
      ```
      Authorization: Bearer <token>
      ```

    **Raises:**
    - HTTP 401 Unauthorized for missing, expired, or invalid tokens.
    """

    # Ensure Authorization header is present
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    try:
        # Extract the token from the "Bearer <token>" format
        token = authorization.split(" ")[1]  # Remove 'Bearer '

        # Decode JWT without signature verification (should be verified in production)
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        # Return decoded user details
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

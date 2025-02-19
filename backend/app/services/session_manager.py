import uuid
import jwt
import datetime
from fastapi import HTTPException, Response, Cookie


import secrets

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
# JWT expiration time
TOKEN_EXPIRATION_DAYS = 1
ENV = os.environ["ENV"]
FRONTEND_DOMAIN = os.environ["FRONTEND_DOMAIN"]


def generate_secret_key():
    return secrets.token_hex(32)


def create_session():
    """
    Generates a new session ID and returns an encoded JWT token.
    """
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    payload = {
        "session_id": session_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=TOKEN_EXPIRATION_DAYS),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return session_id, token


def decode_session(token: str):
    """
    Decodes a JWT and retrieves the session_id.
    """
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_data["session_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")


def set_session_cookie(response: Response, token: str):
    """
    Stores the session token as an HttpOnly, Secure cookie.
    Dynamically configures cookie attributes based on environment.
    """
    is_production = ENV == "production"

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,  # Prevents JavaScript access (XSS protection)
        # secure=is_production,  # Enforces HTTPS in production
        secure=False,
        samesite=(
            "None" if is_production else "Lax"
        ),  # "None" required for cross-origin, "Lax" for local dev
        # domain=(
        #     FRONTEND_DOMAIN if is_production else "localhost"
        # ),  # Restrict cookie to frontend domain
    )


if __name__ == "__main__":
    print(generate_secret_key())

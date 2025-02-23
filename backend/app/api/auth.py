from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.services.auth import exchange_code_for_token

router = APIRouter()


@router.get("/auth/callback")
async def auth_callback(request: Request):
    """ " Handles Google OAuth callback and exchanges code for access token"""
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_data = exchange_code_for_token(code)

    # Store access token securely (in HTTP-only cookie)
    response = RedirectResponse(url="http://localhost:3000/")
    response.set_cookie(
        "token", token_data["id_token"], httponly=True, secure=True, samesite="Lax"
    )
    return response

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns a simple status message.
    """
    return {"status": "ok"}

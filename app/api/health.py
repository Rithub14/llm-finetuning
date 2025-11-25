from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    """
    Basic health check endpoint.
    Returns current server time and status.
    Does not touch the model or DB.
    """
    return{
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z"
    }
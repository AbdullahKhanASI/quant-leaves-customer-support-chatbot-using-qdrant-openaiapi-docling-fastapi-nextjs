"""Health check endpoint."""
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Service health probe")
async def healthcheck() -> dict:
    return {"status": "ok"}

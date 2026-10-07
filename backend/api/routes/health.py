from datetime import UTC, datetime

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "polaris-api",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/ready")
async def ready() -> dict:
    return {
        "status": "ready",
        "service": "polaris-api",
    }

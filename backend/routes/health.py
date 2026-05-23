from fastapi import APIRouter
from services.database import stats

router = APIRouter(tags=["system"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "WebSense RAG"}


@router.get("/stats")
async def get_stats():
    return stats()

from fastapi import APIRouter
from services.database import list_incidents

router = APIRouter(tags=["history"])


@router.get("/history")
async def history(limit: int = 50):
    return list_incidents(limit)

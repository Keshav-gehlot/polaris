from datetime import UTC, datetime
from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel, Field
router = APIRouter(prefix="/cases", tags=["cases"])
class CaseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
@router.post("")
async def create_case(payload: CaseCreate) -> dict:
    return {"id":str(uuid4()),"title":payload.title,"description":payload.description,"created_at":datetime.now(UTC).isoformat(),"status":"open"}

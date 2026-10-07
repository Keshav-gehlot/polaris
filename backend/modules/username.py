from fastapi import APIRouter, Query
from backend.modules.common import retrieved_at
from backend.modules.models import SourceRecord
router = APIRouter(prefix="/username", tags=["username"])
@router.get("/lookup")
async def lookup(username: str = Query(min_length=1, max_length=64)) -> dict:
    record = SourceRecord(source="Username provider registry", retrieved_at=retrieved_at(), status="not_searched", note="No provider query was executed. Add individual public providers before enabling searches.")
    return {"module":"username","searched":False,"target":username,"records":[record.model_dump()]}

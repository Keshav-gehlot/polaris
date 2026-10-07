from fastapi import APIRouter
from backend.modules.models import SourceRecord
router = APIRouter(prefix="/catalogue", tags=["catalogue"])
@router.get("/schema")
async def schema() -> dict:
    return {"module":"catalogue","searched":False,"status":"ready","record":SourceRecord.model_json_schema()}

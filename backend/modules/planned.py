from fastapi import APIRouter
router = APIRouter(prefix="/planned", tags=["planned"])
@router.get("/{module_id}")
async def planned(module_id: str) -> dict:
    return {"module":module_id,"searched":False,"status":"planned","note":"This module is reserved in the Polaris architecture but has no live provider implementation yet."}

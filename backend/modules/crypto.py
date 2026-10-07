import re
from fastapi import APIRouter
from backend.modules.common import retrieved_at
from backend.modules.models import CryptoRequest, SourceRecord
router = APIRouter(prefix="/crypto", tags=["crypto"])
BTC = re.compile(r"^(bc1[a-z0-9]{11,87}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$")
EVM = re.compile(r"^0x[a-fA-F0-9]{40}$")
@router.post("/lookup")
async def lookup(request: CryptoRequest) -> dict:
    address = request.address.strip()
    if not (BTC.fullmatch(address) or EVM.fullmatch(address)):
        return {"module":"crypto","searched":False,"status":"invalid_target","note":"Only Bitcoin and EVM address formats are currently accepted."}
    record = SourceRecord(source="Provider registry", retrieved_at=retrieved_at(), status="not_searched", note="Configure a supported blockchain provider on the backend before querying external records.")
    return {"module":"crypto","searched":False,"target":address,"records":[record.model_dump()]}

import httpx
from fastapi import APIRouter
from backend.modules.common import retrieved_at
from backend.modules.models import SourceRecord

router = APIRouter(prefix="/watchtower", tags=["watchtower"])
USGS_FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
EONET_EVENTS = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open"

@router.get("/events")
async def events() -> dict:
    records = []
    async with httpx.AsyncClient(timeout=15, follow_redirects=False) as client:
        for name, url in (("USGS Earthquake Catalog", USGS_FEED), ("NASA EONET", EONET_EVENTS)):
            try:
                response = await client.get(url)
                response.raise_for_status()
                records.append(SourceRecord(source=name, retrieved_at=retrieved_at(), data=response.json()))
            except (httpx.HTTPError, ValueError) as exc:
                records.append(SourceRecord(source=name, retrieved_at=retrieved_at(), status="error", note=str(exc)))
    return {"module":"watchtower", "searched":True, "records":[r.model_dump() for r in records]}

@router.get("/health")
async def health() -> dict:
    return {"module":"watchtower", "status":"live"}

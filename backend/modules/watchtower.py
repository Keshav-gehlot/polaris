import httpx
from fastapi import APIRouter, Query

from backend.modules.common import retrieved_at
from backend.modules.models import SourceRecord

router = APIRouter(prefix="/watchtower", tags=["watchtower"])

USGS_FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
EONET_FEED = "https://eonet.gsfc.nasa.gov/api/v3/events/geojson?status=open"
TIMEOUT = httpx.Timeout(15.0, connect=5.0)


def _usgs_events(payload: dict, source: str, retrieved: str) -> list[dict]:
    events = []
    for feature in payload.get("features", []):
        props = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        coords = geometry.get("coordinates") or []
        point = {"longitude": coords[0], "latitude": coords[1]} if geometry.get("type") == "Point" and len(coords) >= 2 else None
        events.append({
            "id": feature.get("id"),
            "title": props.get("title") or "USGS earthquake",
            "description": None,
            "category": "earthquakes",
            "source": source,
            "source_url": props.get("url") or props.get("detail"),
            "retrieved_at": retrieved,
            "time": props.get("time"),
            "magnitude": props.get("mag"),
            "status": props.get("status"),
            "location": point,
            "raw": feature,
        })
    return events


def _eonet_events(payload: dict, source: str, retrieved: str) -> list[dict]:
    events = []
    for feature in payload.get("features", []):
        props = feature.get("properties") or {}
        geometry = feature.get("geometry") or {}
        coords = geometry.get("coordinates") or []
        point = {"longitude": coords[0], "latitude": coords[1]} if geometry.get("type") == "Point" and len(coords) >= 2 else None
        categories = props.get("categories") or []
        category = categories[0].get("title") if categories and isinstance(categories[0], dict) else None
        events.append({
            "id": feature.get("id") or props.get("id"),
            "title": props.get("title") or "NASA EONET event",
            "description": props.get("description"),
            "category": category,
            "source": source,
            "source_url": props.get("link"),
            "retrieved_at": retrieved,
            "time": props.get("date"),
            "magnitude": props.get("magnitudeValue"),
            "status": "open" if props.get("closed") is None else "closed",
            "location": point,
            "raw": feature,
        })
    return events


@router.get("/events")
async def events(
    source: str = Query(default="all", pattern="^(all|usgs|eonet)$"),
    limit: int = Query(default=100, ge=1, le=500),
) -> dict:
    records: list[SourceRecord] = []
    normalized_events: list[dict] = []

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        follow_redirects=False,
        headers={"User-Agent": "Polaris/0.1"},
    ) as client:
        if source in {"all", "usgs"}:
            retrieved = retrieved_at()
            try:
                response = await client.get(USGS_FEED)
                response.raise_for_status()
                payload = response.json()
                records.append(SourceRecord(
                    source="USGS Earthquake Catalog",
                    retrieved_at=retrieved,
                    data={"url": USGS_FEED, "count": len(payload.get("features", []))},
                ))
                normalized_events.extend(_usgs_events(payload, "USGS Earthquake Catalog", retrieved))
            except (httpx.HTTPError, ValueError) as exc:
                records.append(SourceRecord(
                    source="USGS Earthquake Catalog",
                    retrieved_at=retrieved_at(),
                    status="error",
                    note=str(exc),
                    data={"url": USGS_FEED},
                ))

        if source in {"all", "eonet"}:
            retrieved = retrieved_at()
            try:
                response = await client.get(EONET_FEED)
                response.raise_for_status()
                payload = response.json()
                records.append(SourceRecord(
                    source="NASA EONET",
                    retrieved_at=retrieved,
                    data={"url": EONET_FEED, "count": len(payload.get("features", []))},
                ))
                normalized_events.extend(_eonet_events(payload, "NASA EONET", retrieved))
            except (httpx.HTTPError, ValueError) as exc:
                records.append(SourceRecord(
                    source="NASA EONET",
                    retrieved_at=retrieved_at(),
                    status="error",
                    note=str(exc),
                    data={"url": EONET_FEED},
                ))

    normalized_events.sort(key=lambda item: str(item.get("time") or ""), reverse=True)
    return {
        "module": "watchtower",
        "searched": True,
        "sources": [record.model_dump() for record in records],
        "events": normalized_events[:limit],
        "count": min(len(normalized_events), limit),
    }


@router.get("/health")
async def health() -> dict:
    return {"module": "watchtower", "status": "live"}

from datetime import UTC, datetime
from urllib.parse import urlparse

def retrieved_at() -> str:
    return datetime.now(UTC).isoformat()

def normalize_domain(value: str) -> str:
    raw = value.strip().lower()
    if "://" in raw:
        parsed = urlparse(raw)
        if parsed.scheme != "https" or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
            raise ValueError("Only a bare domain or HTTPS origin is accepted")
        raw = parsed.hostname or ""
    raw = raw.rstrip(".")
    if not raw or "/" in raw or ":" in raw or "@" in raw or " " in raw or len(raw) > 253:
        raise ValueError("Invalid domain")
    return raw

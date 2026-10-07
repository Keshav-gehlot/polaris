import ipaddress
import socket
import httpx
from fastapi import APIRouter, HTTPException
from backend.modules.common import normalize_domain, retrieved_at
from backend.modules.models import DomainRequest, SourceRecord

router = APIRouter(prefix="/netscan", tags=["netscan"])
IANA_RDAP_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
CLOUDFLARE_DOH = "https://cloudflare-dns.com/dns-query"
CRT_SH = "https://crt.sh/"

def validate_public_hostname(domain: str) -> str:
    try:
        normalized = normalize_domain(domain)
        ip = ipaddress.ip_address(normalized)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise ValueError("Private or reserved IP targets are not accepted")
        return normalized
    except ValueError:
        if "." not in domain:
            raise ValueError("A fully qualified domain is required")
        try:
            addresses = socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
        except socket.gaierror as exc:
            raise ValueError("Domain does not resolve") from exc
        for item in addresses:
            ip = ipaddress.ip_address(item[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError("Domain resolves to a private or reserved address")
        return domain

async def rdap_lookup(client: httpx.AsyncClient, domain: str) -> SourceRecord:
    bootstrap = await client.get(IANA_RDAP_BOOTSTRAP)
    bootstrap.raise_for_status()
    endpoint = None
    for tlds, urls in bootstrap.json().get("services", []):
        if domain.rsplit(".", 1)[-1] in tlds and urls:
            endpoint = urls[0]
            break
    if not endpoint:
        return SourceRecord(source="IANA RDAP", retrieved_at=retrieved_at(), status="not_found", note="No RDAP service was advertised for this TLD.")
    endpoint = endpoint.rstrip("/") + "/domain/" + domain
    if httpx.URL(endpoint).scheme != "https":
        raise ValueError("RDAP endpoint must use HTTPS")
    response = await client.get(endpoint)
    if response.status_code == 404:
        return SourceRecord(source="RDAP", retrieved_at=retrieved_at(), status="not_found", note="No RDAP record returned.")
    response.raise_for_status()
    return SourceRecord(source="RDAP", retrieved_at=retrieved_at(), data=response.json())

@router.post("/domain")
async def domain_lookup(request: DomainRequest) -> dict:
    try:
        domain = validate_public_hostname(normalize_domain(request.domain))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    records = []
    async with httpx.AsyncClient(timeout=15, follow_redirects=False, headers={"User-Agent":"Polaris/0.1"}) as client:
        for source, call in [
            ("RDAP", lambda: rdap_lookup(client, domain)),
            ("Cloudflare DoH", lambda: client.get(CLOUDFLARE_DOH, params={"name":domain,"type":"A"}, headers={"accept":"application/dns-json"})),
            ("crt.sh", lambda: client.get(CRT_SH, params={"q":"%." + domain,"output":"json"})),
        ]:
            try:
                result = await call()
                if isinstance(result, SourceRecord):
                    records.append(result)
                else:
                    result.raise_for_status()
                    records.append(SourceRecord(source=source, retrieved_at=retrieved_at(), data=result.json()))
            except (httpx.HTTPError, ValueError) as exc:
                records.append(SourceRecord(source=source, retrieved_at=retrieved_at(), status="error", note=str(exc)))
    return {"module":"netscan", "searched":True, "target":domain, "records":[r.model_dump() for r in records]}

@router.post("/authorized-scan")
async def authorized_scan(request: DomainRequest, authorization_confirmed: bool = False) -> dict:
    if not authorization_confirmed:
        raise HTTPException(status_code=403, detail="Active scanning requires explicit authorization confirmation.")
    return {"module":"netscan", "searched":False, "status":"not_implemented", "note":"The isolated scanner worker is not enabled yet. No active traffic was generated.", "target":request.domain}

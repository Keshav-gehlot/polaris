from backend.modules.models import ModuleStatus

MODULES = [
    ModuleStatus(id="watchtower", name="Watchtower", status="live", description="Live geographic and disaster-event intelligence.", capabilities=["USGS earthquakes", "NASA EONET events"]),
    ModuleStatus(id="netscan", name="NetScan", status="partial", description="Passive network and domain intelligence with an authorization-gated active scanning boundary.", capabilities=["RDAP", "DNS-over-HTTPS", "certificate transparency", "authorized scanning boundary"]),
    ModuleStatus(id="crypto", name="Crypto", status="partial", description="Blockchain address intelligence through configured public data providers.", capabilities=["Bitcoin", "EVM", "provider-backed records"]),
    ModuleStatus(id="catalogue", name="Catalogue", status="partial", description="Evidence catalogue and source records.", capabilities=["source records", "retrieval timestamps", "case-ready evidence"]),
    ModuleStatus(id="username", name="Username Research", status="partial", description="Username investigation framework; providers are added individually.", capabilities=["provider registry", "not-searched semantics"]),
    ModuleStatus(id="camera", name="Camera", status="planned", description="Image and camera intelligence module."),
    ModuleStatus(id="hawk", name="Hawk", status="planned", description="Advanced investigative intelligence module."),
    ModuleStatus(id="skywave", name="Skywave", status="planned", description="Wireless and radio intelligence module."),
    ModuleStatus(id="fisherman", name="Fisherman", status="planned", description="Collection and ingestion module."),
    ModuleStatus(id="cases", name="Cases", status="live", description="Investigation case board foundation.", capabilities=["case metadata", "evidence references"]),
]

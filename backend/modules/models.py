from typing import Any
from pydantic import BaseModel, Field

class SourceRecord(BaseModel):
    source: str
    retrieved_at: str
    status: str = "ok"
    data: Any = None
    note: str | None = None

class ModuleStatus(BaseModel):
    id: str
    name: str
    status: str
    description: str
    capabilities: list[str] = Field(default_factory=list)

class DomainRequest(BaseModel):
    domain: str = Field(min_length=1, max_length=253)

class CryptoRequest(BaseModel):
    address: str = Field(min_length=1, max_length=128)

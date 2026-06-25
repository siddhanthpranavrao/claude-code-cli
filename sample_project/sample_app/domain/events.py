from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    tenant_id: str
    payload: dict[str, Any]
    created_at: datetime = datetime.utcnow()


def document_indexed(tenant_id: str, document_id: str, chunk_count: int) -> DomainEvent:
    return DomainEvent(
        event_type="document.indexed",
        tenant_id=tenant_id,
        payload={"document_id": document_id, "chunk_count": chunk_count},
    )


def indexing_failed(tenant_id: str, document_id: str, reason: str) -> DomainEvent:
    return DomainEvent(
        event_type="document.indexing_failed",
        tenant_id=tenant_id,
        payload={"document_id": document_id, "reason": reason},
    )


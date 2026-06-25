from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class DocumentStatus(str, Enum):
    PENDING = "pending"
    INDEXED = "indexed"
    FAILED = "failed"
    ARCHIVED = "archived"


@dataclass
class Tenant:
    id: str
    name: str
    allowed_collections: set[str] = field(default_factory=set)

    def can_access(self, collection: str) -> bool:
        return collection in self.allowed_collections


@dataclass
class Document:
    id: str
    tenant_id: str
    collection: str
    title: str
    body: str
    metadata: dict[str, Any] = field(default_factory=dict)
    status: DocumentStatus = DocumentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)

    def word_count(self) -> int:
        return len(self.body.split())

    def mark_indexed(self) -> None:
        self.status = DocumentStatus.INDEXED

    def mark_failed(self, reason: str) -> None:
        self.status = DocumentStatus.FAILED
        self.metadata["failure_reason"] = reason


@dataclass
class Chunk:
    id: str
    document_id: str
    tenant_id: str
    ordinal: int
    text: str
    token_count: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def preview(self, limit: int = 120) -> str:
        compact = " ".join(self.text.split())
        return compact[:limit]


@dataclass
class SearchHit:
    chunk_id: str
    document_id: str
    score: float
    source: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def explain(self) -> str:
        return f"{self.source} score={self.score:.4f} chunk={self.chunk_id}"


@dataclass
class Answer:
    text: str
    citations: list[str]
    warnings: list[str] = field(default_factory=list)

    def has_citation_drift(self) -> bool:
        return any("citation drift" in warning.lower() for warning in self.warnings)


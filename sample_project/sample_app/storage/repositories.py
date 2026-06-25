from sample_app.domain.events import DomainEvent
from sample_app.domain.models import Chunk, Document
from sample_app.storage.database import InMemoryDatabase


class DocumentRepository:
    def __init__(self, db: InMemoryDatabase):
        self.db = db

    def save_document(self, document: Document) -> None:
        self.db.put("documents", document.id, document)

    def save_chunk(self, chunk: Chunk) -> None:
        self.db.put("chunks", chunk.id, chunk)

    def save_dead_letter(self, event: DomainEvent) -> None:
        self.db.put("events", f"dead-letter:{event.payload.get('document_id')}", event)


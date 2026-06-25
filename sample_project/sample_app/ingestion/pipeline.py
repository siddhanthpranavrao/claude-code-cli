from pathlib import Path

from sample_app.config.settings import Settings
from sample_app.domain.events import document_indexed, indexing_failed
from sample_app.domain.models import Chunk, Document
from sample_app.ingestion.chunker import TextChunker
from sample_app.ingestion.file_loader import FileLoader
from sample_app.ingestion.metadata import MetadataEnricher
from sample_app.ingestion.parser import MarkdownParser
from sample_app.observability.logger import get_logger
from sample_app.storage.repositories import DocumentRepository

logger = get_logger(__name__)


class IngestionPipeline:
    """Large orchestration class with nested calls for retrieval testing.

    Search keywords intentionally present here:
    ingest directory, chunk overlap, metadata enrichment, dead letter queue,
    indexing failed, stale vector index, tenant isolation.
    """

    def __init__(
        self,
        settings: Settings,
        loader: FileLoader,
        parser: MarkdownParser,
        enricher: MetadataEnricher,
        repository: DocumentRepository,
    ):
        self.settings = settings
        self.loader = loader
        self.parser = parser
        self.enricher = enricher
        self.repository = repository
        self.chunker = TextChunker(settings.chunk_size, settings.chunk_overlap)

    def ingest_directory(self, root: Path, tenant_id: str, collection: str) -> list[Chunk]:
        chunks: list[Chunk] = []
        for path in self.loader.discover_files(root):
            try:
                chunks.extend(self.ingest_file(path, tenant_id, collection))
            except Exception as exc:
                event = indexing_failed(tenant_id, path.stem, str(exc))
                logger.error("indexing failed", extra={"event": event.payload})
                self.repository.save_dead_letter(event)
        return chunks

    def ingest_file(self, path: Path, tenant_id: str, collection: str) -> list[Chunk]:
        document = self._load_and_parse(path, tenant_id, collection)
        document = self._enrich_document(document)
        chunks = self._chunk_document(document)
        self._persist_indexable_units(document, chunks)
        self._publish_success_event(document, chunks)
        return chunks

    def _load_and_parse(self, path: Path, tenant_id: str, collection: str) -> Document:
        document = self.loader.load_text_file(path, tenant_id, collection)
        normalized = self.parser.normalize(document.body)
        document.body = normalized
        return document

    def _enrich_document(self, document: Document) -> Document:
        headings = self.parser.extract_headings(document.body)
        return self.enricher.enrich(document, headings)

    def _chunk_document(self, document: Document) -> list[Chunk]:
        chunks = self.chunker.chunk(document)
        if not chunks:
            document.mark_failed("no chunks produced during chunk overlap processing")
            raise ValueError("empty document cannot be indexed")
        return chunks

    def _persist_indexable_units(self, document: Document, chunks: list[Chunk]) -> None:
        document.mark_indexed()
        self.repository.save_document(document)
        for chunk in chunks:
            self.repository.save_chunk(chunk)

    def _publish_success_event(self, document: Document, chunks: list[Chunk]) -> None:
        event = document_indexed(document.tenant_id, document.id, len(chunks))
        logger.info("document indexed", extra={"event": event.payload})


def build_ingestion_pipeline(settings: Settings, repository: DocumentRepository) -> IngestionPipeline:
    return IngestionPipeline(
        settings=settings,
        loader=FileLoader(),
        parser=MarkdownParser(),
        enricher=MetadataEnricher(),
        repository=repository,
    )


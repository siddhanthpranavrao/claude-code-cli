from pathlib import Path

from sample_app.config.settings import Settings
from sample_app.ingestion.pipeline import build_ingestion_pipeline
from sample_app.storage.database import InMemoryDatabase
from sample_app.storage.repositories import DocumentRepository


def test_pipeline_indexes_text_file(tmp_path: Path):
    path = tmp_path / "note.txt"
    path.write_text("# Title\nhello semantic search and lexical search", encoding="utf-8")
    settings = Settings(tenant_id="tenant", data_dir=tmp_path, chunk_size=10, chunk_overlap=2)
    pipeline = build_ingestion_pipeline(settings, DocumentRepository(InMemoryDatabase()))
    chunks = pipeline.ingest_file(path, "tenant", "docs")
    assert chunks


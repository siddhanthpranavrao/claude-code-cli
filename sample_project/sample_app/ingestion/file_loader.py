from pathlib import Path

from sample_app.domain.models import Document


class FileLoader:
    def load_text_file(self, path: Path, tenant_id: str, collection: str) -> Document:
        text = path.read_text(encoding="utf-8")
        return Document(
            id=path.stem,
            tenant_id=tenant_id,
            collection=collection,
            title=path.name,
            body=text,
            metadata={"source_path": str(path), "loader": "FileLoader"},
        )

    def discover_files(self, root: Path) -> list[Path]:
        return sorted(path for path in root.rglob("*.txt") if path.is_file())


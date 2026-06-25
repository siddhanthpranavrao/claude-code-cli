from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    tenant_id: str
    data_dir: Path
    chunk_size: int = 900
    chunk_overlap: int = 120
    embedding_dimensions: int = 1536
    bm25_k1: float = 1.5
    bm25_b: float = 0.75
    max_context_tokens: int = 6000

    def validate(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk overlap must be smaller than chunk size")
        if self.embedding_dimensions not in (384, 768, 1024, 1536, 3072):
            raise ValueError("unsupported embedding dimension for vector index")


def load_settings(root: Path | None = None) -> Settings:
    base = root or Path.cwd()
    settings = Settings(tenant_id="demo-tenant", data_dir=base / "data")
    settings.validate()
    return settings


from sample_app.domain.errors import EmbeddingDimensionMismatch, StaleVectorIndexError
from sample_app.domain.models import Chunk, SearchHit
from sample_app.utils.text import cosine_similarity


class InMemoryVectorStore:
    def __init__(self, dimensions: int):
        self.dimensions = dimensions
        self._vectors: dict[str, list[float]] = {}
        self._chunks: dict[str, Chunk] = {}
        self._version = 0

    def upsert(self, chunk: Chunk, embedding: list[float]) -> None:
        if len(embedding) != self.dimensions:
            raise EmbeddingDimensionMismatch(
                f"EmbeddingDimensionMismatch expected {self.dimensions} got {len(embedding)}"
            )
        self._vectors[chunk.id] = embedding
        self._chunks[chunk.id] = chunk
        self._version += 1

    def search(self, query_embedding: list[float], limit: int = 10, expected_version: int | None = None) -> list[SearchHit]:
        if expected_version is not None and expected_version != self._version:
            raise StaleVectorIndexError("stale_vector_index detected during semantic search")
        if len(query_embedding) != self.dimensions:
            raise EmbeddingDimensionMismatch("query embedding dimension mismatch")
        hits = []
        for chunk_id, vector in self._vectors.items():
            chunk = self._chunks[chunk_id]
            hits.append(
                SearchHit(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    score=cosine_similarity(query_embedding, vector),
                    source="vector",
                    text=chunk.text,
                )
            )
        return sorted(hits, key=lambda hit: hit.score, reverse=True)[:limit]


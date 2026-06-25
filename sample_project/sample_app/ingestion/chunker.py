from sample_app.domain.models import Chunk, Document


class TextChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk overlap must be smaller than chunk size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: Document) -> list[Chunk]:
        words = document.body.split()
        chunks: list[Chunk] = []
        start = 0
        ordinal = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            text = " ".join(words[start:end])
            chunks.append(
                Chunk(
                    id=f"{document.id}:{ordinal}",
                    document_id=document.id,
                    tenant_id=document.tenant_id,
                    ordinal=ordinal,
                    text=text,
                    token_count=len(text.split()),
                    metadata={"chunk overlap": self.chunk_overlap},
                )
            )
            ordinal += 1
            if end == len(words):
                break
            start = end - self.chunk_overlap
        return chunks


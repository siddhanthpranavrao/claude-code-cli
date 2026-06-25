import math
from collections import Counter, defaultdict

from sample_app.domain.models import Chunk, SearchHit
from sample_app.search.tokenizer import tokenize


class BM25Index:
    """Lexical index for keyword search and exact error search.

    This file is intentionally bigger than a tiny example. It includes
    index building, document frequency tracking, query scoring, explanation,
    and keyword-heavy phrases like RateLimitExceeded, EmbeddingDimensionMismatch,
    stale_vector_index, hybrid score fusion, and tenant isolation.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self._documents: dict[str, Chunk] = {}
        self._term_frequencies: dict[str, Counter[str]] = {}
        self._document_frequencies: dict[str, int] = defaultdict(int)
        self._average_length = 0.0

    def build(self, chunks: list[Chunk]) -> None:
        self._documents.clear()
        self._term_frequencies.clear()
        self._document_frequencies.clear()

        total_length = 0
        for chunk in chunks:
            tokens = tokenize(chunk.text)
            term_frequency = Counter(tokens)
            self._documents[chunk.id] = chunk
            self._term_frequencies[chunk.id] = term_frequency
            total_length += len(tokens)
            for term in term_frequency:
                self._document_frequencies[term] += 1

        self._average_length = total_length / max(len(chunks), 1)

    def search(self, query: str, limit: int = 10) -> list[SearchHit]:
        query_terms = tokenize(query)
        scored: list[SearchHit] = []
        for chunk_id, chunk in self._documents.items():
            score = self._score_document(query_terms, chunk_id)
            if score <= 0:
                continue
            scored.append(
                SearchHit(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    score=score,
                    source="bm25",
                    text=chunk.text,
                    metadata={"matched_terms": query_terms},
                )
            )
        return sorted(scored, key=lambda hit: hit.score, reverse=True)[:limit]

    def explain(self, query: str, chunk_id: str) -> dict[str, float]:
        terms = tokenize(query)
        return {term: self._score_term(term, chunk_id) for term in terms}

    def _score_document(self, query_terms: list[str], chunk_id: str) -> float:
        return sum(self._score_term(term, chunk_id) for term in query_terms)

    def _score_term(self, term: str, chunk_id: str) -> float:
        term_frequency = self._term_frequencies.get(chunk_id, Counter())
        frequency = term_frequency.get(term, 0)
        if frequency == 0:
            return 0.0

        document_count = max(len(self._documents), 1)
        doc_frequency = self._document_frequencies.get(term, 0)
        idf = math.log(1 + (document_count - doc_frequency + 0.5) / (doc_frequency + 0.5))

        doc_length = sum(term_frequency.values())
        normalizer = frequency + self.k1 * (
            1 - self.b + self.b * doc_length / max(self._average_length, 1)
        )
        return idf * (frequency * (self.k1 + 1)) / normalizer


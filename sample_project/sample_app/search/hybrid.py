from collections import defaultdict

from sample_app.domain.models import SearchHit
from sample_app.search.bm25 import BM25Index
from sample_app.search.query_expansion import QueryExpander
from sample_app.search.reranker import SemanticReranker
from sample_app.search.vector_store import InMemoryVectorStore


class HybridSearchEngine:
    """Coordinates lexical search, vector search, fusion, and reranking.

    Keywords for retrieval tests:
    hybrid score fusion, semantic reranking, query rewrite, BM25 search,
    vector recall, lexical precision, duplicate collapse.
    """

    def __init__(
        self,
        bm25: BM25Index,
        vectors: InMemoryVectorStore,
        expander: QueryExpander,
        reranker: SemanticReranker,
    ):
        self.bm25 = bm25
        self.vectors = vectors
        self.expander = expander
        self.reranker = reranker

    def search(self, query: str, embedding: list[float], limit: int = 8) -> list[SearchHit]:
        rewritten_queries = self.expander.expand(query)
        lexical_hits = self._run_lexical_queries(rewritten_queries, limit=limit * 2)
        vector_hits = self.vectors.search(embedding, limit=limit * 2)
        fused = self._reciprocal_rank_fusion(lexical_hits, vector_hits)
        return self.reranker.rerank(query, fused, limit=limit)

    def _run_lexical_queries(self, queries: list[str], limit: int) -> list[SearchHit]:
        hits: list[SearchHit] = []
        for query in queries:
            hits.extend(self.bm25.search(query, limit=limit))
        return self._deduplicate(hits)

    def _reciprocal_rank_fusion(self, lexical: list[SearchHit], vector: list[SearchHit]) -> list[SearchHit]:
        scores: dict[str, float] = defaultdict(float)
        examples: dict[str, SearchHit] = {}
        for source_hits in (lexical, vector):
            for rank, hit in enumerate(source_hits, start=1):
                scores[hit.chunk_id] += 1 / (60 + rank)
                examples[hit.chunk_id] = hit

        fused = []
        for chunk_id, score in scores.items():
            hit = examples[chunk_id]
            fused.append(
                SearchHit(
                    chunk_id=hit.chunk_id,
                    document_id=hit.document_id,
                    score=score,
                    source="hybrid score fusion",
                    text=hit.text,
                    metadata={**hit.metadata, "fusion_score": score},
                )
            )
        return sorted(fused, key=lambda item: item.score, reverse=True)

    def _deduplicate(self, hits: list[SearchHit]) -> list[SearchHit]:
        best: dict[str, SearchHit] = {}
        for hit in hits:
            current = best.get(hit.chunk_id)
            if current is None or hit.score > current.score:
                best[hit.chunk_id] = hit
        return list(best.values())


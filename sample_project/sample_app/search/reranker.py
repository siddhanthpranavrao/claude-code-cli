from sample_app.domain.models import SearchHit
from sample_app.search.tokenizer import unique_terms


class SemanticReranker:
    def rerank(self, query: str, hits: list[SearchHit], limit: int = 8) -> list[SearchHit]:
        query_terms = unique_terms(query)
        reranked = []
        for hit in hits:
            overlap = len(query_terms & unique_terms(hit.text))
            boosted = SearchHit(
                chunk_id=hit.chunk_id,
                document_id=hit.document_id,
                score=hit.score + overlap * 0.05,
                source=f"{hit.source}+semantic_reranking",
                text=hit.text,
                metadata={**hit.metadata, "semantic_overlap": overlap},
            )
            reranked.append(boosted)
        return sorted(reranked, key=lambda item: item.score, reverse=True)[:limit]


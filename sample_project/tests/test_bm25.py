from sample_app.domain.models import Chunk
from sample_app.search.bm25 import BM25Index


def test_bm25_finds_error_keyword():
    chunk = Chunk("c1", "d1", "t1", 0, "EmbeddingDimensionMismatch in vector index", 4)
    index = BM25Index()
    index.build([chunk])
    hits = index.search("EmbeddingDimensionMismatch")
    assert hits[0].chunk_id == "c1"


from sample_app.domain.errors import CitationDriftError
from sample_app.domain.models import Answer, SearchHit


class CitationValidator:
    def validate(self, answer: Answer, hits: list[SearchHit]) -> None:
        available = {hit.chunk_id for hit in hits}
        missing = [citation for citation in answer.citations if citation not in available]
        if missing:
            raise CitationDriftError(f"citation drift detected for citations: {missing}")


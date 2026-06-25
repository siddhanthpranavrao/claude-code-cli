from sample_app.domain.models import Document


class MetadataEnricher:
    def enrich(self, document: Document, headings: list[str]) -> Document:
        document.metadata["headings"] = headings
        document.metadata["word_count"] = document.word_count()
        document.metadata["contains_error_terms"] = self._contains_error_terms(document.body)
        return document

    def _contains_error_terms(self, text: str) -> bool:
        terms = ["traceback", "exception", "timeout", "rate limit", "dimension mismatch"]
        lowered = text.lower()
        return any(term in lowered for term in terms)


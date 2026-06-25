class RagError(Exception):
    """Base application error."""


class DocumentNotFoundError(RagError):
    pass


class TenantIsolationViolation(RagError):
    pass


class EmbeddingDimensionMismatch(RagError):
    pass


class StaleVectorIndexError(RagError):
    pass


class CitationDriftError(RagError):
    pass


class RateLimitExceeded(RagError):
    pass


from dataclasses import dataclass


@dataclass
class FeatureFlags:
    enable_query_rewrite: bool = True
    enable_semantic_reranking: bool = True
    enable_pii_redaction: bool = True
    enable_dead_letter_queue: bool = True
    enable_citation_validation: bool = True

    def is_enabled(self, flag_name: str) -> bool:
        return bool(getattr(self, flag_name, False))


DEFAULT_FLAGS = FeatureFlags()


SYNONYMS = {
    "auth": ["authentication", "authorization", "login"],
    "timeout": ["deadline exceeded", "slow request", "latency"],
    "embedding": ["vector", "semantic representation", "dense retrieval"],
    "citation": ["source reference", "grounding", "attribution"],
}


class QueryExpander:
    def expand(self, query: str) -> list[str]:
        lowered = query.lower()
        variants = [query]
        for key, replacements in SYNONYMS.items():
            if key in lowered:
                variants.extend(f"{query} {replacement}" for replacement in replacements)
        return variants


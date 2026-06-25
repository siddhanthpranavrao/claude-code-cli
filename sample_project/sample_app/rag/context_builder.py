from sample_app.domain.models import SearchHit


class ContextBuilder:
    def build(self, hits: list[SearchHit], max_chars: int = 12_000) -> str:
        blocks = []
        used = 0
        for hit in hits:
            block = f"[{hit.chunk_id}] {hit.text}"
            if used + len(block) > max_chars:
                break
            blocks.append(block)
            used += len(block)
        return "\n\n".join(blocks)


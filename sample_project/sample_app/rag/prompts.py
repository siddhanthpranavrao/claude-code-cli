SYSTEM_PROMPT = """You are a grounded assistant. Use citations and say when context is missing."""


def build_user_prompt(question: str, context: str) -> str:
    return f"Question:\n{question}\n\nContext:\n{context}\n\nAnswer with citations."


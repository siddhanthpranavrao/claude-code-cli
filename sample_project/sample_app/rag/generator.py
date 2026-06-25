from sample_app.domain.models import Answer, SearchHit
from sample_app.rag.citations import CitationValidator
from sample_app.rag.context_builder import ContextBuilder
from sample_app.rag.prompts import SYSTEM_PROMPT, build_user_prompt


class FakeLLMClient:
    def complete(self, system: str, user: str) -> str:
        return f"{system}\n\nSynthetic answer based on prompt length={len(user)} [demo:0]"


class AnswerGenerator:
    """Answer generation with citation validation and fallback warnings."""

    def __init__(self, client: FakeLLMClient, context_builder: ContextBuilder, validator: CitationValidator):
        self.client = client
        self.context_builder = context_builder
        self.validator = validator

    def answer(self, question: str, hits: list[SearchHit]) -> Answer:
        context = self.context_builder.build(hits)
        prompt = build_user_prompt(question, context)
        raw = self.client.complete(SYSTEM_PROMPT, prompt)
        citations = [hits[0].chunk_id] if hits else []
        answer = Answer(text=raw, citations=citations)
        self._validate_or_warn(answer, hits)
        return answer

    def _validate_or_warn(self, answer: Answer, hits: list[SearchHit]) -> None:
        try:
            self.validator.validate(answer, hits)
        except Exception as exc:
            answer.warnings.append(f"citation drift warning: {exc}")


def build_answer_generator() -> AnswerGenerator:
    return AnswerGenerator(FakeLLMClient(), ContextBuilder(), CitationValidator())


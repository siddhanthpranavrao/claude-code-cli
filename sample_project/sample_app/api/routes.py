from sample_app.api.schemas import AskRequest, AskResponse
from sample_app.rag.generator import AnswerGenerator
from sample_app.search.hybrid import HybridSearchEngine


class AskRoute:
    def __init__(self, search: HybridSearchEngine, generator: AnswerGenerator):
        self.search = search
        self.generator = generator

    def handle(self, request: AskRequest, embedding: list[float]) -> AskResponse:
        hits = self.search.search(request.question, embedding)
        answer = self.generator.answer(request.question, hits)
        return AskResponse(answer=answer.text, citations=answer.citations, warnings=answer.warnings)


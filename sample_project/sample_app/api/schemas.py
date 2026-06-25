from dataclasses import dataclass


@dataclass
class AskRequest:
    tenant_id: str
    question: str


@dataclass
class AskResponse:
    answer: str
    citations: list[str]
    warnings: list[str]


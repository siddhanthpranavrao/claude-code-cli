from dataclasses import dataclass


@dataclass
class Job:
    id: str
    kind: str
    payload: dict[str, object]
    attempts: int = 0

    def mark_attempted(self) -> None:
        self.attempts += 1


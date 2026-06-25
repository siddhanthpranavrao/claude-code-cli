from collections import Counter


class Metrics:
    def __init__(self):
        self.counters: Counter[str] = Counter()

    def increment(self, name: str, value: int = 1) -> None:
        self.counters[name] += value

    def snapshot(self) -> dict[str, int]:
        return dict(self.counters)


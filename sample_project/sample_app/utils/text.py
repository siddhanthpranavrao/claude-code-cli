import math


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def redact_pii(text: str) -> str:
    words = []
    for word in text.split():
        if "@" in word:
            words.append("[REDACTED_EMAIL]")
        else:
            words.append(word)
    return " ".join(words)


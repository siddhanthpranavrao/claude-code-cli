from time import monotonic


class TTLCache:
    def __init__(self):
        self._items: dict[str, tuple[float, object]] = {}

    def set(self, key: str, value: object, ttl_seconds: float) -> None:
        self._items[key] = (monotonic() + ttl_seconds, value)

    def get(self, key: str) -> object | None:
        expires_at, value = self._items.get(key, (0, None))
        if expires_at < monotonic():
            self._items.pop(key, None)
            return None
        return value


class InMemoryDatabase:
    def __init__(self):
        self.tables: dict[str, dict[str, object]] = {
            "documents": {},
            "chunks": {},
            "events": {},
        }

    def put(self, table: str, key: str, value: object) -> None:
        self.tables.setdefault(table, {})[key] = value

    def get(self, table: str, key: str) -> object | None:
        return self.tables.get(table, {}).get(key)


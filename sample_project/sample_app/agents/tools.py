from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[[str], str]


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools[name]


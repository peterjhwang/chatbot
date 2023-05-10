from typing import Callable, Protocol


class AgentTool(Protocol):
    def __init__(self, history) -> None:
        super().__init__()

    def run(self, query: str) -> str:
        ...

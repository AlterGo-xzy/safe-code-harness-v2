from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def next_action(self, context: str) -> str:
        """Return one raw action protocol response for the supplied context."""

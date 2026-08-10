from safe_code_harness.llm.base import LLMClient


class MockLLM(LLMClient):
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses.copy()
        self._index = 0

    def next_action(self, context: str) -> str:
        if self._index >= len(self._responses):
            raise RuntimeError("mock responses exhausted")
        response = self._responses[self._index]
        self._index += 1
        return response

from .agent_client import AgentClient

class GeminiAdapter(AgentClient):
    def __init__(self, name: str, api_key: str, model: str):
        super().__init__(name, config={"model": model})
        self.api_key = api_key

    def call(self, prompt: str) -> str:
        raise NotImplementedError("Gemini-Adapter noch nicht implementiert")

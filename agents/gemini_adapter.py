# agents/gemini_adapter.py
import requests
from .agent_client import AgentClient

class GeminiAdapter(AgentClient):
    """
    Adapter für die Gemini-API. Sendet Prompts und erhält Antworten.
    """
    def __init__(self, name: str, api_key: str, model: str, temperature: float = 0.7):
        super().__init__(name, config={"model": model, "temperature": temperature})
        self.api_key = api_key

    def call(self, prompt: str) -> str:
        url = "https://gemini.googleapis.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.config["model"],
            "messages": [{"role": "system", "content": prompt}],
            "temperature": self.config.get("temperature", 0.7)
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Annahme: Datenstruktur analog zu OpenAI
        return data["choices"][0]["message"]["content"]

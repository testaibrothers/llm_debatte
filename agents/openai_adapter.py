# agents/openai_adapter.py
import requests
from .agent_client import AgentClient

class OpenAIAdapter(AgentClient):
    """
    Adapter für die OpenAI-API. Sendet Prompts und erhält Antworten.
    """
    def __init__(self, name: str, api_key: str, model: str, temperature: float = 0.7):
        super().__init__(name, config={"model": model, "temperature": temperature})
        self.api_key = api_key

    def call(self, prompt: str) -> str:
        """
        Sendet das Prompt an OpenAI und gibt den Text der Antwort zurück.
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.config["model"],
            "messages": [{"role": "system", "content": prompt}],
            "temperature": self.config["temperature"],
            "max_tokens": 500
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

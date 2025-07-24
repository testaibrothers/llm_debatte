# agents/gemini_adapter.py
import requests
from .agent_client import AgentClient

class GeminiAdapter(AgentClient):
    """
    Adapter für die Gemini-API über Google Generative Language.
    """
    def __init__(self, name: str, api_key: str, model: str, temperature: float = 0.7):
        super().__init__(name, config={"model": model, "temperature": temperature})
        self.api_key = api_key

    def call(self, prompt: str) -> str:
        """
        Sendet den Prompt an die Google Generative Language API für Gemini.
        Nutzt API-Key im Authorization-Header.
        """
        url = f"https://generativelanguage.googleapis.com/v1beta2/models/{self.config['model']}:generateMessage"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "prompt": {"text": prompt},
            "temperature": self.config.get("temperature", 0.7),
            "candidateCount": 1
        }
        try:
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("candidates", [{}])[0].get("output", "")
        except requests.HTTPError as e:
            return f"[Gemini API Error: {e.response.status_code}] {e.response.text}"

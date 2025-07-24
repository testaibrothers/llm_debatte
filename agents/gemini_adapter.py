# agents/gemini_adapter.py
import requests
from .agent_client import AgentClient

class GeminiAdapter(AgentClient):
    """
    Adapter für die Gemini-API.
    Aktuell nicht implementiert, gibt Platzhalter-Antwort zurück.
    """
    def __init__(self, name: str, api_key: str, model: str, temperature: float = 0.7):
        super().__init__(name, config={"model": model, "temperature": temperature})
        self.api_key = api_key

    def call(self, prompt: str) -> str:
                # Realer API-Aufruf an Gemini (Google Generative AI)
        url = f"https://generativelanguage.googleapis.com/v1beta2/models/{self.config['model']}:generateMessage"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "prompt": {"text": prompt},
            "temperature": self.config.get("temperature", 0.7),
            "candidateCount": 1
        }
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Annahme: Antwort-Text im Feld "candidates"[0]["output"]
        return data.get("candidates", [{}])[0].get("output", "")

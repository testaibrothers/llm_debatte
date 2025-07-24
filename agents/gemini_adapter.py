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
        """
        Sendet den Prompt an die Google Generative Language API für Gemini.
        Nutzt API-Key als Query-Parameter.
        """
        # Formular: URL mit API-Key als Parameter
        base_url = "https://generativelanguage.googleapis.com/v1beta2/models/{model}:generateMessage"
        url = base_url.format(model=self.config['model']) + f"?key={self.api_key}"
        payload = {
            "prompt": {"text": prompt},
            "temperature": self.config.get("temperature", 0.7),
            "candidateCount": 1
        }
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Antwort-Text im Feld "candidates"[0]["output"]
            return data.get("candidates", [{}])[0].get("output", "")
        except requests.HTTPError as e:
            return f"[Gemini API Error: {e.response.status_code}] {e.response.text}"

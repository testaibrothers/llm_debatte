# agents/gemini_adapter.py
from .agent_client import AgentClient

class GeminiAdapter(AgentClient):
    def __init__(self, name, api_key, model, temperature=0.7):
        super().__init__(name, config={"model": model, "temperature": temperature})
        self.api_key = api_key

    def call(self, prompt):
        # Platzhalter: Implementierung für Gemini-API
        # Beispiel:
        # url = "https://gemini.googleapis.com/v1/models/{self.config['model']}/:generateMessage"
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        # payload = {"prompt": prompt, ...}
        # resp = requests.post(url, headers=headers, json=payload)
        # return resp.json()["message"]["content"]
        raise NotImplementedError("Gemini-Adapter muss noch implementiert werden")

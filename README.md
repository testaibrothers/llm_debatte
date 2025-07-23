# KI-Debattenplattform (modular)

Dieses Projekt ist eine modularisierte Version der KI-Debattenplattform mit:
- **consensus/**: Konsens-Orchestrierung
- **agents/**: Adapter für verschiedene LLMs
- **utils/**: Hilfsfunktionen für JSON, Similarity
- **app/**: Streamlit UI

## Deployment
1. Python-Umgebung anlegen:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Streamlit starten:
   ```bash
   streamlit run app/main.py
   ```

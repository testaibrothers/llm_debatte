import os, sys
# eine Ebene über 'app/' zum Modul-Suchpfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus import ConsensusOrchestrator
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter

def main():
    st.set_page_config(page_title="KI-Debattenplattform", layout="centered")
    st.title("🤖 KI-Debattenplattform – Modular")

    # Hilfetexte (einmal definiert)
    agent_provider_help = (
        "Wähle den KI-Anbieter für deinen Agenten aus. "
        "OpenAI ist weit verbreitet, Gemini ist Googles Modell. "
        "(Standard: OpenAI)"
    )
    agent_model_help = (
        "Wähle das Modell für die KI. GPT-4 liefert in der Regel genauere, "
        "komplexere Antworten als gpt-3.5-turbo, ist jedoch teurer und langsamer. "
        "(Standard: gpt-3.5-turbo)"
    )
    prompt_help = (
        "Definiere hier den System-Prompt, der das Verhalten der KI steuert. "
        "Beispiel: ‘Du bist ein Finanzberater auf Topniveau…’. "
        "(Standard-Prompt vordefiniert)"
    )

    # ── Sidebar: LLM-Einstellungen ─────────────────────────
    with st.sidebar.expander("LLM-Einstellungen", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            provider_a = st.selectbox(
                "Agent A Anbieter", ["OpenAI", "Gemini"], index=0,
                help=agent_provider_help
            )
            model_a = st.selectbox(
                "Agent A Modell",
                ["gpt-3.5-turbo", "gpt-4"] if provider_a == "OpenAI" else ["gemini-proto"],
                index=0,
                help=agent_model_help
            )
            prompt_a = st.text_area(
                "Prompt Agent A",
                "Du bist ein Finanzberater auf Topniveau…",
                height=100,
                help=prompt_help
            )
        with col2:
            # Für Gemini API-Key hinzufügen
            provider_b = st.selectbox(
                "Agent B Anbieter", ["OpenAI", "Gemini"], index=0,
                help=agent_provider_help
            )
            model_b = st.selectbox(
                "Agent B Modell",
                ["gpt-3.5-turbo", "gpt-4"] if provider_b == "OpenAI" else ["gemini-proto"],
                index=0,
                help=agent_model_help
            )
            prompt_b = st.text_area(
                "Prompt Agent B",
                "Du bist ein Risikomanager auf Expert:innen-Level…",
                height=100,
                help=prompt_help
            )

    # ── Sidebar: Konsens-Einstellungen ──────────────────────
    with st.sidebar.expander("Konsens-Einstellungen", expanded=False):
        cfg = ConsensusConfig()  # Standard-Defaults laden
        divergence_rounds = st.number_input(
            "Divergenz-Runden", 1, 20, value=cfg.divergence_rounds,
            help=(
                "Anzahl der Runden (Standard: 3), in denen die KIs abwechselnd "
                "neue Perspektiven liefern. Mehr Runden = mehr Vielfalt."
            )
        )
        divergence_threshold = st.slider(
            "Divergenz-Threshold", 0.0, 1.0, value=cfg.divergence_threshold,
            help=(
                "Steuert, wie unterschiedlich eine neue Antwort sein muss (Standard: 0.5). "
                "Geringere Werte = stärker neue Ideen."
            )
        )
        convergence_threshold = st.slider(
            "Konvergenz-Threshold", 0.0, 1.0, value=cfg.convergence_threshold,
            help=(
                "Ab welchem Ähnlichkeitswert die Diskussion als Konsens gilt (Standard: 0.8). "
                "Höhere Werte = strengere Einigung."
            )
        )
        max_total = st.number_input(
            "Max. Gesamt-Beiträge", 1, 50, value=cfg.max_rounds_total,
            help=(
                "Gesamtzahl der Nachrichten (Standard: 10), danach stoppt die Debatte automatisch."
            )
        )
        manual_pause = st.checkbox(
            "Manueller Stopp möglich", value=cfg.manual_pause,
            help=(
                "Ermöglicht dir, die Debatte jederzeit per Button zu beenden."
            )
        )
        stop_on_manual = True

    # ── Werte ins Config-Objekt schreiben ──────────────────
    cfg.divergence_rounds = divergence_rounds
    cfg.divergence_threshold = divergence_threshold
    cfg.convergence_threshold = convergence_threshold
    cfg.max_rounds_total = max_total
    cfg.max_rounds = max_total               # legacy
    cfg.similarity_threshold = convergence_threshold  # legacy
    cfg.manual_pause = manual_pause
    cfg.stop_on_manual = stop_on_manual

    # ── Agenten instanziieren ──────────────────────────────
    openai_key = st.secrets.get("openai_api_key", "")
    gemini_key = st.secrets.get("gemini_api_key", "")
    def make_agent(name, provider, model, prompt):
        if provider == "OpenAI":
            return OpenAIAdapter(name, openai_key, model=model, temperature=0.7)
        # Für Gemini musst du in den App-Secrets 'gemini_api_key' setzen
        return GeminiAdapter(name, gemini_key, model=model)

    agent_a = make_agent("Agent A", provider_a, model_a, prompt_a)
    agent_b = make_agent("Agent B", provider_b, model_b, prompt_b)

    orchestrator = ConsensusOrchestrator(cfg)

    # ── Hauptbereich: Thema eingeben & Diskussion starten ────
    topic = st.text_area("Thema / Idee", height=120)
    if st.button("Diskussion starten") and topic:
        history = orchestrator.run(agent_a, agent_b, initial_prompt=topic)
        # Finale Empfehlung anzeigen
        final_agent, final_text = history[-1]
        st.markdown("### Finale Empfehlung")
        st.markdown(f"**{final_agent}:** {final_text}")

if __name__ == "__main__":
    main()

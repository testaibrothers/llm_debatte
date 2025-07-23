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

    # Hilfetexte (einmal definiert und wiederverwendet)
    agent_provider_help = (
        "Wähle den KI-Anbieter aus, den Agent A und B nutzen sollen. "
        "OpenAI ist sehr etabliert und weit verbreitet; Gemini ist Googles Modell. "
        "Je nach Anbieter können sich Antworten und Geschwindigkeit unterscheiden."
    )
    agent_model_help = (
        "Wähle das Modell für die KI. "
        "GPT-4 liefert in der Regel genauere und komplexere Antworten als gpt-3.5-turbo, "
        "ist aber auch teurer und etwas langsamer."
    )
    prompt_help = (
        "Gib hier den System-Prompt ein, der der KI erklärt, wie sie sich verhalten soll. "
        "Beispiel: ‚Du bist ein Finanzberater auf Topniveau…‘. "
        "Der Prompt steuert, welcher Stil und welche Expertise die Antwort hat."
    )

    # ── Sidebar: Agenten-Konfiguration ──────────────────────
    col1, col2 = st.sidebar.columns(2)
    with col1:
        provider_a = st.selectbox(
            "Agent A Anbieter", ["OpenAI", "Gemini"],
            help=agent_provider_help
        )
        model_a = st.selectbox(
            "Agent A Modell",
            ["gpt-3.5-turbo", "gpt-4"] if provider_a == "OpenAI" else ["gemini-proto"],
            help=agent_model_help
        )
        prompt_a = st.text_area(
            "Prompt Agent A", "Du bist ein Finanzberater auf Topniveau…", height=100,
            help=prompt_help
        )
    with col2:
        provider_b = st.selectbox(
            "Agent B Anbieter", ["OpenAI", "Gemini"],
            help=agent_provider_help
        )
        model_b = st.selectbox(
            "Agent B Modell",
            ["gpt-3.5-turbo", "gpt-4"] if provider_b == "OpenAI" else ["gemini-proto"],
            help=agent_model_help
        )
        prompt_b = st.text_area(
            "Prompt Agent B", "Du bist ein Risikomanager auf Expert:innen-Level…", height=100,
            help=prompt_help
        )

    # ── Sidebar: Konsens-Einstellungen ──────────────────────
    st.sidebar.markdown("### Konsens-Einstellungen")
    cfg = ConsensusConfig()  # Standard-Defaults laden

    divergence_rounds = st.sidebar.number_input(
        "Divergenz-Runden", 1, 20, getattr(cfg, "divergence_rounds", 3),
        help=(
            "Wie viele Runden die beiden KIs abwechselnd neue Ideen und Perspektiven liefern sollen. "
            "Mehr Runden = mehr Vielfalt, aber dauert länger."
        )
    )
    divergence_threshold = st.sidebar.slider(
        "Divergenz-Threshold", 0.0, 1.0, getattr(cfg, "divergence_threshold", 0.5),
        help=(
            "Steuert, wie unterschiedlich eine neue Antwort im Vergleich zur vorherigen sein muss, um als neue Perspektive gezählt zu werden. "
            "0 = völlig anders, 1 = identisch. Nutze niedrigere Werte für mehr Abwechslung."
        )
    )
    convergence_threshold = st.sidebar.slider(
        "Konvergenz-Threshold", 0.0, 1.0, getattr(cfg, "convergence_threshold", 0.8),
        help=(
            "Ab welchem Ähnlichkeitswert die beiden KIs als inhaltlich einverstanden gelten und die Debatte endet. "
            "Höhere Werte = strengerer Konsens."
        )
    )
    max_total = st.sidebar.number_input(
        "Max. Gesamt-Beiträge", 1, 50, getattr(cfg, "max_rounds_total", getattr(cfg, "max_rounds", 10)),
        help=(
            "Gesamtzahl aller Nachrichten (Divergenz + Konvergenz) bevor die Debatte automatisch stoppt. "
            "Schützt vor Endlosschleifen."
        )
    )
    manual_pause = st.sidebar.checkbox(
        "Manueller Stopp möglich", value=getattr(cfg, "manual_pause", False),
        help=(
            "Wenn aktiviert, kannst du jederzeit manuell aufhören, indem du in der App auf den Stop-Button klickst."
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
    api_key = st.secrets["openai_api_key"]
    def make_agent(name, provider, model, prompt):
        if provider == "OpenAI":
            return OpenAIAdapter(name, api_key, model=model, temperature=0.7)
        return GeminiAdapter(name, api_key, model=model)

    agent_a = make_agent("Agent A", provider_a, model_a, prompt_a)
    agent_b = make_agent("Agent B", provider_b, model_b, prompt_b)

    orchestrator = ConsensusOrchestrator(cfg)

    # ── Hauptbereich: Thema eingeben & Diskussion starten ────
    topic = st.text_area("Thema / Idee", height=120)
    if st.button("Diskussion starten") and topic:
        history = orchestrator.run(agent_a, agent_b, initial_prompt=topic)

        # Nur das finale Ergebnis anzeigen
        final_agent, final_text = history[-1]
        st.markdown("### Finale Empfehlung")
        st.markdown(f"**{final_agent}:** {final_text}")


if __name__ == "__main__":
    main()

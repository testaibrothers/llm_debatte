import os, sys
# Suchpfad um eine Ebene nach oben erweitern
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus import ConsensusOrchestrator
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter

def main():
    st.set_page_config(page_title="KI-Debattenplattform", layout="centered")
    st.title("🤖 KI-Debattenplattform – Modular")

    # Sidebar: Agenten-Konfiguration
    col1, col2 = st.sidebar.columns(2)
    with col1:
        provider_a = st.selectbox("Agent A Anbieter", ["OpenAI", "Gemini"])
        model_a    = st.selectbox("Agent A Modell",
                       ["gpt-3.5-turbo","gpt-4"] if provider_a=="OpenAI"
                       else ["gemini-proto"])
        prompt_a   = st.text_area("Prompt Agent A",
                       "Du bist ein Finanzberater auf Topniveau...", height=100)
    with col2:
        provider_b = st.selectbox("Agent B Anbieter", ["OpenAI", "Gemini"])
        model_b    = st.selectbox("Agent B Modell",
                       ["gpt-3.5-turbo","gpt-4"] if provider_b=="OpenAI"
                       else ["gemini-proto"])
        prompt_b   = st.text_area("Prompt Agent B",
                       "Du bist ein Risikomanager auf Expert:innen-Level...", height=100)

    # Sidebar: Konsens-Einstellungen
    st.sidebar.markdown("### Konsens-Einstellungen")
    base_cfg = ConsensusConfig()
    cfg = ConsensusConfig(
        divergence_rounds     = st.sidebar.number_input(
                                   "Divergenz-Runden",
                                   min_value=1,
                                   max_value=20,
                                   value=base_cfg.divergence_rounds),
        divergence_threshold  = st.sidebar.slider(
                                   "Divergenz-Threshold",
                                   0.0, 1.0,
                                   value=base_cfg.divergence_threshold),
        convergence_threshold = st.sidebar.slider(
                                   "Konvergenz-Threshold",
                                   0.0, 1.0,
                                   value=base_cfg.convergence_threshold),
        max_rounds_total      = st.sidebar.number_input(
                                   "Max. Gesamt-Beiträge",
                                   min_value=1,
                                   max_value=50,
                                   value=base_cfg.max_rounds_total),
        manual_pause          = st.sidebar.checkbox(
                                   "Manueller Stopp möglich",
                                   value=base_cfg.manual_pause),
        stop_on_manual        = True,
        log_level             = base_cfg.log_level
    )

    # Agenten erzeugen
    api_key = st.secrets["openai_api_key"]
    def make_agent(name, provider, model, prompt):
        if provider == "OpenAI":
            return OpenAIAdapter(name, api_key, model=model, temperature=0.7)
        else:
            return GeminiAdapter(name, api_key, model=model)
    agent_a = make_agent("Agent A", provider_a, model_a, prompt_a)
    agent_b = make_agent("Agent B", provider_b, model_b, prompt_b)

    orchestrator = ConsensusOrchestrator(cfg)

    # Hauptbereich: Thema eingeben
    topic = st.text_area("Thema / Idee", height=120)
    if st.button("Diskussion starten") and topic:
        history = orchestrator.run(agent_a, agent_b, initial_prompt=topic)

        # Nur das finale Ergebnis anzeigen
        final_agent, final_text = history[-1]
        st.markdown("### Finale Empfehlung")
        st.markdown(f"**{final_agent}:** {final_text}")

if __name__ == "__main__":
    main()

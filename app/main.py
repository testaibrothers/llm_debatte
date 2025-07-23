import os, sys
# eine Ebene über 'app/' zum Modul-Suchpfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus_engine import ConsensusEngine
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter

# Initialisiere Session State Defaults
if 'provider' not in st.session_state:
    st.session_state.provider = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'prompt' not in st.session_state:
    st.session_state.prompt = None
if 'config' not in st.session_state:
    st.session_state.config = None

# Wizard Stepper UI
st.sidebar.title("Navigiere")
steps = ["Agents konfigurieren", "Konsensregeln einstellen", "Diskussion starten"]
# Radio-Widget für Schrittwahl (nur Local Variable, kein Session State)
step_selection = st.sidebar.radio(
    "Schritt im Prozess",
    steps,
    index=0,
    key="step_selector_radio"
)
# Berechne aktuellen Schritt aus der Auswahl
step = steps.index(step_selection) + 1

# LLM Einstellungen (Step 1) (Step 1) (Step 1)
if st.session_state.step == 1:
    st.header("1. Agents konfigurieren")
    provider = st.selectbox("Anbieter", ["OpenAI", "Gemini"])
    model = st.selectbox("Modell", ["gpt-3.5-turbo", "gpt-4"] if provider=="OpenAI" else ["gemini-proto"])
    prompt = st.text_area("System-Prompt:", "Du bist ein Finanzberater...")
    if st.button("Weiter zu Konsensregeln"):
        st.session_state.provider = provider
        st.session_state.model = model
        st.session_state.prompt = prompt
        st.session_state.step = 2
        st.experimental_rerun()

# Konsensregeln einstellen (Step 2)
elif st.session_state.step == 2:
    st.header("2. Konsensregeln einstellen")
    cfg = ConsensusConfig()
    divergence = st.number_input("Divergenz-Runden", 1, 20, cfg.divergence_rounds)
    convergence = st.slider("Konvergenz-Threshold", 0.0, 1.0, cfg.convergence_threshold)
    max_total = st.number_input("Max. Gesamt-Beiträge", 1, 50, cfg.max_rounds_total)
    manual = st.checkbox("Manueller Stopp möglich", value=cfg.manual_pause)
    if st.button("Weiter zu Diskussion starten"):
        cfg.divergence_rounds = divergence
        cfg.convergence_threshold = convergence
        cfg.max_rounds_total = max_total
        cfg.manual_pause = manual
        st.session_state.config = cfg
        st.session_state.step = 3
        st.experimental_rerun()

# Diskussion starten (Step 3)
else:
    st.header("3. Diskussion starten")
    cfg = st.session_state.config
    provider = st.session_state.provider
    model = st.session_state.model
    prompt = st.session_state.prompt
    # Agent Instanz
    api_key = st.secrets.get("openai_api_key", "") if provider=="OpenAI" else st.secrets.get("gemini_api_key", "")
    agent = OpenAIAdapter("Agent", api_key, model=model, temperature=0.7) if provider=="OpenAI" else GeminiAdapter("Agent", api_key, model=model)
    engine = ConsensusEngine(cfg)
    if st.button("Diskussion starten"):
        history = engine.run(agent, agent, prompt)
        st.success("Diskussion abgeschlossen. Finale Empfehlung:")
        st.write(history[-1][1])

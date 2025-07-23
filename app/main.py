import os, sys
# eine Ebene über 'app/' zum Modul-Suchpfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus_engine import ConsensusEngine
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter

# --- Session State Defaults ---
if 'agent_a' not in st.session_state:
    st.session_state.agent_a = {'provider': 'OpenAI', 'model': 'gpt-3.5-turbo', 'prompt': 'Du bist Agent A...'}
if 'agent_b' not in st.session_state:
    st.session_state.agent_b = {'provider': 'OpenAI', 'model': 'gpt-3.5-turbo', 'prompt': 'Du bist Agent B...'}
if 'consensus_config' not in st.session_state:
    st.session_state.consensus_config = ConsensusConfig()

# --- Wizard Steps ---
st.sidebar.title("Navigiere")
steps = ["Agents konfigurieren", "Konsensregeln einstellen", "Diskussion starten"]
step = st.sidebar.radio("Schritt im Prozess", steps, index=0)

# --- Step 1: Agenten konfigurieren ---
if step == steps[0]:
    st.header("1. Agents konfigurieren")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Agent A")
        a = st.session_state.agent_a
        a['provider'] = st.selectbox("Anbieter A", ["OpenAI","Gemini"], index=["OpenAI","Gemini"].index(a['provider']))
        models_a = ["gpt-3.5-turbo","gpt-4"] if a['provider']=="OpenAI" else ["gemini-proto"]
        a['model'] = st.selectbox("Modell A", models_a, index=models_a.index(a['model']) if a['model'] in models_a else 0)
        a['prompt'] = st.text_area("Prompt A", a['prompt'], height=100)
    with col2:
        st.subheader("Agent B")
        b = st.session_state.agent_b
        b['provider'] = st.selectbox("Anbieter B", ["OpenAI","Gemini"], index=["OpenAI","Gemini"].index(b['provider']))
        models_b = ["gpt-3.5-turbo","gpt-4"] if b['provider']=="OpenAI" else ["gemini-proto"]
        b['model'] = st.selectbox("Modell B", models_b, index=models_b.index(b['model']) if b['model'] in models_b else 0)
        b['prompt'] = st.text_area("Prompt B", b['prompt'], height=100)

# --- Step 2: Konsensregeln einstellen ---
elif step == steps[1]:
    st.header("2. Konsensregeln einstellen")
    cfg = st.session_state.consensus_config
    cfg.divergence_rounds = st.number_input("Divergenz-Runden", 1, 20, cfg.divergence_rounds)
    cfg.divergence_threshold = st.slider("Divergenz-Threshold", 0.0, 1.0, cfg.divergence_threshold)
    cfg.convergence_threshold = st.slider("Konvergenz-Threshold", 0.0, 1.0, cfg.convergence_threshold)
    cfg.max_rounds_total = st.number_input("Max. Gesamt-Beiträge", 1, 50, cfg.max_rounds_total)
    cfg.manual_pause = st.checkbox("Manueller Stopp möglich", value=cfg.manual_pause)

# --- Step 3: Diskussion starten ---
else:
    st.header("3. Diskussion starten")
    # Zusammenfassung der Einstellungen
    st.subheader("Agent A")
    st.write(st.session_state.agent_a)
    st.subheader("Agent B")
    st.write(st.session_state.agent_b)
    st.subheader("Konsens-Parameter")
    st.write(st.session_state.consensus_config)

    # Agenten instanziieren
    def make_agent(config):
        api_key = st.secrets.get("openai_api_key","") if config['provider']=="OpenAI" else st.secrets.get("gemini_api_key","")
        if config['provider']=="OpenAI":
            return OpenAIAdapter(config.get('name',"Agent"), api_key, model=config['model'], temperature=0.7)
        else:
            return GeminiAdapter(config.get('name',"Agent"), api_key, model=config['model'])

    agent_a = make_agent({**st.session_state.agent_a, 'name':'Agent A'})
    agent_b = make_agent({**st.session_state.agent_b, 'name':'Agent B'})
    engine = ConsensusEngine(st.session_state.consensus_config)

    if st.button("Diskussion starten"):
        history = engine.run(agent_a, agent_b, initial_prompt=st.session_state.agent_a['prompt'])
        st.success("Diskussion abgeschlossen. Finale Empfehlung:")
        st.write(history[-1][1])

# app/main.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus_engine import ConsensusEngine
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter

# --- Session State Defaults ---
if 'cfg' not in st.session_state:
    st.session_state.cfg = ConsensusConfig()
if 'topic' not in st.session_state:
    st.session_state.topic = ""

# Sidebar: Einstellungen
st.sidebar.title("Konsens-System konfigurieren")
cfg = st.sidebar.experimental_singleton(lambda: st.session_state.cfg)
# Agentenauswahl
with st.sidebar.expander("LLM-Einstellungen"):
    provider_a = st.selectbox("Agent A Anbieter", ["OpenAI", "Gemini"], key="provider_a")
    model_a = st.selectbox("Agent A Modell", ["gpt-3.5-turbo", "gpt-4"] if provider_a=="OpenAI" else ["gemini-proto"], key="model_a")
    st.text_area("Prompt Agent A", st.session_state.cfg.ROLE_PROMPT_A, key="prompt_a")

    provider_b = st.selectbox("Agent B Anbieter", ["OpenAI", "Gemini"], key="provider_b")
    model_b = st.selectbox("Agent B Modell", ["gpt-3.5-turbo", "gpt-4"] if provider_b=="OpenAI" else ["gemini-proto"], key="model_b")
    st.text_area("Prompt Agent B", st.session_state.cfg.ROLE_PROMPT_B, key="prompt_b")

with st.sidebar.expander("Konsens-Einstellungen"):
    # Parameter
    st.slider("Temp Divergenz", 0.1, 2.0, st.session_state.cfg.TEMP_DIV, 0.05, key="TEMP_DIV")
    st.slider("Temp Konvergenz", 0.1, 2.0, st.session_state.cfg.TEMP_CONV, 0.05, key="TEMP_CONV")
    st.number_input("Max Divergenz-Runden", 1, 20, st.session_state.cfg.MAX_DIVERGENCE_ROUNDS, key="MAX_DIVERGENCE_ROUNDS")
    st.number_input("Max Konvergenz-Runden", 1, 20, st.session_state.cfg.MAX_CONVERGENCE_ROUNDS, key="MAX_CONVERGENCE_ROUNDS")
    st.number_input("Max Gesamt-Runden", 1, 50, st.session_state.cfg.MAX_TOTAL_ROUNDS, key="MAX_TOTAL_ROUNDS")
    st.slider("Similarity Cutoff", 0.7, 0.99, st.session_state.cfg.SIMILARITY_CUTOFF, 0.01, key="SIMILARITY_CUTOFF")
    st.slider("Novelty Threshold", 0.05, 0.3, st.session_state.cfg.NOVELTY_THRESHOLD, 0.01, key="NOVELTY_THRESHOLD")
    st.slider("Combo Bonus %", 0, 50, st.session_state.cfg.COMBO_BONUS_PERCENT, 1, key="COMBO_BONUS_PERCENT")

# --- Hauptbereich ---
st.header("3. Diskussion starten")
# Thema
question = st.text_area("Deine Frage / Thema", value=st.session_state.topic, key="topic")
if st.button("Debatte starten"):
    engine = ConsensusEngine(st.session_state.cfg)
    report, raw_json = engine.run(topic)
    st.markdown(report)
    st.download_button("JSON speichern", raw_json, file_name="debate.json")

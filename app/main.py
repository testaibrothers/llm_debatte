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

# LLM Einstellungen
with st.sidebar.expander("1. LLM-Einstellungen", expanded=True):
    provider_a = st.selectbox("Agent A Anbieter", ["OpenAI", "Gemini"], key="provider_a")
    model_a = st.selectbox(
        "Agent A Modell",
        ["gpt-3.5-turbo", "gpt-4"] if provider_a == "OpenAI" else ["gemini-proto"],
        key="model_a"
    )
    prompt_a = st.text_area(
        "Prompt Agent A",
        st.session_state.cfg.ROLE_PROMPT_A,
        key="prompt_a",
        help=st.session_state.cfg.__dataclass_fields__['ROLE_PROMPT_A'].metadata['help']
    )
    provider_b = st.selectbox("Agent B Anbieter", ["OpenAI", "Gemini"], key="provider_b")
    model_b = st.selectbox(
        "Agent B Modell",
        ["gpt-3.5-turbo", "gpt-4"] if provider_b == "OpenAI" else ["gemini-proto"],
        key="model_b"
    )
    prompt_b = st.text_area(
        "Prompt Agent B",
        st.session_state.cfg.ROLE_PROMPT_B,
        key="prompt_b",
        help=st.session_state.cfg.__dataclass_fields__['ROLE_PROMPT_B'].metadata['help']
    )

# Konsens Einstellungen
with st.sidebar.expander("2. Konsens-Einstellungen", expanded=False):
    cfg = st.session_state.cfg
    cfg.TEMP_DIV = st.slider(
        "Temperatur Divergenz", 0.1, 2.0, cfg.TEMP_DIV, 0.05,
        help=cfg.__dataclass_fields__['TEMP_DIV'].metadata['help'], key="TEMP_DIV"
    )
    cfg.TEMP_CONV = st.slider(
        "Temperatur Konvergenz", 0.1, 2.0, cfg.TEMP_CONV, 0.05,
        help=cfg.__dataclass_fields__['TEMP_CONV'].metadata['help'], key="TEMP_CONV"
    )
    cfg.MAX_DIVERGENCE_ROUNDS = st.number_input(
        "Max Divergenz-Runden", 1, 20, cfg.MAX_DIVERGENCE_ROUNDS,
        help=cfg.__dataclass_fields__['MAX_DIVERGENCE_ROUNDS'].metadata['help'], key="MAX_DIVERGENCE_ROUNDS"
    )
    cfg.MAX_CONVERGENCE_ROUNDS = st.number_input(
        "Max Konvergenz-Runden", 1, 20, cfg.MAX_CONVERGENCE_ROUNDS,
        help=cfg.__dataclass_fields__['MAX_CONVERGENCE_ROUNDS'].metadata['help'], key="MAX_CONVERGENCE_ROUNDS"
    )
    cfg.MAX_TOTAL_ROUNDS = st.number_input(
        "Max Gesamt-Runden", 1, 50, cfg.MAX_TOTAL_ROUNDS,
        help=cfg.__dataclass_fields__['MAX_TOTAL_ROUNDS'].metadata['help'], key="MAX_TOTAL_ROUNDS"
    )
    cfg.SIMILARITY_CUTOFF = st.slider(
        "Similarity Cutoff", 0.7, 0.99, cfg.SIMILARITY_CUTOFF, 0.01,
        help=cfg.__dataclass_fields__['SIMILARITY_CUTOFF'].metadata['help'], key="SIMILARITY_CUTOFF"
    )
    cfg.NOVELTY_THRESHOLD = st.slider(
        "Novelty Threshold", 0.05, 0.3, cfg.NOVELTY_THRESHOLD, 0.01,
        help=cfg.__dataclass_fields__['NOVELTY_THRESHOLD'].metadata['help'], key="NOVELTY_THRESHOLD"
    )
    cfg.COMBO_BONUS_PERCENT = st.slider(
        "Combo Bonus %", 0.0, 50.0, float(cfg.COMBO_BONUS_PERCENT), 1.0,
        help=cfg.__dataclass_fields__['COMBO_BONUS_PERCENT'].metadata['help'], key="COMBO_BONUS_PERCENT"
    )

# Hauptbereich
st.header("3. Diskussion starten")
# Fragefeld, speichert lokal in 'question'
question = st.text_area(
    "Deine Frage / Thema", st.session_state.topic, key="topic_input"
)
if st.button("Debatte starten"):
    engine = ConsensusEngine(st.session_state.cfg)
    with st.spinner("Diskussion läuft…"):
        try:
            report_markdown, raw_json = engine.run_debate(question)
        except Exception as e:
            st.error(f"Debatte fehlgeschlagen: {e}")
        else:
            st.markdown(report_markdown, unsafe_allow_html=True)
            st.download_button(
                label="JSON speichern",
                data=raw_json,
                file_name="debate.json",
                mime="application/json"
            )

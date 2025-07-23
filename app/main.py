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
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Sidebar: Konsens-System konfigurieren ---
st.sidebar.title("Konsens-System konfigurieren")

# Kreativität
st.sidebar.subheader("Kreativität")
cfg = st.session_state.cfg
cfg.TEMP_DIV = st.sidebar.slider(
    "Temperatur (Divergenz)", 0.1, 2.0, cfg.TEMP_DIV, 0.05,
    help=cfg.__dataclass_fields__['TEMP_DIV'].metadata['help']
)
cfg.TEMP_CONV = st.sidebar.slider(
    "Temperatur (Konvergenz)", 0.1, 2.0, cfg.TEMP_CONV, 0.05,
    help=cfg.__dataclass_fields__['TEMP_CONV'].metadata['help']
)

# Runden-Limits
st.sidebar.subheader("Runden-Limits")
cfg.MAX_DIVERGENCE_ROUNDS = st.sidebar.number_input(
    "Max Divergenz-Runden", 1, 20, cfg.MAX_DIVERGENCE_ROUNDS,
    help=cfg.__dataclass_fields__['MAX_DIVERGENCE_ROUNDS'].metadata['help']
)
cfg.MAX_CONVERGENCE_ROUNDS = st.sidebar.number_input(
    "Max Konvergenz-Runden", 1, 20, cfg.MAX_CONVERGENCE_ROUNDS,
    help=cfg.__dataclass_fields__['MAX_CONVERGENCE_ROUNDS'].metadata['help']
)
cfg.MAX_TOTAL_ROUNDS = st.sidebar.number_input(
    "Max Gesamt-Runden", 1, 50, cfg.MAX_TOTAL_ROUNDS,
    help=cfg.__dataclass_fields__['MAX_TOTAL_ROUNDS'].metadata['help']
)

# Metrik-Schwellen
st.sidebar.subheader("Metrik-Schwellen")
cfg.SIMILARITY_CUTOFF = st.sidebar.slider(
    "Similarity Cutoff", 0.70, 0.99, cfg.SIMILARITY_CUTOFF, 0.01,
    help=cfg.__dataclass_fields__['SIMILARITY_CUTOFF'].metadata['help']
)
cfg.NOVELTY_THRESHOLD = st.sidebar.slider(
    "Novelty Threshold", 0.05, 0.30, cfg.NOVELTY_THRESHOLD, 0.01,
    help=cfg.__dataclass_fields__['NOVELTY_THRESHOLD'].metadata['help']
)
cfg.COMBO_BONUS_PERCENT = st.sidebar.slider(
    "Combo Bonus %", 0.0, 50.0, cfg.COMBO_BONUS_PERCENT, 1.0,
    help=cfg.__dataclass_fields__['COMBO_BONUS_PERCENT'].metadata['help']
)

# Score-Gewichte
st.sidebar.subheader("Score-Gewichte")
weights = [
    ('Nutzen', 'WEIGHT_NUTZEN'),
    ('Risiko', 'WEIGHT_RISIKO'),
    ('Kosten', 'WEIGHT_KOSTEN'),
    ('Machbarkeit', 'WEIGHT_MACHB')
]
total = 0
for label, field in weights:
    value = st.sidebar.slider(
        f"{label}", 0.0, 1.0, getattr(cfg, field), 0.05,
        help=cfg.__dataclass_fields__[field].metadata['help']
    )
    setattr(cfg, field, value)
    total += value
# Normierung
if total > 0:
    for _, field in weights:
        setattr(cfg, field, getattr(cfg, field) / total)

# Prompts
st.sidebar.subheader("Prompt-Texte")
cfg.SYSTEM_PROMPT = st.sidebar.text_area(
    "System Prompt", cfg.SYSTEM_PROMPT, height=100, 
    help=cfg.__dataclass_fields__['SYSTEM_PROMPT'].metadata['help']
)
cfg.ROLE_PROMPT_A = st.sidebar.text_area(
    "Role Prompt A", cfg.ROLE_PROMPT_A, height=80,
    help=cfg.__dataclass_fields__['ROLE_PROMPT_A'].metadata['help']
)
cfg.ROLE_PROMPT_B = st.sidebar.text_area(
    "Role Prompt B", cfg.ROLE_PROMPT_B, height=80,
    help=cfg.__dataclass_fields__['ROLE_PROMPT_B'].metadata['help']
)

# Hauptbereich
st.title("KI-Konsens Debatte")
question = st.text_input("Deine Frage:", key="question_input")
if st.button("Debatte starten"):
    if not question:
        st.error("Bitte eine Frage eingeben.")
    else:
        with st.spinner("Diskussion läuft …"):
            engine = ConsensusEngine(cfg)
            report, raw_json = engine.run_debate(question)
            st.markdown(report)
            st.download_button("JSON speichern", raw_json, file_name="debate.json")

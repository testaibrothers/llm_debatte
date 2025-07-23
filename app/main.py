# app/main.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus_engine import ConsensusEngine
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter
import json

# Sidebar: Konsens-Einstellungen
st.sidebar.title("Konsens-System konfigurieren")
# Config laden
cfg = ConsensusConfig()
# Kreativitäts-Parameter
cfg.TEMP_DIV = st.sidebar.slider(
    "Temperatur Divergenz (TEMP_DIV)",
    0.1, 2.0, cfg.TEMP_DIV, 0.05,
    help=cfg.__dataclass_fields__["TEMP_DIV"].metadata["help"]
)
cfg.TEMP_CONV = st.sidebar.slider(
    "Temperatur Konvergenz (TEMP_CONV)",
    0.1, 2.0, cfg.TEMP_CONV, 0.05,
    help=cfg.__dataclass_fields__["TEMP_CONV"].metadata["help"]
)
# Runden-Limits
cfg.MAX_DIVERGENCE_ROUNDS = st.sidebar.number_input(
    "Max Divergenz-Runden (MAX_DIVERGENCE_ROUNDS)",
    min_value=1, value=cfg.MAX_DIVERGENCE_ROUNDS,
    help=cfg.__dataclass_fields__["MAX_DIVERGENCE_ROUNDS"].metadata["help"]
)
cfg.MAX_CONVERGENCE_ROUNDS = st.sidebar.number_input(
    "Max Konvergenz-Runden (MAX_CONVERGENCE_ROUNDS)",
    min_value=1, value=cfg.MAX_CONVERGENCE_ROUNDS,
    help=cfg.__dataclass_fields__["MAX_CONVERGENCE_ROUNDS"].metadata["help"]
)
cfg.MAX_TOTAL_ROUNDS = st.sidebar.number_input(
    "Max Gesamt-Runden (MAX_TOTAL_ROUNDS)",
    min_value=1, value=cfg.MAX_TOTAL_ROUNDS,
    help=cfg.__dataclass_fields__["MAX_TOTAL_ROUNDS"].metadata["help"]
)
# Metrik-Schwellen\                                                                                                                               
cfg.SIMILARITY_CUTOFF = st.sidebar.slider(
    "Similarity Cutoff (SIMILARITY_CUTOFF)",
    0.70, 0.99, cfg.SIMILARITY_CUTOFF, 0.01,
    help=cfg.__dataclass_fields__["SIMILARITY_CUTOFF"].metadata["help"]
)
cfg.NOVELTY_THRESHOLD = st.sidebar.slider(
    "Novelty Threshold (NOVELTY_THRESHOLD)",
    0.05, 0.30, cfg.NOVELTY_THRESHOLD, 0.01,
    help=cfg.__dataclass_fields__["NOVELTY_THRESHOLD"].metadata["help"]
)
cfg.COMBO_BONUS_PERCENT = st.sidebar.slider(
    "Combo Bonus % (COMBO_BONUS_PERCENT)",
    0.0, 50.0, cfg.COMBO_BONUS_PERCENT, 1.0,
    help=cfg.__dataclass_fields__["COMBO_BONUS_PERCENT"].metadata["help"]
)
# Score-Gewichte
weights = ["WEIGHT_NUTZEN","WEIGHT_RISIKO","WEIGHT_KOSTEN","WEIGHT_MACHB"]
sum_weights = sum(getattr(cfg,w) for w in weights)
for w in weights:
    val = st.sidebar.slider(
        f"{w}", 0.0, 1.0, getattr(cfg,w), 0.05,
        help=cfg.__dataclass_fields__[w].metadata["help"]
    )
    setattr(cfg,w, val)
# Normalisiere Summe auf 1.0
total = sum(getattr(cfg,w) for w in weights)
for w in weights:
    setattr(cfg, w, getattr(cfg,w)/total if total else 0)
# Prompt-Texte
cfg.SYSTEM_PROMPT = st.sidebar.text_area(
    "System Prompt (SYSTEM_PROMPT)", cfg.SYSTEM_PROMPT, height=100,
    help=cfg.__dataclass_fields__["SYSTEM_PROMPT"].metadata["help"]
)
cfg.ROLE_PROMPT_A = st.sidebar.text_area(
    "Rolle A Prompt (ROLE_PROMPT_A)", cfg.ROLE_PROMPT_A, height=80,
    help=cfg.__dataclass_fields__["ROLE_PROMPT_A"].metadata["help"]
)
cfg.ROLE_PROMPT_B = st.sidebar.text_area(
    "Rolle B Prompt (ROLE_PROMPT_B)", cfg.ROLE_PROMPT_B, height=80,
    help=cfg.__dataclass_fields__["ROLE_PROMPT_B"].metadata["help"]
)
# Preset-Auswahl
preset = st.sidebar.selectbox(
    "Preset-Modus",
    ["Benutzerdefiniert","Kreativ","Streng","Risk-Aware"]
)
# Presets definieren
def apply_preset(name):
    if name=="Kreativ":
        cfg.TEMP_DIV, cfg.TEMP_CONV = 1.8,0.7
    elif name=="Streng":
        cfg.SIMILARITY_CUTOFF, cfg.NOVELTY_THRESHOLD = 0.95,0.05
    elif name=="Risk-Aware":
        cfg.WEIGHT_RISIKO = 0.5
if preset!="Benutzerdefiniert": apply_preset(preset)

# Hauptbereich
st.title("KI Konsens Debatte")
user_q = st.text_area("1. Dein Thema / Frage", height=80)
if st.button("2. Debatte starten"):
    with st.spinner("Diskussion läuft …"):
        engine = ConsensusEngine(cfg)
        report, raw = engine.run(user_q)
    st.markdown(report)
    st.download_button("3. JSON speichern", raw, file_name="debate.json")

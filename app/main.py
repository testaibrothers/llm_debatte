import os, sys
# eine Ebene über 'app/' zum Modul-Suchpfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus_engine import ConsensusEngine
from agents.openai_adapter import OpenAIAdapter
from agents.gemini_adapter import GeminiAdapter


def main():
    st.set_page_config(page_title="KI-Debattenplattform", layout="centered")
    st.title("🤖 KI-Debattenplattform – Modular")

    # Stepper für Workflow
    step = st.session_state.get("step", 1)
    if "step" not in st.session_state:
        st.session_state.step = 1

    def next_step():
        st.session_state.step += 1
    def prev_step():
        st.session_state.step -= 1

    st.markdown("---")
    cols = st.columns([1,1,1])
    for i, label in enumerate(["1. Agents konfigurieren","2. Konsensregeln","3. Diskussion starten"], start=1):
        if st.session_state.step == i:
            cols[i-1].button(f"▶ {label}", on_click=lambda i=i: st.session_state.update({"step": i}))
        else:
            cols[i-1].button(label, on_click=lambda i=i: st.session_state.update({"step": i}))
    st.markdown("---")

    # STEP 1: Agents konfigurieren
    if st.session_state.step == 1:
        with st.expander("LLM Einstellungen", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                provider_a = st.selectbox("Agent Anbieter", ["OpenAI","Gemini"], key="provider_a")
                model_a = st.selectbox("Modell", ["gpt-3.5-turbo","gpt-4"] if provider_a=="OpenAI" else ["gemini-proto"], key="model_a")
                prompt_a = st.text_area("System-Prompt", "Du bist ein Experte...", key="prompt_a")
            with col2:
                provider_b = st.selectbox("Agent Anbieter", ["OpenAI","Gemini"], key="provider_b")
                model_b = st.selectbox("Modell", ["gpt-3.5-turbo","gpt-4"] if provider_b=="OpenAI" else ["gemini-proto"], key="model_b")
                prompt_b = st.text_area("System-Prompt", "Du bist ein Experte...", key="prompt_b")
        if st.button("Weiter", on_click=next_step): pass

    # STEP 2: Konsensregeln einstellen
    elif st.session_state.step == 2:
        with st.expander("Konsens-Einstellungen", expanded=True):
            base = ConsensusConfig()
            divergence_rounds = st.number_input("Divergenz-Runden",1,20, base.divergence_rounds, key="divergence_rounds")
            divergence_threshold = st.slider("Divergenz-Threshold",0.0,1.0, base.divergence_threshold, key="divergence_threshold")
            convergence_threshold = st.slider("Konvergenz-Threshold",0.0,1.0, base.convergence_threshold, key="convergence_threshold")
            max_total = st.number_input("Max. Gesamt-Beiträge",1,50, base.max_rounds, key="max_rounds_total")
            manual_pause = st.checkbox("Manueller Stopp möglich", value=base.manual_pause, key="manual_pause")
        cols = st.columns(2)
        if cols[0].button("Zurück", on_click=prev_step): pass
        if cols[1].button("Weiter", on_click=next_step): pass

    # STEP 3: Diskussion starten
    else:
        if st.button("Zurück", on_click=prev_step): pass
        topic = st.text_area("Thema / Idee", key="topic")
        if st.button("Diskussion starten"):
            # Config befüllen
            cfg = ConsensusConfig(
                max_rounds=st.session_state.max_rounds_total,
                similarity_threshold=st.session_state.convergence_threshold,
                divergence_rounds=st.session_state.divergence_rounds,
                divergence_threshold=st.session_state.divergence_threshold,
                convergence_threshold=st.session_state.convergence_threshold,
                max_rounds_total=st.session_state.max_rounds_total,
                manual_pause=st.session_state.manual_pause,
                stop_on_manual=True,
                log_level=base.log_level
            )
            # Agents
            openai_key = st.secrets.get("openai_api_key")
            gemini_key = st.secrets.get("gemini_api_key")
            def make_agent(name, provider, model, prompt):
                if provider=="OpenAI": return OpenAIAdapter(name, openai_key, model, 0.7)
                return GeminiAdapter(name, gemini_key, model, 0.7)
            agent_a = make_agent("Agent A", st.session_state.provider_a, st.session_state.model_a, st.session_state.prompt_a)
            agent_b = make_agent("Agent B", st.session_state.provider_b, st.session_state.model_b, st.session_state.prompt_b)

            engine = ConsensusEngine(cfg)
            history = engine.run(agent_a, agent_b, initial_prompt=st.session_state.topic)
            final_agent, final_text = history[-1]
            st.markdown("### Finale Empfehlung")
            st.markdown(f"**{final_agent}:** {final_text}")

if __name__ == "__main__":
    main()

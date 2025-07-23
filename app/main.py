import streamlit as st
from consensus.consensus_config import ConsensusConfig
from consensus.consensus import ConsensusOrchestrator
from agents.openai_adapter import OpenAIAdapter
from utils.json_utils import extract_json_fallback

def main():
    st.set_page_config(page_title="KI-Debattenplattform", layout="centered")
    st.title("🤖 KI-Debattenplattform – Modular")

    # Load config
    config = ConsensusConfig(
        max_rounds=st.sidebar.number_input("Max Runden", 1, 100, ConsensusConfig().max_rounds),
        similarity_threshold=st.sidebar.slider("Consensus-Threshold", 0.0, 1.0, ConsensusConfig().similarity_threshold)
    )

    # Initialize agents
    api_key = st.secrets["openai_api_key"]
    agent_a = OpenAIAdapter("Agent A", api_key, model=st.sidebar.selectbox("Model A", ["gpt-3.5-turbo","gpt-4"]), temperature=st.sidebar.slider("Temp A",0.0,1.0,0.7))
    agent_b = OpenAIAdapter("Agent B", api_key, model=st.sidebar.selectbox("Model B", ["gpt-3.5-turbo","gpt-4"]), temperature=st.sidebar.slider("Temp B",0.0,1.0,0.7))

    orchestrator = ConsensusOrchestrator(config)

    topic = st.text_area("Thema / Idee")
    if st.button("Diskussion starten") and topic:
        history = orchestrator.run(agent_a, agent_b, initial_prompt=topic)
        st.write("### Verlauf")
        for agent, resp in history:
            st.markdown(f"**{agent}:** {resp}")

if __name__ == "__main__":
    main()

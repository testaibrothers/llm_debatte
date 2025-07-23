# consensus/consensus_engine.py
import logging
import time
import json
from typing import Tuple, List, Dict
from consensus.consensus_config import ConsensusConfig
from utils.similarity import cosine_similarity

class ConsensusEngine:
    """
    Engine zur Durchführung von Divergenz- und Konvergenz-Phasen.

    Methoden:
    - run_debate(question: str, cfg: ConsensusConfig) -> Tuple[str, str]
        Führt die Debatte durch und gibt (Markdown-Report, JSON-Log) zurück.
    """
    def __init__(self, config: ConsensusConfig):
        self.cfg = config
        logging.basicConfig(level=logging.INFO)
        self.history: List[Dict] = []  # Pro Runde: {agent, text, agree, issues, similarity}

    def run_debate(self, question: str, agent_a, agent_b) -> Tuple[str, str]:
        # Initial prompt
        prompt = question
        round_idx = 0
        # Divergenz-Phase
        while round_idx < self.cfg.MAX_DIVERGENCE_ROUNDS:
            for agent in (agent_a, agent_b):
                response = agent.call(prompt)
                # Simulate agree/disagree block (simplified)
                similarity = cosine_similarity(prompt, response)
                entry = {
                    "round": round_idx+1,
                    "agent": agent.name,
                    "text": response,
                    "similarity": similarity
                }
                self.history.append(entry)
                prompt = response
            round_idx += 1

        # Konvergenz-Phase
        conv_rounds = 0
        while conv_rounds < self.cfg.MAX_CONVERGENCE_ROUNDS:
            responses = []
            for agent in (agent_a, agent_b):
                response = agent.call(prompt)
                sim = cosine_similarity(prompt, response)
                res_entry = {
                    "round": self.cfg.MAX_DIVERGENCE_ROUNDS + conv_rounds + 1,
                    "agent": agent.name,
                    "text": response,
                    "similarity": sim
                }
                self.history.append(res_entry)
                responses.append(response)
            # Check consensus condition
            if cosine_similarity(responses[0], responses[1]) >= self.cfg.SIMILARITY_CUTOFF:
                break
            prompt = responses[-1]
            conv_rounds += 1

        # Ergebnisreport
        report_lines = [f"**{h['agent']}** (Runde {h['round']}): {h['text']}" for h in self.history]
        report = "\n\n".join(report_lines)
        raw_json = json.dumps(self.history, ensure_ascii=False, indent=2)
        return report, raw_json

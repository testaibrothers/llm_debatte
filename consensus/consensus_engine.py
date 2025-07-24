# consensus/consensus_engine.py
import logging
import time
import json
from typing import Tuple, List, Dict
from consensus.consensus_config import ConsensusConfig
from utils.json_utils import extract_json_block
from utils.similarity import cosine_similarity

class ConsensusEngine:
    """
    Engine zur Durchführung von Divergenz- und Konvergenz-Phasen.

    Die Methode run_debate erwartet nun:
      - question: Die Ausgangsfrage des Nutzers
      - agent_a, agent_b: zwei AgentClient-Instanzen
    Liefert (report_markdown, raw_json)
    """

    def __init__(self, config: ConsensusConfig):
        self.cfg = config
        logging.basicConfig(level=logging.INFO)
        self.history: List[Dict] = []
        self.scores: List[float] = []

    def run_debate(self, question: str, agent_a, agent_b) -> Tuple[str, str]:
        """
        Führt die Debatte mit zwei Agenten durch.
        """
        self.history.clear()
        self.scores.clear()
        start_time = time.time()
        msg = question
        current_agent, other_agent = agent_a, agent_b

        # Divergenz-Phase
        for rnd in range(self.cfg.MAX_DIVERGENCE_ROUNDS):
            response = current_agent.call(msg)
            block = extract_json_block(response)
            score = cosine_similarity(msg, response)
            entry = {"phase": "divergence", "round": rnd+1, "agent": current_agent.name, "text": response, "score": score, "agree": block.get("agree", None)}
            self.history.append(entry)
            self.scores.append(score)
            msg = response
            current_agent, other_agent = other_agent, current_agent

        # Konvergenz-Phase
        for rnd in range(self.cfg.MAX_CONVERGENCE_ROUNDS):
            response = current_agent.call(msg)
            block = extract_json_block(response)
            score = cosine_similarity(msg, response)
            entry = {"phase": "convergence", "round": rnd+1, "agent": current_agent.name, "text": response, "score": score, "agree": block.get("agree", None)}
            self.history.append(entry)
            self.scores.append(score)
            if block.get("agree", False) or score >= self.cfg.SIMILARITY_CUTOFF:
                break
            msg = response
            current_agent, other_agent = other_agent, current_agent

        duration = time.time() - start_time
        # Report generieren
        report = f"# Konsensbericht\n- Dauer: {duration:.2f}s\n- Runden: {len(self.history)}\n\n## Verlauf\n"
        for e in self.history:
            report += f"- [{e['phase']}/{e['round']}] {e['agent']}: Score={e['score']:.2f}\n  {e['text']}\n"

        raw_json = json.dumps({"history": self.history, "scores": self.scores}, ensure_ascii=False)
        return report, raw_json

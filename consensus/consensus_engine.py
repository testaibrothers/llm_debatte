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
    - run_debate(question: str) -> Tuple[str, str]
      Führt die Debatte durch und gibt (report_markdown, raw_json) zurück.
    """

    def __init__(self, config: ConsensusConfig):
        self.cfg = config
        logging.basicConfig(level=logging.INFO)
        self.history: List[Dict] = []
        self.scores: List[float] = []
        self.start_time = None

    def run_debate(self, question: str) -> Tuple[str, str]:
        """
        Hauptmethode: Startet Divergenz- und Konvergenzphasen.
        """
        from agents.openai_adapter import OpenAIAdapter
        from agents.gemini_adapter import GeminiAdapter

        self.start_time = time.time()
        self.history.clear()
        self.scores.clear()

        # Dummy initial message
        msg = question

        # Divergenz-Phase
        for rnd in range(self.cfg.MAX_DIVERGENCE_ROUNDS):
            score = cosine_similarity(msg, question)
            self.scores.append(score)
            self.history.append({"phase": "divergence", "round": rnd+1, "score": score, "text": msg})
            # Dummy message update
            msg = msg

        # Konvergenz-Phase
        for rnd in range(self.cfg.MAX_CONVERGENCE_ROUNDS):
            score = cosine_similarity(msg, question)
            self.scores.append(score)
            self.history.append({"phase": "convergence", "round": rnd+1, "score": score, "text": msg})
            if score >= self.cfg.SIMILARITY_CUTOFF:
                break
            msg = msg

        # Report erstellen
        duration = time.time() - self.start_time
        report = f"# Konsensbericht\n- Dauer: {duration:.2f}s\n- Runden: {len(self.history)}\n\n"
        report += "## Verlauf\n"
        for entry in self.history:
            report += f"- [{entry['phase']}/{entry['round']}] Score={entry['score']:.2f}: {entry['text']}\n"

        raw_json = json.dumps({"history": self.history, "scores": self.scores})
        return report, raw_json

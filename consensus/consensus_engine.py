# consensus/consensus_engine.py
import logging, time, json
from typing import Tuple, List, Dict
from consensus.consensus_config import ConsensusConfig
from utils.similarity import cosine_similarity

class ConsensusEngine:
    def __init__(self, config: ConsensusConfig):
        self.cfg = config
        logging.basicConfig(level=logging.INFO)
        self.history: List[Dict] = []
        self.scores: List[float] = []

    def run_debate(self, question: str) -> Tuple[str, str]:
        """Führt Divergenz- und Konvergenz-Phasen aus und liefert (report, raw_json)."""
        self.history.clear()
        self.scores.clear()
        start = time.time()

        # Dummy-Debatte (ersetze hier mit echtem Agenten-Call)
        for rnd in range(self.cfg.MAX_DIVERGENCE_ROUNDS):
            score = cosine_similarity(question, question)
            self.scores.append(score)
            self.history.append({"phase": "divergence", "round": rnd+1, "score": score, "text": question})

        for rnd in range(self.cfg.MAX_CONVERGENCE_ROUNDS):
            score = cosine_similarity(question, question)
            self.scores.append(score)
            self.history.append({"phase": "convergence", "round": rnd+1, "score": score, "text": question})
            if score >= self.cfg.SIMILARITY_CUTOFF:
                break

        duration = time.time() - start
        report = f"# Konsensbericht\n- Dauer: {duration:.2f}s\n- Runden: {len(self.history)}\n\n## Verlauf\n"
        for e in self.history:
            report += f"- [{e['phase']}/{e['round']}] Score={e['score']:.2f}: {e['text']}\n"

        raw_json = json.dumps({"history": self.history, "scores": self.scores})
        return report, raw_json

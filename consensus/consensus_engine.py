# consensus/consensus_engine.py
import logging
import time
import json
from typing import Tuple, List

from consensus.consensus_config import ConsensusConfig
from utils.similarity import cosine_similarity

class ConsensusEngine:
    """
    Engine zur Durchführung von Divergenz- und Konvergenz-Phasen.
    """
    def __init__(self, config: ConsensusConfig):
        self.cfg = config
        logging.basicConfig(level=logging.INFO)

    def run_debate(self, user_question: str) -> Tuple[str, str]:
        """
        Führt die Debatte durch und gibt (report_markdown, raw_json) zurück.
        """
        # Initialisierung
        history = []  # List[dict]
        report_lines: List[str] = []

        # 1. Divergenz-Phase
        for i in range(self.cfg.MAX_DIVERGENCE_ROUNDS):
            prompt = f"{self.cfg.SYSTEM_PROMPT}\n
User-Thema: {user_question}\n"  \
                     f"Runde {i+1} (Divergenz): Generiere neue Ideen mit Temp {self.cfg.TEMP_DIV}."
            # Hier KI-Aufruf (Adapter) einfügen
            response = self._call_agent(prompt, role_prompt=self.cfg.ROLE_PROMPT_A, temperature=self.cfg.TEMP_DIV)
            history.append({"round": i+1, "phase": "divergence", "response": response})
            report_lines.append(f"- Idee {i+1}: {response}")

        # 2. Konvergenz-Phase
        for j in range(self.cfg.MAX_CONVERGENCE_ROUNDS):
            prompt = f"{self.cfg.SYSTEM_PROMPT}\n
Basierend auf Ideen: {[h['response'] for h in history]}\n"  \
                     f"Runde {j+1} (Konvergenz): Prüfe und kombiniere mit Temp {self.cfg.TEMP_CONV}."
            response = self._call_agent(prompt, role_prompt=self.cfg.ROLE_PROMPT_B, temperature=self.cfg.TEMP_CONV)
            similarity = cosine_similarity(history[-1]["response"], response)
            history.append({"round": j+1, "phase": "convergence", "response": response, "similarity": similarity})
            report_lines.append(f"- Konsolidierung {j+1} (Sim: {similarity:.2f}): {response}")
            if similarity >= self.cfg.SIMILARITY_CUTOFF:
                report_lines.append("**Konsens erreicht!**")
                break

        # 3. Finalbericht
        report_markdown = "## Konsensbericht\n" + "\n".join(report_lines)
        raw_json = json.dumps(history, ensure_ascii=False, indent=2)
        return report_markdown, raw_json

    def _call_agent(self, prompt: str, role_prompt: str, temperature: float) -> str:
        """
        Platzhalter für KI-Adapter-Aufrufe.
        """
        # Aktuell Dummy-Implementierung:
        logging.info(f"Calling agent with temp={temperature}")
        time.sleep(0.5)  # Simuliere Latenz
        return f"[Antwort bei Temp {temperature}]"

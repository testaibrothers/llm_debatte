# consensus/consensus_engine.py
import os, sys
# Eine Ebene über dem Paket-Ordner hinzufügen, damit 'utils' gefunden wird
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import time
import json
from consensus.consensus_config import ConsensusConfig
from utils.similarity import cosine_similarity

class ConsensusEngine:
    """
    Engine zur Orchestrierung von Divergenz- und Konvergenz-Phasen.
    """
    def __init__(self, config: ConsensusConfig):
        self.cfg = config
        logging.basicConfig(level=config.log_level)
        self.history = []  # List of tuples (agent_name, text, agree_block)
        self.similarity_log = []
        self.start_time = time.time()

    def add_message(self, agent_name: str, text: str, agree_block: dict = None):
        self.history.append((agent_name, text, agree_block))

    def has_diverged(self) -> bool:
        if len(self.history) < 2:
            return True
        _, prev_text, _ = self.history[-2]
        _, curr_text, _ = self.history[-1]
        sim = cosine_similarity(prev_text, curr_text)
        self.similarity_log.append(sim)
        return sim <= self.cfg.divergence_threshold

    def has_converged(self, agree_block: dict) -> bool:
        agreed = agree_block.get("agree", False) if agree_block else False
        sim = self.similarity_log[-1] if self.similarity_log else 0.0
        return agreed and sim >= self.cfg.convergence_threshold

    def run(self, agent_a, agent_b, initial_prompt: str):
        round_counter = 0
        current, other = agent_a, agent_b
        text = initial_prompt
        agree_block = {}

        # Divergenz-Phase
        for _ in range(self.cfg.divergence_rounds):
            response = current.call(text)
            try:
                # JSON-Block am Ende parsen
                agree_block = json.loads(response.split("```json\n")[-1])
            except:
                agree_block = {}
            self.add_message(current.name, response, agree_block)
            text = response
            current, other = other, current
            round_counter += 1

        # Konvergenz-Phase
        while round_counter < self.cfg.max_rounds and not self.has_converged(agree_block):
            response = current.call(text)
            try:
                agree_block = json.loads(response.split("```json\n")[-1])
            except:
                agree_block = {}
            self.add_message(current.name, response, agree_block)
            text = response
            current, other = other, current
            round_counter += 1

        # Rückgabe ohne agree_block
        return [(agent, txt) for agent, txt, _ in self.history]

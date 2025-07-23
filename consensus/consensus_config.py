# consensus/consensus.py
import logging
from consensus.consensus_config import ConsensusConfig
from utils.similarity import cosine_similarity

class ConsensusOrchestrator:
    def __init__(self, config: ConsensusConfig):
        self.config = config
        logging.basicConfig(level=config.log_level)
        self.history = []  # List of tuples (agent_name, text)
        self.similarity_log = []

    def add_message(self, agent_name: str, text: str):
        self.history.append((agent_name, text))

    def has_consensus(self) -> bool:
        if len(self.history) < 2:
            return False
        _, prev = self.history[-2]
        _, last = self.history[-1]
        score = cosine_similarity(prev, last)
        self.similarity_log.append(score)
        return score >= self.config.convergence_threshold

    def run(self, agent_a, agent_b, initial_prompt: str):
        round_count = 0
        current, other = agent_a, agent_b
        text = initial_prompt
        # Divergenz-Phase
        for _ in range(self.config.divergence_rounds):
            response = current.call(text)
            self.add_message(current.name, response)
            text = response
            current, other = other, current
        # Konvergenz-Phase
        while round_count < self.config.max_rounds and not self.has_consensus():
            response = current.call(text)
            self.add_message(current.name, response)
            text = response
            current, other = other, current
            round_count += 1
        return self.history

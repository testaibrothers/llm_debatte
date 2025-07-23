# consensus/consensus.py
import logging
from dataclasses import asdict
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

    def has_converged(self) -> bool:
        if len(self.history) < 2:
            return False
        prev = self.history[-2][1]
        curr = self.history[-1][1]
        score = cosine_similarity(prev, curr)
        self.similarity_log.append(score)
        return score >= self.config.convergence_threshold

    def run(self, agent_a, agent_b, initial_prompt: str):
        round_count = 0
        text = initial_prompt
        current_agent, next_agent = agent_a, agent_b

        # Divergenz-Phase
        for _ in range(self.config.divergence_rounds):
            response = current_agent.call(text)
            self.add_message(current_agent.name, response)
            text = response
            current_agent, next_agent = next_agent, current_agent
        
        # Konvergenz-Phase
        while round_count < self.config.max_rounds_total:
            response = current_agent.call(text)
            self.add_message(current_agent.name, response)
            text = response
            if self.has_converged():
                break
            current_agent, next_agent = next_agent, current_agent
            round_count += 1
            if self.config.manual_pause:
                input("Weiter mit [Enter]...")
        return self.history

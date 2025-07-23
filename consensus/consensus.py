import logging
from .consensus_config import ConsensusConfig
from utils.similarity import cosine_similarity

class ConsensusOrchestrator:
    def __init__(self, config: ConsensusConfig):
        self.config = config
        logging.basicConfig(level=config.log_level)
        self.history = []

    def add_message(self, agent_name: str, text: str):
        self.history.append((agent_name, text))

    def has_consensus(self) -> bool:
        if len(self.history) < 2:
            return False
        _, prev = self.history[-2]
        _, last = self.history[-1]
        score = cosine_similarity(prev, last)
        return score >= self.config.similarity_threshold

    def run(self, agent_a, agent_b, initial_prompt: str):
        round_counter = 0
        current_agent, other_agent = agent_a, agent_b
        text = initial_prompt
        while True:
            response = current_agent.call(text)
            self.add_message(current_agent.name, response)

            if self.has_consensus() or round_counter >= self.config.max_rounds:
                break
            if self.config.manual_pause:
                input("Weiter mit nächster Runde? [Enter]")
            text = response
            current_agent, other_agent = other_agent, current_agent
            round_counter += 1

        return self.history

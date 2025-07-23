# consensus/consensus_engine.py

import time
import json
from utils.similarity import cosine_similarity

class ConsensusEngine:
    def __init__(self, config):
        self.cfg = config
        self.history = []  # [(agent_name, text, metrics)]
        self.similarity_log = []
        self.start_time = time.time()

    def add_message(self, agent_name, text, agree_block=None):
        # agree_block ist dict mit agree/open_issues
        metrics = {'agree': None, 'open_issues': []}
        if agree_block:
            metrics.update(agree_block)
        self.history.append((agent_name, text, metrics))

    def get_similarity(self, a, b):
        return cosine_similarity(a, b)

    def run(self, agent_a, agent_b, initial_prompt):
        current, other = agent_a, agent_b
        prompt = initial_prompt
        round_count = 0

        while True:
            # Stop-Conditions
            if round_count >= self.cfg.max_rounds_total:
                break
            if time.time() - self.start_time > 120:
                break  # Timeout nach 120s

            # Agent liefert Antwort + Agree/Disagree-JSON
            response = current.call(prompt)
            try:
                main_text, agree_json = response.split('```json')
                agree_block = json.loads(agree_json)
            except:
                main_text = response
                agree_block = None

            # Loggen und Metriken
            self.add_message(current.name, main_text, agree_block)
            sim = self.get_similarity(
                self.history[-2][1] if len(self.history)>1 else initial_prompt,
                main_text
            )
            self.similarity_log.append(sim)

            # Konsensprüfung
            if agree_block and agree_block.get('agree', False) and sim >= self.cfg.similarity_threshold:
                break

            # Adaptive Threshold
            if len(self.similarity_log) >= 3:
                recent = self.similarity_log[-3:]
                var = max(recent) - min(recent)
                if var > 0.2:
                    self.cfg.similarity_threshold = min(0.9, self.cfg.similarity_threshold + 0.05)
                else:
                    self.cfg.similarity_threshold = max(0.6, self.cfg.similarity_threshold - 0.05)

            # Wechsel
            prompt = main_text
            current, other = other, current
            round_count += 1

        return self.history

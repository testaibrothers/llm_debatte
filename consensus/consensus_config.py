from dataclasses import dataclass

@dataclass
class ConsensusConfig:
    max_rounds: int = 10
    similarity_threshold: float = 0.8
    manual_pause: bool = False
    stop_on_manual: bool = True
    log_level: str = "INFO"

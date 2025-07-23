# consensus/consensus_config.py

from dataclasses import dataclass

@dataclass
class ConsensusConfig:
    # ◾ Legacy-Felder (für bestehenden Orchestrator)
    max_rounds: int = 10
    similarity_threshold: float = 0.8

    # ◾ Divergenz-Phase
    divergence_rounds: int = 3
    divergence_threshold: float = 0.5

    # ◾ Konvergenz-Phase
    convergence_threshold: float = 0.8

    # ◾ Generelle Abbruchkriterien
    max_rounds_total: int = 10
    manual_pause: bool = False
    stop_on_manual: bool = True

    # ◾ Logging
    log_level: str = "INFO"

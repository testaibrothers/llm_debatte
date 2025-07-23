from dataclasses import dataclass

@dataclass
class ConsensusConfig:
    # Divergenz-Phase
    divergence_rounds: int = 3             # Anzahl Divergenz-Zyklen
    divergence_threshold: float = 0.5       # ≤0.5 = Beiträge gelten als divergent

    # Konvergenz-Phase
    convergence_threshold: float = 0.8     # ≥0.8 = Konsens erreicht

    # Generelle Abbruchkriterien
    max_rounds_total: int = 10             # Max Beiträge insgesamt
    manual_pause: bool = False
    stop_on_manual: bool = True

    # Logging
    log_level: str = "INFO"

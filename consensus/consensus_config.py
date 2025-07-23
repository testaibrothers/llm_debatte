# consensus/consensus_config.py

from dataclasses import dataclass

@dataclass
class ConsensusConfig:
    # Divergenz-Phase
    divergence_rounds: int = 3             # Anzahl Divergenz-Zyklen
    divergence_threshold: float = 0.5       # Beiträge gelten als divergent, wenn Cosine-Sim ≤ 0.5

    # Konvergenz-Phase
    convergence_threshold: float = 0.8     # Konsens, wenn Cosine-Sim ≥ 0.8

    # Generelle Abbruchkriterien
    max_rounds_total: int = 10             # Max Beiträge insgesamt (Diver+Konvergenz)
    manual_pause: bool = False             # an jeder Runde pausieren?
    stop_on_manual: bool = True            # manuellen Stopp akzeptieren

    # Logging
    log_level: str = "INFO"
 

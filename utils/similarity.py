# consensus/consensus_config.py
from dataclasses import dataclass, field

@dataclass
class ConsensusConfig:
    # Hard-Cap für alle Beiträge
    max_rounds: int = field(default=10)
    # Startwert für Konvergenz-Threshold (0.0–1.0)
    similarity_threshold: float = field(default=0.8)

    # Einstellungen Divergenz-Phase
    divergence_rounds: int = field(default=3)
    divergence_threshold: float = field(default=0.5)

    # Einstellung Konvergenz-Phase
    convergence_threshold: float = field(default=0.8)

    # Weitere Abbruchkriterien
    max_rounds_total: int = field(default=10)
    manual_pause: bool = field(default=False)
    stop_on_manual: bool = field(default=True)

    # Logging-Level
    log_level: str = field(default="INFO")

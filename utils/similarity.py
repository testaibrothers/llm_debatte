# consensus/consensus_config.py
from dataclasses import dataclass, field

@dataclass
class ConsensusConfig:
    # Gesamtzahl aller Beiträge (Hard-Cap)
    max_rounds: int = field(default=10)
    # Konvergenz-Schwelle: Ähnlichkeit ab der wir Konsens annehmen (0.0–1.0)
    similarity_threshold: float = field(default=0.8)

    # Divergenz-Phase: Anzahl der Runden und Schwelle
    divergence_rounds: int = field(default=3)
    divergence_threshold: float = field(default=0.5)

    # Konvergenz-Phase: wann wir Konsenscheit erreichen
    convergence_threshold: float = field(default=0.8)

    # Gesamt-Abbruch
    max_rounds_total: int = field(default=10)
    manual_pause: bool = field(default=False)
    stop_on_manual: bool = field(default=True)

    # Logging-Level (z.B. INFO, DEBUG)
    log_level: str = field(default="INFO")

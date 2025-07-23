# consensus/consensus_config.py
from dataclasses import dataclass, field

@dataclass
class ConsensusConfig:
    """
    Konfigurationsparameter für die Konsens-Plattform.
    """
    # Hard-Cap: Maximale Gesamtzahl aller Nachrichten (Divergenz + Konvergenz)
    max_rounds: int = field(default=10)
    # Startwert für den Konvergenz-Threshold (0.0–1.0)
    similarity_threshold: float = field(default=0.8)

    # Divergenz-Phase
    # Anzahl der Runden, in denen divergente Ideen generiert werden
    divergence_rounds: int = field(default=3)
    # Divergenz-Threshold: maximale Ähnlichkeit, bis neue Ideen erzwungen werden
    divergence_threshold: float = field(default=0.5)

    # Konvergenz-Phase
    # Schwelle für Konsens nach Divergenz-Runden
    convergence_threshold: float = field(default=0.8)

    # Zusätzliche Abbruchkriterien
    # Gesamtzahl aller Beiträge (zusätzlich zu max_rounds)
    max_rounds_total: int = field(default=10)
    # Manuelles Pausieren per Button erlauben
    manual_pause: bool = field(default=False)
    # Manuellen Stopp akzeptieren
    stop_on_manual: bool = field(default=True)

    # Logging-Detailgrad (z.B. 'INFO', 'DEBUG')
    log_level: str = field(default="INFO")

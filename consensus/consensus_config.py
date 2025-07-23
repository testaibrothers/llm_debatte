# consensus/consensus_config.py
from dataclasses import dataclass, field

@dataclass
class ConsensusConfig:
    # Gesamtzahl aller Beiträge (Hard-Cap)
    max_rounds: int = field(default=10)
    # Konvergenz-Schwelle: Ähnlichkeit, ab der Konsens angenommen wird (0.0–1.0)
    similarity_threshold: float = field(default=0.8)

    # Divergenz-Phase: Anzahl der Runden, um unterschiedliche Ideen zu sammeln
    divergence_rounds: int = field(default=3)
    # Divergenz-Threshold: maximale Ähnlichkeit, um weiterhin Divergenz zu erzwingen
    divergence_threshold: float = field(default=0.5)

    # Konvergenz-Phase: Schwellwert für Konsens nach Divergenz
    convergence_threshold: float = field(default=0.8)

    # Gesamtanzahl Beiträge (Schutz gegen Endlosschleifen)
    max_rounds_total: int = field(default=10)
    # Manueller Stopp: zeigt Button für manuelles Pausieren
    manual_pause: bool = field(default=False)
    # Akzeptiert manuellen Stop als Abbruchkriterium
    stop_on_manual: bool = field(default=True)

    # Logging-Detailgrad (z. B. "INFO", "DEBUG")
    log_level: str = field(default="INFO")

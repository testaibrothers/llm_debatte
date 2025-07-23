# consensus/consensus_config.py
from dataclasses import dataclass, field

@dataclass
class ConsensusConfig:
    """
    Konfigurationsparameter für die Konsens-Plattform.
    """
    # Gesamtzahl aller Beiträge (Hard-Cap)
    max_rounds: int = field(default=10)
    # Konvergenz-Schwelle: Ähnlichkeitsempfindlichkeit (0.0–1.0)
    similarity_threshold: float = field(default=0.8)

    # Anzahl der Divergenz-Runden (Standard: 3)
    divergence_rounds: int = field(default=3)
    # Divergenz-Threshold: maximale Ähnlichkeit, um weiterhin neue Ideen zu fördern
    divergence_threshold: float = field(default=0.5)

    # Konvergenz-Phase: Schwelle für Konsens nach Divergenz-Runden
    convergence_threshold: float = field(default=0.8)

    # Gesamtanzahl an Beiträgen (zusätzliche Schutzschicht gegen Endlosschleifen)
    max_rounds_total: int = field(default=10)
    # Manueller Stopp: zeigt in der UI einen Button für manuelles Pausieren
    manual_pause: bool = field(default=False)
    # Akzeptiert manuellen Stop als Abbruchkriterium
    stop_on_manual: bool = field(default=True)

    # Logging-Detailgrad (z. B. "INFO", "DEBUG")
    log_level: str = field(default="INFO")

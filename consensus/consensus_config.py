# consensus/consensus_config.py
from pydantic import BaseModel, Field, validator

class ConsensusConfig(BaseModel):
    # Obergrenze für alle Beiträge (Hard-Cap)
    max_rounds: int = Field(10, description="Hard-Cap für Gesamt-Beiträge, danach Stop")
    # Initialer Konvergenz-Threshold (wird ggf. adaptiv angepasst)
    similarity_threshold: float = Field(0.8, description="Startwert für Konvergenz-Schwelle")
    
    # Divergenz-Phase: wie viele Runden, bevor wir in Konvergenz übergehen
    divergence_rounds: int = Field(3, description="Anzahl der Divergenz-Runden (Standard: 3)")
    # Divergenz-Threshold: wie unterschiedlich Antworten sein müssen
    divergence_threshold: float = Field(0.5, description="Maximale Ähnlichkeit, um noch divergente Ideen zu erzwingen")

    # Konvergenz-Phase: ab welchem Ähnlichkeitswert gilt Konsens
    convergence_threshold: float = Field(0.8, description="Schwelle für Konsens nach Divergenz")

    # Zusätzliche Abbruchkriterien
    max_rounds_total: int = Field(10, description="Gesamtzahl aller Beiträge (Standard: 10)")
    manual_pause: bool = Field(False, description="Einschalten eines manuellen Stop-Buttons")
    stop_on_manual: bool = Field(True, description="Ob manueller Stop akzeptiert wird")

    # Logging-Level
    log_level: str = Field("INFO", description="Logging-Detailgrad")

    @validator('similarity_threshold', 'divergence_threshold', 'convergence_threshold')
    def check_threshold(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError("Threshold muss zwischen 0.0 und 1.0 liegen")
        return v

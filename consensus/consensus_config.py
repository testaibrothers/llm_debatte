# consensus/consensus_config.py

from dataclasses import dataclass

@dataclass
class ConsensusConfig:
    # ◾ Legacy-Felder (für bestehenden Orchestrator)
    max_rounds: int = 10
    similarity_threshold: float = 0.8

    # ◾ Divergenz-Phase
    divergence_rounds: int = 3             # Zyklen, in denen clean divergiert wird
    divergence_threshold: float = 0.5       # Beiträge gelten als divergent, wenn CosSim ≤ 0.5

    # ◾ Konvergenz-Phase
    convergence_threshold: float = 0.8     # Konsens, wenn CosSim ≥ 0.8

    # ◾ Generelle Abbruchkriterien
    max_rounds_total: int = 10             # Alternative für max_rounds
    manual_pause: bool = False             # jede Runde pausieren?
    stop_on_manual: bool = True            # manuellen Stopp akzeptieren

    # ◾ Logging
    log_level: str = "INFO"

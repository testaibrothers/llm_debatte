# consensus/consensus_config.py
from dataclasses import dataclass, field

@dataclass
class ConsensusConfig:
    # Kreativität in der Divergenz-Phase
    TEMP_DIV: float = field(default=1.2, metadata={"help": "Temperatur der Ideen-Phase. 1.3 = riskantere Vorschläge, 0.8 = konservativ."})
    # Kreativität in der Konvergenz-Phase
    TEMP_CONV: float = field(default=0.5, metadata={"help": "Temperatur der Prüf-Phase. 0.4 = präzise Argumente."})

    # Runden-Limits
    MAX_DIVERGENCE_ROUNDS: int = field(default=6, metadata={"help": "Max. Ideensammel-Runden. 8 = viel Brainstorming."})
    MAX_CONVERGENCE_ROUNDS: int = field(default=6, metadata={"help": "Max. Bewertungs-/Auswahl-Runden."})
    MAX_TOTAL_ROUNDS: int = field(default=12, metadata={"help": "Hartes Gesamt-Limit, inkl. Zusatzrunden."})

    # Metrik-Schwellen
    SIMILARITY_CUTOFF: float = field(default=0.85, metadata={"help": "Mind. inhaltl. Übereinstimmung für Konsens. 0.9 = sehr streng."})
    NOVELTY_THRESHOLD: float = field(default=0.10, metadata={"help": "Minimaler Neuheitsabstand. 0.15 = 15 % anders als bekannte Ideen."})
    COMBO_BONUS_PERCENT: float = field(default=10.0, metadata={"help": "Zusatz-Vorteil, den eine Kombi liefern muss. 10 % = sinnvoll."})

    # Score-Gewichte (Summe sollte 1.0 ergeben)
    WEIGHT_NUTZEN: float = field(default=0.40, metadata={"help": "Einfluss des Nutzens auf Gesamtpunktzahl."})
    WEIGHT_RISIKO: float = field(default=0.30, metadata={"help": "Einfluss des Risikos auf Gesamtpunktzahl."})
    WEIGHT_KOSTEN: float = field(default=0.20, metadata={"help": "Einfluss der Kosten auf Gesamtpunktzahl."})
    WEIGHT_MACHB: float = field(default=0.10, metadata={"help": "Einfluss der Machbarkeit auf Gesamtpunktzahl."})

    # Prompt-Texte
    SYSTEM_PROMPT: str = field(default="Du bist ein hilfreicher Debatten-Moderator.", metadata={"help": "System-Prompt steuert das Gesamtverhalten."})
    ROLE_PROMPT_A: str = field(default="Du bist Rolle A: Guerilla-Entrepreneur.", metadata={"help": "Rollenbeschreibung für Agent A."})
    ROLE_PROMPT_B: str = field(default="Du bist Rolle B: Risikomanager.", metadata={"help": "Rollenbeschreibung für Agent B."})

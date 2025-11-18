"""Types TypedDict pour la documentation et validation"""
from typing import TypedDict, List

class ResultatDiagnostic(TypedDict):
    """Structure du résultat de diagnostic"""
    succes: bool
    diagnostic: str
    description: str
    gravite: str
    cout_estimatif: str
    conseils: str
    confiance: str
    score: float
    symptomes_utilises: List[str]
    explication_ia: str  # Ajouté par l'assistant IA

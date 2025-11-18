"""Modèle pour représenter un diagnostic"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Diagnostic:
    """Représente un diagnostic automobile"""
    id: str
    nom: str
    description: str
    gravite: str  # Léger, Moyen, Critique
    cout_min: int
    cout_max: int
    symptomes_requis: List[str]  # IDs des symptômes
    symptomes_optionnels: List[str] = None
    conseils: Optional[str] = None
    
    def __post_init__(self):
        if self.symptomes_optionnels is None:
            self.symptomes_optionnels = []
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'gravite': self.gravite,
            'cout_estimatif': f"{self.cout_min:,}Ar - {self.cout_max:,}Ar".replace(',', ' '),
            'symptomes_requis': self.symptomes_requis,
            'symptomes_optionnels': self.symptomes_optionnels,
            'conseils': self.conseils
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crée un Diagnostic depuis un dictionnaire"""
        return cls(
            id=data['id'],
            nom=data['nom'],
            description=data['description'],
            gravite=data['gravite'],
            cout_min=data['cout_min'],
            cout_max=data['cout_max'],
            symptomes_requis=data['symptomes_requis'],
            symptomes_optionnels=data.get('symptomes_optionnels', []),
            conseils=data.get('conseils')
        )

"""Modèle pour représenter un symptôme"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Symptome:
    """Représente un symptôme automobile"""
    id: str
    nom: str
    description: Optional[str] = None
    categorie: Optional[str] = None
    poids: float = 1.0  # Importance du symptôme (0.0 à 1.0)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Symptome):
            return self.id == other.id
        return False
    
    def to_dict(self):
        """Convertit en dictionnaire"""
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'poids': self.poids
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crée un Symptome depuis un dictionnaire"""
        return cls(
            id=data['id'],
            nom=data['nom'],
            description=data.get('description'),
            categorie=data.get('categorie'),
            poids=data.get('poids', 1.0)
        )

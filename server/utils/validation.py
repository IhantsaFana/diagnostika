"""Validation des entrées utilisateur"""
from typing import Tuple, List, Optional
import config

def valider_requete_diagnostic(data: dict) -> Tuple[bool, Optional[str], Optional[List[str]]]:
    """
    Valide une requête de diagnostic
    
    Args:
        data: Données de la requête
        
    Returns:
        (valide, message_erreur, symptomes_ids)
    """
    if not isinstance(data, dict):
        return False, "Format de requête invalide", None
    
    symptomes = data.get('symptomes', [])
    
    if not isinstance(symptomes, list):
        return False, "Les symptômes doivent être une liste", None
    
    if len(symptomes) < config.MIN_SYMPTOMES_PAR_REQUETE:
        return False, f"Minimum {config.MIN_SYMPTOMES_PAR_REQUETE} symptôme requis", None
    
    if len(symptomes) > config.MAX_SYMPTOMES_PAR_REQUETE:
        return False, f"Maximum {config.MAX_SYMPTOMES_PAR_REQUETE} symptômes autorisés", None
    
    # Vérifier que ce sont des chaînes
    if not all(isinstance(s, str) for s in symptomes):
        return False, "Tous les symptômes doivent être des chaînes de caractères", None
    
    # Nettoyer les symptômes
    symptomes_clean = [s.strip() for s in symptomes if s.strip()]
    
    if not symptomes_clean:
        return False, "Aucun symptôme valide fourni", None
    
    return True, None, symptomes_clean

def valider_recherche(data: dict) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Valide une requête de recherche de symptômes
    
    Args:
        data: Données de la requête
        
    Returns:
        (valide, message_erreur, texte)
    """
    if not isinstance(data, dict):
        return False, "Format de requête invalide", None
    
    texte = data.get('texte', '')
    
    if not isinstance(texte, str):
        return False, "Le texte doit être une chaîne de caractères", None
    
    texte = texte.strip()
    
    if not texte:
        return False, "Le texte de recherche ne peut pas être vide", None
    
    if len(texte) < 3:
        return False, "Le texte doit contenir au moins 3 caractères", None
    
    if len(texte) > 200:
        return False, "Le texte est trop long (maximum 200 caractères)", None
    
    return True, None, texte

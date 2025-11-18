"""Tests de validation des entrées"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.validation import valider_requete_diagnostic, valider_recherche

def test_validation_diagnostic():
    """Test validation des requêtes de diagnostic"""
    print("\n=== Test Validation Diagnostic ===")
    
    # Test valide
    valide, erreur, symptomes = valider_requete_diagnostic({
        'symptomes': ['symptome1', 'symptome2']
    })
    assert valide == True
    assert erreur is None
    assert len(symptomes) == 2
    print("✓ Requête valide acceptée")
    
    # Test liste vide
    valide, erreur, _ = valider_requete_diagnostic({
        'symptomes': []
    })
    assert valide == False
    assert "Minimum" in erreur
    print("✓ Liste vide rejetée")
    
    # Test trop de symptômes
    valide, erreur, _ = valider_requete_diagnostic({
        'symptomes': ['s1', 's2', 's3', 's4', 's5', 's6']
    })
    assert valide == False
    assert "Maximum" in erreur
    print("✓ Trop de symptômes rejeté")
    
    # Test type invalide
    valide, erreur, _ = valider_requete_diagnostic({
        'symptomes': 'pas une liste'
    })
    assert valide == False
    assert "liste" in erreur
    print("✓ Type invalide rejeté")
    
    # Test symptômes non-string
    valide, erreur, _ = valider_requete_diagnostic({
        'symptomes': [123, 456]
    })
    assert valide == False
    assert "chaînes" in erreur
    print("✓ Non-string rejeté")
    
    # Test nettoyage espaces
    valide, erreur, symptomes = valider_requete_diagnostic({
        'symptomes': ['  symptome1  ', 'symptome2']
    })
    assert valide == True
    assert symptomes[0] == 'symptome1'
    print("✓ Nettoyage des espaces OK")

def test_validation_recherche():
    """Test validation des recherches"""
    print("\n=== Test Validation Recherche ===")
    
    # Test valide
    valide, erreur, texte = valider_recherche({
        'texte': 'le moteur fait du bruit'
    })
    assert valide == True
    assert erreur is None
    assert texte == 'le moteur fait du bruit'
    print("✓ Recherche valide acceptée")
    
    # Test texte vide
    valide, erreur, _ = valider_recherche({
        'texte': ''
    })
    assert valide == False
    assert "vide" in erreur
    print("✓ Texte vide rejeté")
    
    # Test texte trop court
    valide, erreur, _ = valider_recherche({
        'texte': 'ab'
    })
    assert valide == False
    assert "3 caractères" in erreur
    print("✓ Texte trop court rejeté")
    
    # Test texte trop long
    valide, erreur, _ = valider_recherche({
        'texte': 'a' * 201
    })
    assert valide == False
    assert "trop long" in erreur
    print("✓ Texte trop long rejeté")
    
    # Test type invalide
    valide, erreur, _ = valider_recherche({
        'texte': 123
    })
    assert valide == False
    assert "chaîne" in erreur
    print("✓ Type invalide rejeté")
    
    # Test nettoyage
    valide, erreur, texte = valider_recherche({
        'texte': '  test recherche  '
    })
    assert valide == True
    assert texte == 'test recherche'
    print("✓ Nettoyage du texte OK")

if __name__ == '__main__':
    print("=" * 50)
    print("TESTS DE VALIDATION")
    print("=" * 50)
    
    try:
        test_validation_diagnostic()
        test_validation_recherche()
        print("\n" + "=" * 50)
        print("✅ TOUS LES TESTS VALIDATION PASSÉS")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n❌ ÉCHEC: {e}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")

"""Tests des modèles de données"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Symptome, Diagnostic

def test_symptome_creation():
    """Test création d'un symptôme"""
    print("\n=== Test Symptome ===")
    
    symptome = Symptome(
        id="test_symptome",
        nom="Symptôme de test",
        description="Description test",
        categorie="Test",
        poids=0.8
    )
    
    assert symptome.id == "test_symptome"
    assert symptome.nom == "Symptôme de test"
    assert symptome.poids == 0.8
    print("✓ Création de symptôme OK")
    
    # Test conversion dict
    symptome_dict = symptome.to_dict()
    assert symptome_dict['id'] == "test_symptome"
    print("✓ Conversion to_dict OK")
    
    # Test from_dict
    symptome2 = Symptome.from_dict(symptome_dict)
    assert symptome2.id == symptome.id
    print("✓ Conversion from_dict OK")

def test_diagnostic_creation():
    """Test création d'un diagnostic"""
    print("\n=== Test Diagnostic ===")
    
    diagnostic = Diagnostic(
        id="test_diag",
        nom="Diagnostic test",
        description="Description test",
        gravite="Moyen",
        cout_min=10000,
        cout_max=50000,
        symptomes_requis=["symptome1", "symptome2"],
        symptomes_optionnels=["symptome3"],
        conseils="Conseils test"
    )
    
    assert diagnostic.id == "test_diag"
    assert diagnostic.gravite == "Moyen"
    assert len(diagnostic.symptomes_requis) == 2
    print("✓ Création de diagnostic OK")
    
    # Test conversion dict
    diag_dict = diagnostic.to_dict()
    assert "cout_estimatif" in diag_dict
    assert "10 000Ar" in diag_dict['cout_estimatif']
    print("✓ Conversion to_dict OK")
    
    # Test from_dict
    diagnostic2 = Diagnostic.from_dict({
        'id': 'test2',
        'nom': 'Test 2',
        'description': 'Desc',
        'gravite': 'Léger',
        'cout_min': 5000,
        'cout_max': 10000,
        'symptomes_requis': ['s1']
    })
    assert diagnostic2.id == "test2"
    assert len(diagnostic2.symptomes_optionnels) == 0
    print("✓ Conversion from_dict OK")

if __name__ == '__main__':
    print("=" * 50)
    print("TESTS DES MODÈLES")
    print("=" * 50)
    
    try:
        test_symptome_creation()
        test_diagnostic_creation()
        print("\n" + "=" * 50)
        print("✅ TOUS LES TESTS MODÈLES PASSÉS")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n❌ ÉCHEC: {e}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")

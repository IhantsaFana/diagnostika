"""Tests de l'API en direct (serveur doit être lancé)"""
import requests
import json

API_URL = "http://localhost:5000"

def test_api_disponible():
    """Test si l'API répond"""
    print("\n=== Test API Disponible ===")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        assert response.status_code == 200
        data = response.json()
        print(f"✓ API répond: {data.get('message')}")
        print(f"  Version: {data.get('version')}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ API non disponible. Lancez d'abord: python api.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_get_symptomes():
    """Test GET /symptomes"""
    print("\n=== Test GET /symptomes ===")
    try:
        response = requests.get(f"{API_URL}/symptomes")
        assert response.status_code == 200
        data = response.json()
        assert data['succes'] == True
        print(f"✓ {data['total']} symptômes récupérés")
        
        # Afficher quelques exemples
        for symptome in data['symptomes'][:3]:
            print(f"  - {symptome['nom']} (poids: {symptome['poids']})")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_recherche_symptomes():
    """Test POST /rechercher"""
    print("\n=== Test POST /rechercher ===")
    
    tests = [
        "le moteur fait du bruit",
        "fumée noire à l'échappement",
        "la voiture ne démarre pas",
        "problème de freins"
    ]
    
    try:
        for texte in tests:
            response = requests.post(
                f"{API_URL}/rechercher",
                json={"texte": texte},
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data['succes'] == True
            
            print(f"\n✓ Recherche: '{texte}'")
            print(f"  Résultats: {len(data['resultats'])}")
            if data['resultats']:
                meilleur = data['resultats'][0]
                print(f"  Meilleur: {meilleur['nom']} (score: {meilleur['score_similarite']:.3f})")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_diagnostic_exact():
    """Test POST /diagnostiquer avec correspondance exacte"""
    print("\n=== Test POST /diagnostiquer (exact) ===")
    
    tests = [
        {
            "symptomes": ["fumee_noire", "consommation_elevee"],
            "attendu": "Problème d'injection"
        },
        {
            "symptomes": ["moteur_chauffe", "fuite_liquide"],
            "attendu": "Radiateur défectueux"
        },
        {
            "symptomes": ["demarrage_difficile", "batterie_faible"],
            "attendu": "Panne de batterie"
        }
    ]
    
    try:
        for test in tests:
            response = requests.post(
                f"{API_URL}/diagnostiquer",
                json={"symptomes": test["symptomes"]},
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data['succes'] == True
            
            print(f"\n✓ Symptômes: {', '.join(test['symptomes'])}")
            print(f"  Diagnostic: {data['diagnostic']}")
            print(f"  Confiance: {data['confiance']} (score: {data['score']})")
            print(f"  Gravité: {data['gravite']}")
            print(f"  Coût: {data['cout_estimatif']}")
            
            if data['diagnostic'] == test['attendu']:
                print(f"  ✓ Correspond au diagnostic attendu")
            else:
                print(f"  ⚠️  Attendu: {test['attendu']}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_diagnostic_partiel():
    """Test diagnostic avec correspondance partielle"""
    print("\n=== Test Diagnostic Partiel ===")
    
    try:
        response = requests.post(
            f"{API_URL}/diagnostiquer",
            json={"symptomes": ["fumee_noire"]},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data['succes'] == True
        
        print(f"✓ Diagnostic avec 1 symptôme: {data['diagnostic']}")
        print(f"  Confiance: {data['confiance']} (score: {data['score']})")
        
        if 'suggestions' in data:
            print(f"  Suggestions ({len(data['suggestions'])}):")
            for suggestion in data['suggestions'][:3]:
                print(f"    - {suggestion}")
        
        if 'diagnostics_alternatifs' in data:
            print(f"  Diagnostics alternatifs:")
            for alt in data['diagnostics_alternatifs'][:2]:
                print(f"    - {alt['nom']} (score: {alt['score']})")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_validation_erreurs():
    """Test validation des erreurs"""
    print("\n=== Test Validation Erreurs ===")
    
    tests_erreurs = [
        {
            "data": {"symptomes": []},
            "description": "Liste vide"
        },
        {
            "data": {"symptomes": ["s1", "s2", "s3", "s4", "s5", "s6"]},
            "description": "Trop de symptômes"
        },
        {
            "data": {"symptomes": "pas une liste"},
            "description": "Type invalide"
        },
        {
            "data": {},
            "description": "Pas de champ symptomes"
        }
    ]
    
    try:
        for test in tests_erreurs:
            response = requests.post(
                f"{API_URL}/diagnostiquer",
                json=test["data"],
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 400
            data = response.json()
            assert data['succes'] == False
            print(f"✓ {test['description']}: Erreur correctement détectée")
            print(f"  Message: {data['erreur']}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Exécute tous les tests de l'API"""
    print("=" * 70)
    print("TESTS DE L'API EN DIRECT")
    print("=" * 70)
    print("\n⚠️  Le serveur doit être lancé sur http://localhost:5000")
    print("   Commande: python api.py\n")
    
    # Vérifier que l'API est disponible
    if not test_api_disponible():
        print("\n❌ Impossible de continuer sans API")
        return False
    
    # Exécuter les tests
    resultats = []
    resultats.append(("GET /symptomes", test_get_symptomes()))
    resultats.append(("POST /rechercher", test_recherche_symptomes()))
    resultats.append(("POST /diagnostiquer (exact)", test_diagnostic_exact()))
    resultats.append(("POST /diagnostiquer (partiel)", test_diagnostic_partiel()))
    resultats.append(("Validation erreurs", test_validation_erreurs()))
    
    # Résumé
    print("\n" + "=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    
    for nom, succes in resultats:
        statut = "✅" if succes else "❌"
        print(f"{statut} {nom}")
    
    total = len(resultats)
    passes = sum(1 for _, s in resultats if s)
    
    print(f"\nTotal: {passes}/{total} tests réussis")
    
    if passes == total:
        print("\n🎉 TOUS LES TESTS API ONT RÉUSSI ! 🎉")
        return True
    else:
        print(f"\n⚠️  {total - passes} test(s) ont échoué")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

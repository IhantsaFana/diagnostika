"""Tests d'intégration du système complet"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_initialisation_moteur():
    """Test initialisation du moteur de diagnostic"""
    print("\n=== Test Initialisation Moteur ===")
    
    from services import MoteurDiagnostic
    
    print("Initialisation du moteur...")
    moteur = MoteurDiagnostic()
    
    assert len(moteur.symptomes) > 0, "Aucun symptôme chargé"
    print(f"✓ {len(moteur.symptomes)} symptômes chargés")
    
    assert len(moteur.diagnostics) > 0, "Aucun diagnostic chargé"
    print(f"✓ {len(moteur.diagnostics)} diagnostics chargés")
    
    assert moteur.vectorisation is not None, "Service de vectorisation non initialisé"
    print(f"✓ Service de vectorisation initialisé")
    
    assert len(moteur.vectorisation.symptomes_vectors) > 0, "Aucun vecteur créé"
    print(f"✓ {len(moteur.vectorisation.symptomes_vectors)} vecteurs créés")
    
    return moteur

def test_get_symptomes(moteur):
    """Test récupération des symptômes"""
    print("\n=== Test Get Symptômes ===")
    
    symptomes = moteur.get_symptomes_disponibles()
    
    assert isinstance(symptomes, list), "Doit retourner une liste"
    assert len(symptomes) > 0, "Liste vide"
    print(f"✓ {len(symptomes)} symptômes disponibles")
    
    # Vérifier structure
    premier = symptomes[0]
    assert 'id' in premier
    assert 'nom' in premier
    assert 'poids' in premier
    print(f"✓ Structure correcte")
    
    return symptomes

def test_recherche_symptomes(moteur):
    """Test recherche de symptômes par texte"""
    print("\n=== Test Recherche Symptômes ===")
    
    # Test recherche simple
    resultats = moteur.rechercher_symptomes("le moteur fait du bruit", top_k=5)
    
    assert isinstance(resultats, list), "Doit retourner une liste"
    print(f"✓ Recherche 'bruit moteur': {len(resultats)} résultats")
    
    if resultats:
        premier = resultats[0]
        assert 'score_similarite' in premier
        assert 0 <= premier['score_similarite'] <= 1
        print(f"  Meilleur: {premier['nom']} (score: {premier['score_similarite']:.3f})")
    
    # Test recherche fumée
    resultats = moteur.rechercher_symptomes("fumée noire échappement", top_k=3)
    print(f"✓ Recherche 'fumée': {len(resultats)} résultats")
    if resultats:
        print(f"  Meilleur: {resultats[0]['nom']} (score: {resultats[0]['score_similarite']:.3f})")
    
    # Test recherche démarrage
    resultats = moteur.rechercher_symptomes("la voiture ne démarre pas", top_k=3)
    print(f"✓ Recherche 'démarrage': {len(resultats)} résultats")
    if resultats:
        print(f"  Meilleur: {resultats[0]['nom']} (score: {resultats[0]['score_similarite']:.3f})")

def test_diagnostic_exact(moteur):
    """Test diagnostic avec correspondance exacte"""
    print("\n=== Test Diagnostic Exact ===")
    
    # Test 1: Problème d'injection
    resultat = moteur.diagnostiquer(['fumee_noire', 'consommation_elevee'])
    
    assert resultat['succes'] == True
    assert resultat['diagnostic'] == "Problème d'injection"
    assert resultat['confiance'] in ['Haute', 'Moyenne']
    print(f"✓ Diagnostic: {resultat['diagnostic']}")
    print(f"  Confiance: {resultat['confiance']} (score: {resultat['score']})")
    print(f"  Gravité: {resultat['gravite']}")
    print(f"  Coût: {resultat['cout_estimatif']}")
    
    # Test 2: Radiateur défectueux
    resultat = moteur.diagnostiquer(['moteur_chauffe', 'fuite_liquide'])
    
    assert resultat['succes'] == True
    assert resultat['diagnostic'] == "Radiateur défectueux"
    assert resultat['gravite'] == "Critique"
    print(f"\n✓ Diagnostic: {resultat['diagnostic']}")
    print(f"  Confiance: {resultat['confiance']} (score: {resultat['score']})")
    
    # Test 3: Panne batterie
    resultat = moteur.diagnostiquer(['demarrage_difficile', 'batterie_faible'])
    
    assert resultat['succes'] == True
    assert resultat['diagnostic'] == "Panne de batterie"
    assert resultat['gravite'] == "Léger"
    print(f"\n✓ Diagnostic: {resultat['diagnostic']}")
    print(f"  Confiance: {resultat['confiance']} (score: {resultat['score']})")

def test_diagnostic_partiel(moteur):
    """Test diagnostic avec correspondance partielle"""
    print("\n=== Test Diagnostic Partiel ===")
    
    # Un seul symptôme d'une règle
    resultat = moteur.diagnostiquer(['fumee_noire'])
    
    assert resultat['succes'] == True
    print(f"✓ Diagnostic avec 1 symptôme: {resultat['diagnostic']}")
    print(f"  Confiance: {resultat['confiance']} (score: {resultat['score']})")
    
    if 'suggestions' in resultat:
        print(f"  Suggestions: {len(resultat['suggestions'])}")
        for suggestion in resultat['suggestions'][:2]:
            print(f"    - {suggestion}")

def test_diagnostic_avec_optionnels(moteur):
    """Test diagnostic avec symptômes optionnels"""
    print("\n=== Test Diagnostic avec Optionnels ===")
    
    # Symptômes requis + optionnels
    resultat = moteur.diagnostiquer([
        'fumee_noire', 
        'consommation_elevee', 
        'perte_puissance'  # optionnel
    ])
    
    assert resultat['succes'] == True
    print(f"✓ Diagnostic avec optionnels: {resultat['diagnostic']}")
    print(f"  Confiance: {resultat['confiance']} (score: {resultat['score']})")
    print(f"  Symptômes utilisés: {len(resultat['symptomes_utilises'])}")

def test_diagnostic_incertain(moteur):
    """Test diagnostic incertain"""
    print("\n=== Test Diagnostic Incertain ===")
    
    # Symptômes qui ne correspondent à aucune règle
    resultat = moteur.diagnostiquer(['climatisation_inefficace'])
    
    assert resultat['succes'] == True
    print(f"✓ Diagnostic: {resultat['diagnostic']}")
    print(f"  Confiance: {resultat['confiance']}")
    
    if 'suggestions' in resultat:
        print(f"  Suggestions: {len(resultat['suggestions'])}")

def test_diagnostics_alternatifs(moteur):
    """Test diagnostics alternatifs"""
    print("\n=== Test Diagnostics Alternatifs ===")
    
    # Symptômes ambigus
    resultat = moteur.diagnostiquer(['demarrage_difficile', 'ralenti_irregulier'])
    
    assert resultat['succes'] == True
    print(f"✓ Diagnostic principal: {resultat['diagnostic']}")
    
    if 'diagnostics_alternatifs' in resultat:
        print(f"  Diagnostics alternatifs: {len(resultat['diagnostics_alternatifs'])}")
        for alt in resultat['diagnostics_alternatifs']:
            print(f"    - {alt['nom']} (score: {alt['score']})")

def test_validation_limites(moteur):
    """Test validation des limites"""
    print("\n=== Test Validation Limites ===")
    
    # Trop de symptômes
    symptomes_trop = ['fumee_noire'] * 10
    resultat = moteur.diagnostiquer(symptomes_trop)
    # Le moteur accepte mais déduplique
    assert resultat['succes'] == True
    print(f"✓ Gestion des doublons OK")
    
    # Symptômes invalides
    resultat = moteur.diagnostiquer(['symptome_inexistant'])
    assert resultat['succes'] == True  # Retourne diagnostic incertain
    print(f"✓ Gestion symptômes invalides OK")
    
    # Liste vide gérée par validation API
    resultat = moteur.diagnostiquer([])
    assert resultat['succes'] == False
    print(f"✓ Liste vide rejetée OK")

if __name__ == '__main__':
    print("=" * 60)
    print("TESTS D'INTÉGRATION DU SYSTÈME")
    print("=" * 60)
    
    try:
        # Initialisation
        moteur = test_initialisation_moteur()
        
        # Tests fonctionnels
        symptomes = test_get_symptomes(moteur)
        test_recherche_symptomes(moteur)
        test_diagnostic_exact(moteur)
        test_diagnostic_partiel(moteur)
        test_diagnostic_avec_optionnels(moteur)
        test_diagnostic_incertain(moteur)
        test_diagnostics_alternatifs(moteur)
        test_validation_limites(moteur)
        
        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS D'INTÉGRATION PASSÉS")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ ÉCHEC: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

"""Tests de chargement des données JSON"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config

def test_chargement_symptomes():
    """Test chargement du fichier symptomes.json"""
    print("\n=== Test Chargement Symptômes ===")
    
    # Vérifier que le fichier existe
    assert os.path.exists(config.SYMPTOMES_FILE), "Fichier symptomes.json introuvable"
    print(f"✓ Fichier trouvé: {config.SYMPTOMES_FILE}")
    
    # Charger et parser
    with open(config.SYMPTOMES_FILE, 'r', encoding='utf-8') as f:
        symptomes = json.load(f)
    
    assert isinstance(symptomes, list), "symptomes.json doit être une liste"
    print(f"✓ Format JSON valide")
    
    assert len(symptomes) > 0, "Aucun symptôme trouvé"
    print(f"✓ {len(symptomes)} symptômes chargés")
    
    # Vérifier la structure du premier symptôme
    premier = symptomes[0]
    champs_requis = ['id', 'nom', 'description', 'categorie', 'poids']
    for champ in champs_requis:
        assert champ in premier, f"Champ '{champ}' manquant"
    print(f"✓ Structure valide")
    
    # Vérifier les types
    assert isinstance(premier['id'], str)
    assert isinstance(premier['nom'], str)
    assert isinstance(premier['poids'], (int, float))
    assert 0 <= premier['poids'] <= 1
    print(f"✓ Types de données corrects")
    
    # Vérifier unicité des IDs
    ids = [s['id'] for s in symptomes]
    assert len(ids) == len(set(ids)), "IDs de symptômes en double"
    print(f"✓ IDs uniques")
    
    # Afficher quelques exemples
    print(f"\nExemples de symptômes:")
    for s in symptomes[:3]:
        print(f"  - {s['id']}: {s['nom']} (poids: {s['poids']})")

def test_chargement_regles():
    """Test chargement du fichier regles.json"""
    print("\n=== Test Chargement Règles ===")
    
    # Vérifier que le fichier existe
    assert os.path.exists(config.REGLES_FILE), "Fichier regles.json introuvable"
    print(f"✓ Fichier trouvé: {config.REGLES_FILE}")
    
    # Charger et parser
    with open(config.REGLES_FILE, 'r', encoding='utf-8') as f:
        regles = json.load(f)
    
    assert isinstance(regles, list), "regles.json doit être une liste"
    print(f"✓ Format JSON valide")
    
    assert len(regles) > 0, "Aucune règle trouvée"
    print(f"✓ {len(regles)} règles chargées")
    
    # Vérifier la structure de la première règle
    premiere = regles[0]
    champs_requis = ['id', 'nom', 'description', 'gravite', 'cout_min', 'cout_max', 'symptomes_requis']
    for champ in champs_requis:
        assert champ in premiere, f"Champ '{champ}' manquant"
    print(f"✓ Structure valide")
    
    # Vérifier les types
    assert isinstance(premiere['id'], str)
    assert isinstance(premiere['nom'], str)
    assert isinstance(premiere['gravite'], str)
    assert isinstance(premiere['cout_min'], int)
    assert isinstance(premiere['cout_max'], int)
    assert isinstance(premiere['symptomes_requis'], list)
    assert premiere['cout_min'] < premiere['cout_max']
    print(f"✓ Types de données corrects")
    
    # Vérifier gravités valides
    gravites_valides = ['Léger', 'Moyen', 'Critique']
    for regle in regles:
        assert regle['gravite'] in gravites_valides, f"Gravité invalide: {regle['gravite']}"
    print(f"✓ Gravités valides")
    
    # Vérifier unicité des IDs
    ids = [r['id'] for r in regles]
    assert len(ids) == len(set(ids)), "IDs de règles en double"
    print(f"✓ IDs uniques")
    
    # Afficher quelques exemples
    print(f"\nExemples de règles:")
    for r in regles[:3]:
        print(f"  - {r['id']}: {r['nom']} ({r['gravite']})")
        print(f"    Symptômes requis: {len(r['symptomes_requis'])}")

def test_coherence_donnees():
    """Test cohérence entre symptômes et règles"""
    print("\n=== Test Cohérence Données ===")
    
    # Charger les données
    with open(config.SYMPTOMES_FILE, 'r', encoding='utf-8') as f:
        symptomes = json.load(f)
    
    with open(config.REGLES_FILE, 'r', encoding='utf-8') as f:
        regles = json.load(f)
    
    # Créer un set des IDs de symptômes
    symptomes_ids = {s['id'] for s in symptomes}
    
    # Vérifier que tous les symptômes des règles existent
    erreurs = []
    for regle in regles:
        for symptome_id in regle['symptomes_requis']:
            if symptome_id not in symptomes_ids:
                erreurs.append(f"Règle '{regle['id']}': symptôme '{symptome_id}' introuvable")
        
        for symptome_id in regle.get('symptomes_optionnels', []):
            if symptome_id not in symptomes_ids:
                erreurs.append(f"Règle '{regle['id']}': symptôme optionnel '{symptome_id}' introuvable")
    
    if erreurs:
        print("❌ Erreurs de cohérence:")
        for err in erreurs:
            print(f"  - {err}")
        raise AssertionError("Incohérences détectées")
    
    print(f"✓ Tous les symptômes référencés existent")
    
    # Statistiques
    symptomes_utilises = set()
    for regle in regles:
        symptomes_utilises.update(regle['symptomes_requis'])
        symptomes_utilises.update(regle.get('symptomes_optionnels', []))
    
    print(f"✓ {len(symptomes_utilises)}/{len(symptomes_ids)} symptômes utilisés dans les règles")
    
    # Symptômes non utilisés
    non_utilises = symptomes_ids - symptomes_utilises
    if non_utilises:
        print(f"\nℹ️  Symptômes non utilisés ({len(non_utilises)}):")
        for sid in list(non_utilises)[:5]:
            symptome = next(s for s in symptomes if s['id'] == sid)
            print(f"  - {sid}: {symptome['nom']}")
        if len(non_utilises) > 5:
            print(f"  ... et {len(non_utilises) - 5} autres")

if __name__ == '__main__':
    print("=" * 50)
    print("TESTS DE CHARGEMENT DES DONNÉES")
    print("=" * 50)
    
    try:
        test_chargement_symptomes()
        test_chargement_regles()
        test_coherence_donnees()
        print("\n" + "=" * 50)
        print("✅ TOUS LES TESTS DONNÉES PASSÉS")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n❌ ÉCHEC: {e}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

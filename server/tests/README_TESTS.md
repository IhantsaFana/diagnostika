# 🧪 Guide des Tests

## Structure des Tests

```
tests/
├── test_models.py              # Tests des modèles Symptome et Diagnostic
├── test_validation.py          # Tests de validation des entrées
├── test_chargement_donnees.py  # Tests de chargement JSON
├── test_integration.py         # Tests d'intégration complets
└── run_all_tests.py           # Script pour tout exécuter
```

## Exécution des Tests

### Option 1 : Tous les tests (recommandé)
```bash
cd server
python tests/run_all_tests.py
```

### Option 2 : Tests individuels

#### Tests unitaires (sans dépendances lourdes)
```bash
# Tests des modèles
python tests/test_models.py

# Tests de validation
python tests/test_validation.py

# Tests de chargement des données
python tests/test_chargement_donnees.py
```

#### Tests d'intégration (nécessitent numpy, sklearn, sentence-transformers)
```bash
python tests/test_integration.py
```

## Description des Tests

### 1. test_models.py
**Ce qui est testé :**
- Création d'objets Symptome et Diagnostic
- Conversion to_dict() et from_dict()
- Validation des types de données
- Formatage des coûts

**Dépendances :** Aucune (tests purs)

### 2. test_validation.py
**Ce qui est testé :**
- Validation des requêtes de diagnostic
- Validation des recherches de texte
- Gestion des erreurs (liste vide, trop de symptômes, types invalides)
- Nettoyage des entrées (espaces, etc.)

**Dépendances :** Aucune (tests purs)

### 3. test_chargement_donnees.py
**Ce qui est testé :**
- Chargement des fichiers JSON (symptomes.json, regles.json)
- Validation de la structure des données
- Vérification des types
- Cohérence entre symptômes et règles
- Détection des symptômes non utilisés

**Dépendances :** Fichiers JSON dans data/

### 4. test_integration.py
**Ce qui est testé :**
- Initialisation complète du moteur
- Vectorisation des symptômes
- Recherche par texte libre
- Diagnostic avec correspondance exacte
- Diagnostic avec correspondance partielle
- Diagnostic avec symptômes optionnels
- Diagnostics alternatifs
- Gestion des cas incertains
- Validation des limites

**Dépendances :** numpy, scikit-learn, sentence-transformers

## Résultats Attendus

### Tests Unitaires
```
=== Test Symptome ===
✓ Création de symptôme OK
✓ Conversion to_dict OK
✓ Conversion from_dict OK

=== Test Diagnostic ===
✓ Création de diagnostic OK
✓ Conversion to_dict OK
✓ Conversion from_dict OK

✅ TOUS LES TESTS MODÈLES PASSÉS
```

### Tests de Validation
```
=== Test Validation Diagnostic ===
✓ Requête valide acceptée
✓ Liste vide rejetée
✓ Trop de symptômes rejeté
✓ Type invalide rejeté
✓ Non-string rejeté
✓ Nettoyage des espaces OK

✅ TOUS LES TESTS VALIDATION PASSÉS
```

### Tests de Chargement
```
=== Test Chargement Symptômes ===
✓ Fichier trouvé
✓ Format JSON valide
✓ 50 symptômes chargés
✓ Structure valide
✓ Types de données corrects
✓ IDs uniques

=== Test Chargement Règles ===
✓ 16 règles chargées
✓ Structure valide
✓ Gravités valides

✅ TOUS LES TESTS DONNÉES PASSÉS
```

### Tests d'Intégration
```
=== Test Initialisation Moteur ===
✓ 50 symptômes chargés
✓ 16 diagnostics chargés
✓ Service de vectorisation initialisé
✓ 50 vecteurs créés

=== Test Recherche Symptômes ===
✓ Recherche 'bruit moteur': 5 résultats
  Meilleur: Bruit anormal du moteur (score: 0.876)

=== Test Diagnostic Exact ===
✓ Diagnostic: Problème d'injection
  Confiance: Haute (score: 0.95)
  Gravité: Moyen
  Coût: 30 000Ar - 80 000Ar

✅ TOUS LES TESTS D'INTÉGRATION PASSÉS
```

## Dépannage

### Erreur : Module not found
```bash
# Assurez-vous d'être dans le bon dossier
cd server

# Vérifiez que les dépendances sont installées
pip list | grep -E "numpy|scikit|sentence"
```

### Erreur : Fichier JSON introuvable
```bash
# Vérifiez que les fichiers existent
ls data/symptomes.json
ls data/regles.json
```

### Erreur : Modèle d'embeddings non trouvé
```bash
# Le premier lancement télécharge le modèle (peut prendre 1-2 minutes)
# Assurez-vous d'avoir une connexion internet
```

## Ajout de Nouveaux Tests

### Template de test
```python
def test_nouvelle_fonctionnalite():
    """Description du test"""
    print("\n=== Test Nouvelle Fonctionnalité ===")
    
    # Arrange (préparation)
    donnees = {...}
    
    # Act (action)
    resultat = fonction_a_tester(donnees)
    
    # Assert (vérification)
    assert resultat == valeur_attendue
    print("✓ Test réussi")
```

## Couverture des Tests

### Actuellement testé ✅
- Modèles de données
- Validation des entrées
- Chargement des données
- Vectorisation
- Recherche sémantique
- Moteur de diagnostic
- Scoring et confiance
- Diagnostics alternatifs

### À ajouter (optionnel) 📝
- Tests de performance
- Tests de charge (stress tests)
- Tests de l'API Flask (endpoints)
- Tests de l'intégration Gemini
- Tests de sécurité

## Commandes Utiles

```bash
# Exécuter tous les tests avec sortie détaillée
python tests/run_all_tests.py

# Exécuter un test spécifique
python tests/test_models.py

# Vérifier la syntaxe Python
python -m py_compile tests/*.py

# Compter les tests
grep -r "def test_" tests/ | wc -l
```

## Interprétation des Résultats

- ✅ **Test passé** : Tout fonctionne comme prévu
- ❌ **Test échoué** : Un problème a été détecté, vérifier le message d'erreur
- ⏭️ **Test ignoré** : Test non exécuté (dépendances manquantes)

## Support

En cas de problème avec les tests :
1. Vérifiez que toutes les dépendances sont installées
2. Vérifiez que vous êtes dans le bon dossier (server/)
3. Lisez attentivement le message d'erreur
4. Consultez les logs détaillés

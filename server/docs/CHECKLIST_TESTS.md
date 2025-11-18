# ✅ Checklist de Tests

## Avant de lancer les tests

- [ ] Environnement virtuel activé (`venv\Scripts\activate`)
- [ ] Dépendances installées (`pip install numpy scikit-learn sentence-transformers Flask flask-cors python-dotenv`)
- [ ] Dans le dossier `server/`

---

## Phase 1 : Tests Unitaires (5 min)

### Tests des Modèles
```bash
python tests/test_models.py
```
- [ ] Création de Symptome OK
- [ ] Conversion to_dict/from_dict OK
- [ ] Création de Diagnostic OK
- [ ] Formatage des coûts OK

### Tests de Validation
```bash
python tests/test_validation.py
```
- [ ] Requête valide acceptée
- [ ] Liste vide rejetée
- [ ] Trop de symptômes rejeté
- [ ] Types invalides rejetés
- [ ] Nettoyage des espaces OK

### Tests de Chargement
```bash
python tests/test_chargement_donnees.py
```
- [ ] 50 symptômes chargés
- [ ] 16 règles chargées
- [ ] Structure JSON valide
- [ ] Cohérence des données OK
- [ ] IDs uniques

---

## Phase 2 : Tests d'Intégration (1-2 min)

```bash
python tests/test_integration.py
```

### Initialisation
- [ ] Moteur initialisé
- [ ] Symptômes chargés
- [ ] Diagnostics chargés
- [ ] Vecteurs créés

### Recherche Sémantique
- [ ] Recherche "bruit moteur" fonctionne
- [ ] Recherche "fumée" fonctionne
- [ ] Recherche "démarrage" fonctionne
- [ ] Scores de similarité corrects

### Diagnostic Exact
- [ ] Problème d'injection détecté
- [ ] Radiateur défectueux détecté
- [ ] Panne batterie détectée
- [ ] Confiance haute (≥ 0.85)

### Diagnostic Partiel
- [ ] 1 symptôme → diagnostic probable
- [ ] Confiance moyenne/faible
- [ ] Suggestions générées

### Fonctionnalités Avancées
- [ ] Symptômes optionnels pris en compte
- [ ] Diagnostics alternatifs proposés
- [ ] Cas incertain géré
- [ ] Validation des limites OK

---

## Phase 3 : Tests API (1 min)

**Prérequis : Serveur lancé** (`python api.py`)

```bash
python tests/test_api_live.py
```

### Endpoints de Base
- [ ] GET / répond
- [ ] GET /symptomes répond
- [ ] 50 symptômes retournés

### Recherche
- [ ] POST /rechercher fonctionne
- [ ] Résultats avec scores
- [ ] Format JSON correct

### Diagnostic
- [ ] POST /diagnostiquer fonctionne
- [ ] Diagnostic exact OK
- [ ] Diagnostic partiel OK
- [ ] Format JSON correct

### Validation
- [ ] Liste vide → erreur 400
- [ ] Trop de symptômes → erreur 400
- [ ] Type invalide → erreur 400
- [ ] Messages d'erreur clairs

---

## Tests Manuels (optionnel)

### Avec curl
```bash
# Test 1
curl http://localhost:5000/symptomes

# Test 2
curl -X POST http://localhost:5000/rechercher \
  -H "Content-Type: application/json" \
  -d "{\"texte\": \"le moteur fait du bruit\"}"

# Test 3
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"fumee_noire\", \"consommation_elevee\"]}"
```

- [ ] Toutes les requêtes répondent
- [ ] Format JSON valide
- [ ] Données cohérentes

---

## Résultats Attendus

### ✅ Tous les tests passent
```
✅ Tests Modèles : 6/6
✅ Tests Validation : 12/12
✅ Tests Données : 8/8
✅ Tests Intégration : 15/15
✅ Tests API : 20/20
---
Total : 61/61 ✅
```

### ❌ Si des tests échouent

1. **Lire le message d'erreur**
2. **Vérifier les prérequis**
   - Dépendances installées ?
   - Fichiers JSON présents ?
   - Serveur lancé (pour tests API) ?
3. **Consulter les logs**
4. **Relancer le test spécifique**

---

## Commandes Rapides

```bash
# Tout en une fois
python tests/run_all_tests.py

# Tests unitaires seulement
python tests/test_models.py && \
python tests/test_validation.py && \
python tests/test_chargement_donnees.py

# Tests d'intégration
python tests/test_integration.py

# Tests API (serveur doit tourner)
python tests/test_api_live.py
```

---

## Temps Estimés

| Phase | Temps | Prérequis |
|-------|-------|-----------|
| Tests unitaires | 5 sec | Aucun |
| Tests intégration | 30-60 sec | Bibliothèques |
| Tests API | 10 sec | Serveur lancé |
| **Total** | **~1-2 min** | |

---

## Dépannage Rapide

### "Module not found"
```bash
pip install numpy scikit-learn sentence-transformers
```

### "API non disponible"
```bash
# Terminal 1
python api.py

# Terminal 2
python tests/test_api_live.py
```

### "Fichier JSON introuvable"
```bash
# Vérifier
ls data/symptomes.json
ls data/regles.json
```

### Téléchargement lent
```
# Normal au 1er lancement (modèle ~90MB)
# Patience : 1-2 minutes
```

---

## ✅ Validation Finale

Avant de considérer le système prêt :

- [ ] Tous les tests unitaires passent
- [ ] Tous les tests d'intégration passent
- [ ] Tous les tests API passent
- [ ] Aucune erreur dans les logs
- [ ] Performance acceptable (< 2 sec par diagnostic)
- [ ] Mémoire stable (pas de fuite)

---

## 🎉 Système Validé !

Si tous les tests passent, votre système est prêt pour :
- ✅ Développement du frontend
- ✅ Tests utilisateurs
- ✅ Démonstration
- ✅ Déploiement (après tests supplémentaires)

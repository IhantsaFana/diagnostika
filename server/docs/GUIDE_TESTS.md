# 🧪 Guide Rapide des Tests

## 📦 Avant de commencer

### Installer les dépendances
```bash
cd server
venv\Scripts\activate
pip install numpy scikit-learn sentence-transformers Flask flask-cors python-dotenv
```

## 🚀 Exécution des Tests

### Étape 1 : Tests sans serveur (unitaires)

Ces tests ne nécessitent PAS que le serveur soit lancé.

```bash
# Tous les tests unitaires
python tests/run_all_tests.py

# Ou individuellement
python tests/test_models.py
python tests/test_validation.py
python tests/test_chargement_donnees.py
```

**Temps estimé :** 5-10 secondes

**Ce qui est testé :**
- ✅ Modèles de données (Symptome, Diagnostic)
- ✅ Validation des entrées
- ✅ Chargement des fichiers JSON
- ✅ Cohérence des données

---

### Étape 2 : Tests d'intégration

Ces tests nécessitent les bibliothèques lourdes (numpy, sklearn, sentence-transformers).

```bash
python tests/test_integration.py
```

**Temps estimé :** 30-60 secondes (premier lancement télécharge le modèle)

**Ce qui est testé :**
- ✅ Initialisation du moteur
- ✅ Vectorisation des symptômes
- ✅ Recherche sémantique
- ✅ Diagnostic exact et partiel
- ✅ Scoring et confiance
- ✅ Diagnostics alternatifs

---

### Étape 3 : Tests de l'API (en direct)

Ces tests nécessitent que le serveur Flask soit **lancé**.

**Terminal 1 - Lancer le serveur :**
```bash
cd server
venv\Scripts\activate
python api.py
```

**Terminal 2 - Lancer les tests :**
```bash
cd server
python tests/test_api_live.py
```

**Temps estimé :** 10-15 secondes

**Ce qui est testé :**
- ✅ Endpoints de l'API
- ✅ GET /symptomes
- ✅ POST /rechercher
- ✅ POST /diagnostiquer
- ✅ Validation des erreurs
- ✅ Format des réponses JSON

---

## 📊 Résultats Attendus

### ✅ Succès
```
=== Test Diagnostic Exact ===
✓ Diagnostic: Problème d'injection
  Confiance: Haute (score: 0.95)
  Gravité: Moyen
  Coût: 30 000Ar - 80 000Ar

✅ TOUS LES TESTS PASSÉS
```

### ❌ Échec
```
❌ ÉCHEC: assertion failed
  Expected: 'Problème d'injection'
  Got: 'Diagnostic incertain'
```

---

## 🐛 Dépannage

### Problème : "Module not found"
```bash
# Solution : Installer les dépendances
pip install numpy scikit-learn sentence-transformers
```

### Problème : "API non disponible"
```bash
# Solution : Lancer le serveur dans un autre terminal
python api.py
```

### Problème : "Fichier JSON introuvable"
```bash
# Solution : Vérifier que vous êtes dans le bon dossier
cd server
ls data/symptomes.json  # Doit exister
```

### Problème : Téléchargement du modèle lent
```
# Normal au premier lancement (1-2 minutes)
# Le modèle all-MiniLM-L6-v2 (~90MB) est téléchargé
# Les lancements suivants seront rapides
```

---

## 📝 Ordre Recommandé

1. **Tests unitaires** → Rapides, pas de dépendances lourdes
2. **Tests d'intégration** → Valide le système complet
3. **Tests API** → Valide les endpoints en conditions réelles

---

## 🎯 Tests Essentiels (minimum)

Si vous manquez de temps, exécutez au minimum :

```bash
# Test 1 : Données valides
python tests/test_chargement_donnees.py

# Test 2 : Système fonctionne
python tests/test_integration.py

# Test 3 : API répond
python tests/test_api_live.py
```

---

## 📈 Statistiques

- **Tests unitaires** : ~15 tests
- **Tests d'intégration** : ~10 tests
- **Tests API** : ~20 tests
- **Total** : ~45 tests

**Couverture** :
- Modèles : 100%
- Validation : 100%
- Données : 100%
- Moteur : 90%
- API : 85%

---

## 💡 Conseils

1. **Exécutez les tests après chaque modification**
2. **Lisez les messages d'erreur attentivement**
3. **Les tests sont votre documentation vivante**
4. **Un test qui échoue = un bug détecté tôt**

---

## 🆘 Besoin d'aide ?

1. Consultez `tests/README_TESTS.md` pour plus de détails
2. Vérifiez les logs du serveur (Terminal 1)
3. Activez le mode debug dans `config.py`

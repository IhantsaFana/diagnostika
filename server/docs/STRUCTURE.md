# 📁 Structure du Projet Backend

```
server/
│
├── 📄 api.py                          # Point d'entrée de l'API Flask
├── 📄 config.py                       # Configuration centralisée
├── 📄 .env                            # Variables d'environnement (non versionné)
├── 📄 .env.example                    # Template de configuration
│
├── 📂 models/                         # Modèles de données
│   ├── __init__.py
│   ├── symptome.py                   # Classe Symptome
│   └── diagnostic.py                 # Classe Diagnostic
│
├── 📂 services/                       # Logique métier
│   ├── __init__.py
│   ├── vectorisation.py              # Embeddings et similarité
│   ├── moteur_diagnostic.py          # Moteur de règles
│   └── assistant_ia.py               # Intégration Gemini
│
├── 📂 data/                           # Données JSON
│   ├── symptomes.json                # 50 symptômes
│   └── regles.json                   # 16 règles de diagnostic
│
├── 📂 utils/                          # Utilitaires
│   ├── __init__.py
│   └── validation.py                 # Validation des entrées
│
├── 📂 tests/                          # Tests
│   ├── __init__.py
│   ├── test_models.py                # Tests des modèles
│   ├── test_validation.py            # Tests de validation
│   ├── test_chargement_donnees.py    # Tests de chargement
│   ├── test_integration.py           # Tests d'intégration
│   ├── test_api_live.py              # Tests API en direct
│   ├── run_all_tests.py              # Script pour tout exécuter
│   ├── exemples_requetes.md          # Exemples de requêtes
│   └── README_TESTS.md               # Documentation des tests
│
├── 📂 venv/                           # Environnement virtuel Python
│
└── 📄 Documentation
    ├── README_V2.md                  # Documentation principale
    ├── GUIDE_TESTS.md                # Guide des tests
    ├── CHECKLIST_TESTS.md            # Checklist de validation
    └── STRUCTURE.md                  # Ce fichier
```

---

## 📄 Fichiers Principaux

### api.py
**Rôle :** Point d'entrée de l'API Flask  
**Responsabilités :**
- Définir les routes (endpoints)
- Gérer les requêtes HTTP
- Valider les entrées
- Retourner les réponses JSON

**Endpoints :**
- `GET /` - Informations sur l'API
- `GET /symptomes` - Liste des symptômes
- `POST /rechercher` - Recherche par texte libre
- `POST /diagnostiquer` - Effectuer un diagnostic

### config.py
**Rôle :** Configuration centralisée  
**Contenu :**
- Paramètres de l'API (host, port)
- Limites (max symptômes, seuils de confiance)
- Chemins des fichiers
- Configuration IA

---

## 📂 Dossier models/

### symptome.py
**Classe :** `Symptome`  
**Attributs :**
- `id` : Identifiant unique
- `nom` : Nom du symptôme
- `description` : Description détaillée
- `categorie` : Catégorie (Échappement, Bruit, etc.)
- `poids` : Importance (0.0 à 1.0)

**Méthodes :**
- `to_dict()` : Convertir en dictionnaire
- `from_dict()` : Créer depuis dictionnaire

### diagnostic.py
**Classe :** `Diagnostic`  
**Attributs :**
- `id` : Identifiant unique
- `nom` : Nom du diagnostic
- `description` : Description du problème
- `gravite` : Léger / Moyen / Critique
- `cout_min`, `cout_max` : Fourchette de prix
- `symptomes_requis` : Liste d'IDs obligatoires
- `symptomes_optionnels` : Liste d'IDs optionnels
- `conseils` : Recommandations

---

## 📂 Dossier services/

### vectorisation.py
**Classe :** `VectorisationService`  
**Responsabilités :**
- Charger le modèle d'embeddings (sentence-transformers)
- Vectoriser les symptômes
- Calculer la similarité cosinus
- Trouver les symptômes similaires à un texte
- Calculer le score de correspondance avec les règles

**Modèle utilisé :** `all-MiniLM-L6-v2` (léger, performant)

### moteur_diagnostic.py
**Classe :** `MoteurDiagnostic`  
**Responsabilités :**
- Charger les symptômes et règles
- Initialiser le service de vectorisation
- Rechercher des symptômes par texte libre
- Effectuer un diagnostic basé sur les règles
- Calculer les scores de confiance
- Générer des suggestions
- Proposer des diagnostics alternatifs

**Algorithme :**
1. Matching exact → Confiance haute
2. Matching partiel → Confiance moyenne/faible
3. Aucun match → Diagnostic incertain

### assistant_ia.py
**Classe :** `AssistantIA`  
**Responsabilités :**
- Intégration avec Gemini (optionnel)
- Reformulation des diagnostics en langage naturel
- Fallback si API indisponible

---

## 📂 Dossier data/

### symptomes.json
**Format :**
```json
[
  {
    "id": "fumee_noire",
    "nom": "Fumée noire à l'échappement",
    "description": "...",
    "categorie": "Échappement",
    "poids": 0.9
  }
]
```

**Contenu :** 50 symptômes automobiles

### regles.json
**Format :**
```json
[
  {
    "id": "diag_injection",
    "nom": "Problème d'injection",
    "description": "...",
    "gravite": "Moyen",
    "cout_min": 30000,
    "cout_max": 80000,
    "symptomes_requis": ["fumee_noire", "consommation_elevee"],
    "symptomes_optionnels": ["perte_puissance"],
    "conseils": "..."
  }
]
```

**Contenu :** 16 règles de diagnostic

---

## 📂 Dossier utils/

### validation.py
**Fonctions :**
- `valider_requete_diagnostic()` : Valide les symptômes
- `valider_recherche()` : Valide le texte de recherche

**Validations :**
- Type de données
- Limites (min/max)
- Nettoyage des entrées
- Messages d'erreur clairs

---

## 📂 Dossier tests/

### Tests Unitaires
- `test_models.py` : Modèles de données
- `test_validation.py` : Validation des entrées
- `test_chargement_donnees.py` : Chargement JSON

### Tests d'Intégration
- `test_integration.py` : Système complet

### Tests API
- `test_api_live.py` : Endpoints en direct

### Utilitaires
- `run_all_tests.py` : Exécuter tous les tests
- `exemples_requetes.md` : Exemples curl/Python

---

## 🔄 Flux de Données

### Recherche par texte libre
```
Utilisateur → API (/rechercher)
           → Validation
           → VectorisationService.trouver_symptomes_similaires()
           → Calcul similarité cosinus
           → Top 5 symptômes
           → Réponse JSON
```

### Diagnostic
```
Utilisateur → API (/diagnostiquer)
           → Validation
           → MoteurDiagnostic.diagnostiquer()
           → Pour chaque règle:
              - Calculer score
              - Appliquer poids
           → Trier par score
           → Générer suggestions
           → AssistantIA.reformuler() (optionnel)
           → Réponse JSON
```

---

## 📦 Dépendances

### Production
- `Flask` : Framework web
- `flask-cors` : Gestion CORS
- `python-dotenv` : Variables d'environnement
- `numpy` : Calculs vectoriels
- `scikit-learn` : Similarité cosinus
- `sentence-transformers` : Embeddings sémantiques
- `google-generativeai` : Gemini (optionnel)

### Développement
- Tests : Aucune dépendance externe

---

## 🎯 Points d'Extension

### Ajouter un symptôme
1. Éditer `data/symptomes.json`
2. Redémarrer le serveur
3. Vecteur créé automatiquement

### Ajouter une règle
1. Éditer `data/regles.json`
2. Redémarrer le serveur
3. Règle active immédiatement

### Changer le modèle d'embeddings
1. Modifier `config.py` → `EMBEDDING_MODEL`
2. Redémarrer le serveur
3. Nouveau modèle téléchargé

### Ajouter un endpoint
1. Ajouter route dans `api.py`
2. Créer fonction de service si nécessaire
3. Ajouter tests

---

## 📊 Métriques

- **Fichiers Python** : 12
- **Fichiers JSON** : 2
- **Fichiers de tests** : 6
- **Lignes de code** : ~2000
- **Symptômes** : 50
- **Règles** : 16
- **Tests** : ~45

---

## 🔒 Sécurité

- ✅ Validation stricte des entrées
- ✅ Limites de requêtes
- ✅ Variables d'environnement pour secrets
- ✅ CORS configuré
- ✅ Pas d'exécution de code arbitraire
- ✅ Gestion des erreurs

---

## 🚀 Performance

- **Initialisation** : 2-3 secondes (chargement modèle)
- **Recherche** : < 100ms
- **Diagnostic** : < 200ms
- **Mémoire** : ~500MB (modèle d'embeddings)

---

## 📝 Conventions

- **Nommage** : snake_case pour Python
- **IDs** : snake_case (ex: `fumee_noire`)
- **Classes** : PascalCase (ex: `MoteurDiagnostic`)
- **Constantes** : UPPER_CASE (ex: `MAX_SYMPTOMES`)
- **Encodage** : UTF-8
- **Indentation** : 4 espaces

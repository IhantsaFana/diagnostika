# 🚀 Système Expert de Diagnostic Automobile v2.0

## Architecture avec Vectorisation

### 📁 Structure

```
server/
├── api.py                      # API Flask
├── config.py                   # Configuration centralisée
├── models/                     # Modèles de données
│   ├── symptome.py            # Classe Symptome
│   └── diagnostic.py          # Classe Diagnostic
├── services/                   # Logique métier
│   ├── vectorisation.py       # Embeddings et similarité
│   ├── moteur_diagnostic.py   # Moteur de règles
│   └── assistant_ia.py        # Intégration Gemini
├── data/                       # Données
│   ├── symptomes.json         # 50 symptômes
│   └── regles.json            # 16 règles de diagnostic
└── utils/                      # Utilitaires
    └── validation.py          # Validation des entrées
```

### 🎯 Fonctionnalités

#### 1. Sélection par cases à cocher (50 symptômes)
- Base de 50 symptômes catégorisés
- Maximum 5 symptômes par diagnostic
- Chaque symptôme a un poids d'importance

#### 2. Recherche par texte libre
- L'utilisateur tape : "le moteur fait du bruit"
- Le système trouve les symptômes similaires via embeddings
- Retourne les 5 symptômes les plus pertinents avec score

#### 3. Diagnostic intelligent
- **Matching exact** : Tous les symptômes requis présents → Confiance haute
- **Matching partiel** : Symptômes partiels → Confiance moyenne/faible
- **Score pondéré** : Prise en compte du poids de chaque symptôme
- **Suggestions** : Propose des symptômes à vérifier

#### 4. Reformulation IA (optionnel)
- Gemini reformule le diagnostic en langage naturel
- Uniquement pour diagnostics avec confiance haute/moyenne

### 🔧 Technologies

- **sentence-transformers** : Embeddings sémantiques (all-MiniLM-L6-v2)
- **scikit-learn** : Calcul de similarité cosinus
- **numpy** : Opérations vectorielles
- **Flask** : API REST

### 📊 Endpoints

#### GET /symptomes
Retourne tous les symptômes disponibles
```json
{
  "succes": true,
  "total": 50,
  "symptomes": [...]
}
```

#### POST /rechercher
Recherche de symptômes par texte libre
```json
// Requête
{
  "texte": "le moteur fait du bruit"
}

// Réponse
{
  "succes": true,
  "resultats": [
    {
      "id": "bruit_anormal",
      "nom": "Bruit anormal du moteur",
      "score_similarite": 0.87
    }
  ]
}
```

#### POST /diagnostiquer
Effectue un diagnostic
```json
// Requête
{
  "symptomes": ["fumee_noire", "consommation_elevee"]
}

// Réponse
{
  "succes": true,
  "diagnostic": "Problème d'injection",
  "description": "...",
  "gravite": "Moyen",
  "cout_estimatif": "30 000Ar - 80 000Ar",
  "confiance": "Haute",
  "score": 0.95,
  "conseils": "...",
  "explication_ia": "...",
  "symptomes_utilises": [...],
  "suggestions": [...],
  "diagnostics_alternatifs": [...]
}
```

### 🎓 Algorithme de Scoring

```python
Score = (Symptômes requis présents / Total requis) * Poids

Si tous requis présents:
    Score_base = 0.8
    Bonus_optionnels = (Optionnels présents / Total optionnels) * 0.2
    Score_final = (Score_base + Bonus) * Facteur_poids
```

### 🔍 Niveaux de Confiance

- **Haute** (≥ 85%) : Diagnostic très probable
- **Moyenne** (≥ 60%) : Diagnostic probable avec suggestions
- **Faible** (≥ 40%) : Diagnostic possible, inspection recommandée
- **Très faible** (< 40%) : Diagnostic incertain

### 🚀 Démarrage

```bash
# Installer les dépendances
pip install numpy scikit-learn sentence-transformers Flask flask-cors python-dotenv

# Lancer le serveur
python api.py
```

### 📈 Évolutivité

- ✅ Ajout facile de nouveaux symptômes (JSON)
- ✅ Ajout facile de nouvelles règles (JSON)
- ✅ Pas de modification du code nécessaire
- ✅ Système de scoring automatique
- ✅ Support texte libre via embeddings

### 💡 Avantages de l'approche vectorielle

1. **Flexibilité** : Gère texte libre ET sélection
2. **Scalabilité** : Fonctionne avec 10 ou 1000 symptômes
3. **Intelligence** : Trouve des correspondances sémantiques
4. **Robustesse** : Gère les cas partiels et imprécis
5. **Maintenabilité** : Code modulaire et extensible

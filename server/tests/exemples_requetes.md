# 📡 Exemples de Requêtes API

## Utilisation avec curl ou Postman

### 1. Vérifier que l'API fonctionne

```bash
curl http://localhost:5000/
```

**Réponse attendue :**
```json
{
  "message": "API de diagnostic automobile",
  "version": "2.0",
  "endpoints": {...}
}
```

---

### 2. Récupérer tous les symptômes

```bash
curl http://localhost:5000/symptomes
```

**Réponse attendue :**
```json
{
  "succes": true,
  "total": 50,
  "symptomes": [
    {
      "id": "fumee_noire",
      "nom": "Fumée noire à l'échappement",
      "description": "...",
      "categorie": "Échappement",
      "poids": 0.9
    },
    ...
  ]
}
```

---

### 3. Rechercher des symptômes par texte libre

```bash
curl -X POST http://localhost:5000/rechercher \
  -H "Content-Type: application/json" \
  -d "{\"texte\": \"le moteur fait du bruit\"}"
```

**Réponse attendue :**
```json
{
  "succes": true,
  "texte_recherche": "le moteur fait du bruit",
  "resultats": [
    {
      "id": "bruit_anormal",
      "nom": "Bruit anormal du moteur",
      "score_similarite": 0.876,
      "categorie": "Bruit",
      "poids": 0.6
    },
    ...
  ]
}
```

**Autres exemples de recherche :**
```bash
# Fumée
curl -X POST http://localhost:5000/rechercher \
  -H "Content-Type: application/json" \
  -d "{\"texte\": \"fumée noire échappement\"}"

# Démarrage
curl -X POST http://localhost:5000/rechercher \
  -H "Content-Type: application/json" \
  -d "{\"texte\": \"la voiture ne démarre pas\"}"

# Surchauffe
curl -X POST http://localhost:5000/rechercher \
  -H "Content-Type: application/json" \
  -d "{\"texte\": \"moteur qui chauffe trop\"}"
```

---

### 4. Diagnostiquer avec symptômes exacts

#### Exemple 1 : Problème d'injection
```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"fumee_noire\", \"consommation_elevee\"]}"
```

**Réponse attendue :**
```json
{
  "succes": true,
  "diagnostic": "Problème d'injection",
  "description": "Dysfonctionnement du système d'injection de carburant",
  "gravite": "Moyen",
  "cout_estimatif": "30 000Ar - 80 000Ar",
  "conseils": "Faire vérifier les injecteurs et le système d'injection",
  "confiance": "Haute",
  "score": 0.95,
  "symptomes_utilises": [
    "Fumée noire à l'échappement",
    "Consommation de carburant élevée"
  ],
  "explication_ia": "..." (si Gemini activé)
}
```

#### Exemple 2 : Radiateur défectueux
```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"moteur_chauffe\", \"fuite_liquide\"]}"
```

**Réponse attendue :**
```json
{
  "succes": true,
  "diagnostic": "Radiateur défectueux",
  "gravite": "Critique",
  "cout_estimatif": "25 000Ar - 60 000Ar",
  "confiance": "Haute",
  "score": 0.92
}
```

#### Exemple 3 : Panne batterie
```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"demarrage_difficile\", \"batterie_faible\"]}"
```

**Réponse attendue :**
```json
{
  "succes": true,
  "diagnostic": "Panne de batterie",
  "gravite": "Léger",
  "cout_estimatif": "12 000Ar - 25 000Ar",
  "confiance": "Haute",
  "score": 0.88
}
```

---

### 5. Diagnostic avec correspondance partielle

```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"fumee_noire\"]}"
```

**Réponse attendue :**
```json
{
  "succes": true,
  "diagnostic": "Problème d'injection",
  "confiance": "Moyenne",
  "score": 0.65,
  "suggestions": [
    "Vérifiez si présent : Consommation de carburant élevée",
    "Symptôme associé possible : Perte de puissance"
  ],
  "diagnostics_alternatifs": [
    {
      "nom": "Filtre à air encrassé",
      "score": 0.52
    }
  ]
}
```

---

### 6. Diagnostic avec symptômes optionnels

```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"fumee_noire\", \"consommation_elevee\", \"perte_puissance\"]}"
```

**Réponse attendue :**
```json
{
  "succes": true,
  "diagnostic": "Problème d'injection",
  "confiance": "Haute",
  "score": 0.98,
  "symptomes_utilises": [
    "Fumée noire à l'échappement",
    "Consommation de carburant élevée",
    "Perte de puissance"
  ]
}
```

---

### 7. Cas d'erreur : Liste vide

```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": []}"
```

**Réponse attendue (400 Bad Request) :**
```json
{
  "succes": false,
  "erreur": "Minimum 1 symptôme requis"
}
```

---

### 8. Cas d'erreur : Trop de symptômes

```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": [\"s1\", \"s2\", \"s3\", \"s4\", \"s5\", \"s6\"]}"
```

**Réponse attendue (400 Bad Request) :**
```json
{
  "succes": false,
  "erreur": "Maximum 5 symptômes autorisés"
}
```

---

### 9. Cas d'erreur : Type invalide

```bash
curl -X POST http://localhost:5000/diagnostiquer \
  -H "Content-Type: application/json" \
  -d "{\"symptomes\": \"pas une liste\"}"
```

**Réponse attendue (400 Bad Request) :**
```json
{
  "succes": false,
  "erreur": "Les symptômes doivent être une liste"
}
```

---

## 🧪 Tests avec Python (requests)

```python
import requests

# Recherche
response = requests.post(
    'http://localhost:5000/rechercher',
    json={'texte': 'le moteur fait du bruit'}
)
print(response.json())

# Diagnostic
response = requests.post(
    'http://localhost:5000/diagnostiquer',
    json={'symptomes': ['fumee_noire', 'consommation_elevee']}
)
print(response.json())
```

---

## 🎯 Scénarios de Test Complets

### Scénario 1 : Utilisateur décrit un problème
1. Recherche : "fumée noire et consomme beaucoup"
2. Sélection des symptômes trouvés
3. Diagnostic → Problème d'injection

### Scénario 2 : Utilisateur sélectionne directement
1. Sélection : moteur_chauffe, fuite_liquide
2. Diagnostic → Radiateur défectueux (Critique)

### Scénario 3 : Symptômes incomplets
1. Sélection : fumee_noire
2. Diagnostic → Confiance moyenne + suggestions

### Scénario 4 : Symptômes ambigus
1. Sélection : demarrage_difficile, ralenti_irregulier
2. Diagnostic → Plusieurs possibilités avec scores

---

## 📝 Notes

- Tous les IDs de symptômes sont en snake_case (ex: `fumee_noire`)
- Les coûts sont en Ariary (Ar)
- Les scores de confiance vont de 0 à 1
- Les gravités possibles : Léger, Moyen, Critique

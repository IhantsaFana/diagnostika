# 🔧 Assistant Intelligent de Diagnostic Automobile

Mini-système expert pour aider les mécaniciens à identifier les pannes automobiles à partir des symptômes observés.

## 📋 Contexte du projet

Un garage souhaite disposer d'un outil local permettant d'aider les mécaniciens à identifier la cause probable d'une panne à partir des symptômes observés sur un véhicule. L'application combine une logique métier basée sur des règles conditionnelles et une aide IA textuelle pour expliquer les causes probables.

## ✨ Fonctionnalités

- ✅ Sélection des symptômes via cases à cocher
- ✅ Application de règles de diagnostic :
  - **Fumée noire + Consommation élevée** → Problème d'injection
  - **Moteur chauffe + Fuite liquide** → Radiateur défectueux
  - **Démarrage difficile + Batterie faible** → Panne batterie
- ✅ Affichage du diagnostic avec gravité (Léger/Moyen/Critique) et coût estimatif
- ✅ Génération d'explication IA via Gemini (avec fallback en mode simulation)
- ✅ Validation robuste des entrées
- ✅ Interface responsive et moderne

## 🏗️ Architecture

```
diagnostika/
├── server/              # Backend Flask (Python)
│   ├── api.py          # API REST principale
│   ├── moteur_diagnostic.py  # Moteur de règles
│   ├── assistant_ia.py # Intégration Gemini
│   ├── regles.json     # Base de règles de diagnostic
│   ├── .env            # Configuration (clé API)
│   └── venv/           # Environnement virtuel Python
│
└── client/             # Frontend React + TypeScript
    ├── src/
    │   ├── App.tsx     # Composant principal
    │   ├── App.css     # Styles
    │   └── main.tsx    # Point d'entrée
    └── package.json
```

## 🚀 Installation et démarrage

### Prérequis
- Python 3.8+
- Node.js 16+ et Yarn
- Clé API Gemini (optionnel)

### 1. Backend Flask

```cmd
cd server
python -m venv venv
venv\Scripts\activate
pip install Flask flask-cors python-dotenv google-generativeai
```

Configurez votre clé API (optionnel) :
```cmd
copy .env.example .env
```
Éditez `.env` et ajoutez votre clé Gemini.

Démarrez le serveur :
```cmd
python api.py
```
Le backend sera accessible sur http://localhost:5000

### 2. Frontend React

```cmd
cd client
yarn install
yarn dev
```
Le frontend sera accessible sur http://localhost:5173

## 🧪 Test de l'application

1. Ouvrez http://localhost:5173 dans votre navigateur
2. Sélectionnez des symptômes :
   - "fumée noire" + "consommation élevée"
   - "moteur chauffe" + "fuite liquide"
   - "démarrage difficile" + "batterie faible"
3. Cliquez sur "Diagnostiquer"
4. Consultez le résultat avec l'explication IA

## 🔒 Sécurité

- ✅ Variables d'environnement pour les clés API
- ✅ Validation stricte des entrées (type, longueur, liste blanche)
- ✅ Gestion d'erreurs complète
- ✅ Protection CORS configurée
- ✅ Limite de requêtes (max 10 symptômes)

## 📊 Règles de diagnostic

| Symptômes | Diagnostic | Gravité | Coût estimatif |
|-----------|-----------|---------|----------------|
| Fumée noire + Consommation élevée | Problème d'injection | Moyen | 300Ar - 800Ar |
| Moteur chauffe + Fuite liquide | Radiateur défectueux | Critique | 250Ar - 600Ar |
| Démarrage difficile + Batterie faible | Panne batterie | Léger | 120Ar - 250Ar |

## 🛠️ Technologies utilisées

**Backend :**
- Flask (API REST)
- Python-dotenv (gestion des variables d'environnement)
- Google Generative AI (Gemini)
- Flask-CORS

**Frontend :**
- React 19
- TypeScript
- Vite
- CSS moderne (responsive, dark/light mode)

## 📝 API Endpoints

### `GET /`
Vérification du serveur

### `GET /symptomes`
Retourne la liste des symptômes valides
```json
{
  "symptomes": ["fumée noire", "consommation élevée", ...]
}
```

### `POST /diagnostiquer`
Effectue un diagnostic
```json
// Requête
{
  "symptomes": ["fumée noire", "consommation élevée"]
}

// Réponse
{
  "diagnostic": "Problème d'injection",
  "gravite": "Moyen",
  "cout_estimatif": "300Ar - 800Ar",
  "explication_ia": "Un problème d'injection se manifeste..."
}
```

## 🎯 Améliorations implémentées

1. **Sécurité de la clé API** : Utilisation de python-dotenv
2. **Validation robuste** : Vérification type, longueur, liste blanche
3. **Intégration IA réelle** : Gemini avec fallback automatique
4. **Chemin absolu** : Résolution du problème de chargement de regles.json
5. **Interface moderne** : Design responsive avec mode sombre/clair

## 📚 Documentation

- `server/SECURITE.md` - Guide de sécurité
- `server/AMELIORATIONS.md` - Détails des améliorations
- `client/README_FRONTEND.md` - Documentation frontend

## 👨‍💻 Auteur

Projet développé dans le cadre d'un exercice de système expert automobile.

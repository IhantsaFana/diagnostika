from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Charge les variables d'environnement depuis .env
load_dotenv()

# On importe nos modules personnalisés
import moteur_diagnostic
import assistant_ia

# Initialise l'application Flask
app = Flask(__name__)

# Configure CORS pour autoriser les requêtes de votre frontend Vite
# (Mettez '*' pour tester, ou l'URL de Vite, ex: 'http://localhost:5173')
CORS(app)

# Configuration
MAX_SYMPTOMES = 10  # Limite le nombre de symptômes par requête
# Symptômes valides selon le cahier des charges
SYMPTOMES_VALIDES = [
    "fumée noire", 
    "consommation élevée", 
    "moteur chauffe", 
    "fuite liquide", 
    "démarrage difficile", 
    "batterie faible"
]

@app.route("/")
def index():
    """Juste pour vérifier que le serveur fonctionne."""
    return "Bonjour ! Le serveur de diagnostic est en ligne."

def valider_symptomes(symptomes):
    """
    Valide les symptômes reçus du frontend.
    Retourne (True, symptomes_valides) ou (False, message_erreur)
    """
    # Vérifier que c'est bien une liste
    if not isinstance(symptomes, list):
        return False, "Les symptômes doivent être fournis sous forme de liste"
    
    # Vérifier qu'il y a au moins un symptôme
    if len(symptomes) == 0:
        return False, "Aucun symptôme fourni"
    
    # Vérifier la limite de symptômes
    if len(symptomes) > MAX_SYMPTOMES:
        return False, f"Trop de symptômes (maximum: {MAX_SYMPTOMES})"
    
    # Vérifier que tous les symptômes sont des chaînes de caractères
    if not all(isinstance(s, str) for s in symptomes):
        return False, "Tous les symptômes doivent être du texte"
    
    # Nettoyer et normaliser les symptômes
    symptomes_nettoyes = []
    for symptome in symptomes:
        # Enlever les espaces superflus et mettre en minuscules
        symptome_clean = symptome.strip().lower()
        
        # Vérifier la longueur
        if len(symptome_clean) == 0:
            continue
        if len(symptome_clean) > 100:
            return False, "Un symptôme est trop long (maximum: 100 caractères)"
        
        # Vérifier que le symptôme est dans la liste valide
        if symptome_clean not in SYMPTOMES_VALIDES:
            return False, f"Symptôme non reconnu: '{symptome_clean}'"
        
        symptomes_nettoyes.append(symptome_clean)
    
    if len(symptomes_nettoyes) == 0:
        return False, "Aucun symptôme valide fourni"
    
    return True, symptomes_nettoyes

@app.route("/diagnostiquer", methods=["POST"])
def diagnostiquer():
    """
    Le point d'entrée principal de l'API.
    Prend une liste de symptômes en JSON et retourne un diagnostic.
    """
    try:
        # 1. Vérifier que la requête contient du JSON
        if not request.is_json:
            return jsonify({"erreur": "La requête doit être au format JSON"}), 400
        
        # 2. Recevoir les symptômes du frontend (ex: {"symptomes": ["fumée noire"]})
        data = request.json
        symptomes_utilisateur = data.get('symptomes', [])
        
        # 3. Valider les symptômes
        valide, resultat_validation = valider_symptomes(symptomes_utilisateur)
        if not valide:
            return jsonify({"erreur": resultat_validation}), 400
        
        symptomes_utilisateur = resultat_validation
        print(f"[API] Requête reçue avec symptômes : {symptomes_utilisateur}")

        # 4. Utiliser notre moteur de règles
        resultat = moteur_diagnostic.analyser_symptomes(symptomes_utilisateur)

        # 5. Gérer les cas selon le type de diagnostic
        if resultat["diagnostic"] == "Diagnostic incertain":
            # CAS 1: Aucune règle ne correspond → Demander à l'IA de diagnostiquer
            print("[API] Aucune règle trouvée. Appel de l'IA pour diagnostic complet...")
            resultat = assistant_ia.diagnostiquer_avec_ia(symptomes_utilisateur)
        
        elif resultat["diagnostic"] != "Erreur de configuration":
            # CAS 2: Règle trouvée → L'IA explique seulement
            print("[API] Diagnostic trouvé par règle. Appel de l'IA pour explication...")
            explication_ia = assistant_ia.generer_explication(
                resultat["diagnostic"], 
                symptomes_utilisateur
            )
            resultat['explication_ia'] = explication_ia
        
        # CAS 3: Erreur de configuration → Pas d'appel IA

        # 7. Renvoyer le tout au frontend en JSON
        print(f"[API] Réponse envoyée : {resultat['diagnostic']}")
        return jsonify(resultat)
    
    except Exception as e:
        print(f"[API] ERREUR INATTENDUE : {e}")
        # En production, ne pas exposer les détails de l'erreur
        if os.getenv('FLASK_ENV') == 'production':
            return jsonify({"erreur": "Erreur interne du serveur"}), 500
        else:
            return jsonify({"erreur": f"Erreur interne du serveur : {str(e)}"}), 500

@app.route("/symptomes", methods=["GET"])
def liste_symptomes():
    """
    Retourne la liste des symptômes valides.
    Utile pour le frontend (autocomplete, suggestions, etc.)
    """
    return jsonify({"symptomes": sorted(SYMPTOMES_VALIDES)})

# Point d'entrée pour lancer le serveur
if __name__ == "__main__":
    print("Démarrage du serveur de diagnostic Flask...")
    # 'debug=True' permet au serveur de se recharger si vous modifiez le code
    app.run(port=5000, debug=True)
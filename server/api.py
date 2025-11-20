"""API Flask principale"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from services import MoteurDiagnostic, AssistantIA
from utils import valider_requete_diagnostic, valider_recherche

# Initialisation
app = Flask(__name__)
CORS(app)

# Services
print("Initialisation des services...")
moteur = MoteurDiagnostic()
assistant_ia = AssistantIA()
print("Services prêts !")

@app.route('/')
def index():
    """Point d'entrée de l'API"""
    return jsonify({
        'message': 'API de diagnostic automobile',
        'version': '2.0',
        'endpoints': {
            'GET /symptomes': 'Liste tous les symptômes disponibles',
            'POST /rechercher': 'Recherche de symptômes par texte libre',
            'POST /diagnostiquer': 'Effectue un diagnostic'
        }
    })

@app.route('/symptomes', methods=['GET'])
def get_symptomes():
    """Retourne la liste de tous les symptômes disponibles"""
    try:
        symptomes = moteur.get_symptomes_disponibles()
        return jsonify({
            'succes': True,
            'total': len(symptomes),
            'symptomes': symptomes
        })
    except Exception as e:
        return jsonify({
            'succes': False,
            'erreur': f"Erreur serveur: {str(e)}"
        }), 500

@app.route('/rechercher', methods=['POST'])
def rechercher_symptomes():
    """
    Recherche des symptômes similaires à partir d'un texte libre
    
    Body: {"texte": "le moteur fait du bruit"}
    """
    try:
        data = request.get_json()
        
        # Validation
        valide, erreur, texte = valider_recherche(data)
        if not valide:
            return jsonify({
                'succes': False,
                'erreur': erreur
            }), 400

        # Sécuriser le typage pour l'analyse statique
        assert isinstance(texte, str)
        
        # Recherche
        resultats = moteur.rechercher_symptomes(texte, top_k=5)
        
        return jsonify({
            'succes': True,
            'texte_recherche': texte,
            'resultats': resultats
        })
        
    except Exception as e:
        return jsonify({
            'succes': False,
            'erreur': f"Erreur serveur: {str(e)}"
        }), 500

@app.route('/diagnostiquer', methods=['POST'])
def diagnostiquer():
    """
    Effectue un diagnostic basé sur les symptômes fournis
    
    Body: {"symptomes": ["fumee_noire", "consommation_elevee"]}
    """
    try:
        data = request.get_json()
        
        # Validation
        valide, erreur, symptomes_ids = valider_requete_diagnostic(data)
        if not valide:
            return jsonify({
                'succes': False,
                'erreur': erreur
            }), 400

        # Sécuriser le typage pour l'analyse statique
        assert isinstance(symptomes_ids, list)
        
        print(f"[API] Diagnostic demandé pour: {symptomes_ids}")
        
        # Diagnostic
        resultat = moteur.diagnostiquer(symptomes_ids)
        
        if not resultat.get('succes'):
            return jsonify(resultat), 400
        
        # Reformulation IA - toujours activer pour plus de clarté
        if assistant_ia.actif:
            explication_ia = assistant_ia.reformuler_diagnostic(resultat)
            resultat['explication_ia'] = explication_ia
        
        print(f"[API] Diagnostic: {resultat.get('diagnostic')} (confiance: {resultat.get('confiance')})")
        
        return jsonify(resultat)
        
    except Exception as e:
        print(f"[API] Erreur: {e}")
        return jsonify({
            'succes': False,
            'erreur': f"Erreur serveur: {str(e)}"
        }), 500

if __name__ == '__main__':
    print(f"Démarrage du serveur sur {config.API_HOST}:{config.API_PORT}")
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.DEBUG_MODE
    )

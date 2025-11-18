import json
import os

# Obtenir le chemin absolu du fichier de règles
# (dans le même dossier que ce script)
DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CHEMIN_REGLES = os.path.join(DOSSIER_SCRIPT, 'regles.json')

def charger_regles():
    """Charge les règles depuis le fichier JSON."""
    try:
        with open(CHEMIN_REGLES, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERREUR: Fichier de règles '{CHEMIN_REGLES}' non trouvé.")
        return []
    except json.JSONDecodeError:
        print(f"ERREUR: Fichier de règles '{CHEMIN_REGLES}' mal formaté.")
        return []

def analyser_symptomes(symptomes_utilisateur):
    """
    Analyse une liste de symptômes et retourne le premier diagnostic correspondant.
    """
    regles = charger_regles()
    # Convertit les symptômes de l'utilisateur en 'set' pour une recherche efficace
    symptomes_set = set(symptomes_utilisateur)
    
    if not regles:
        return {
            "diagnostic": "Erreur de configuration",
            "gravite": "Inconnue",
            "cout_estimatif": "N/A",
            "erreur": "Impossible de charger les règles de diagnostic."
        }

    for regle in regles:
        # 'issubset' vérifie si tous les symptômes requis sont présents
        if set(regle["symptomes_requis"]).issubset(symptomes_set):
            # On a un match ! On retourne le diagnostic
            # On copie la règle pour éviter de modifier l'original
            resultat = regle.copy()
            resultat.pop('symptomes_requis', None) # Pas besoin de renvoyer ça
            return resultat
    
    # Aucun match trouvé après avoir testé toutes les règles
    return {
        "diagnostic": "Diagnostic incertain",
        "gravite": "Inconnue",
        "cout_estimatif": "N/A",
        "detail": "Les symptômes fournis ne correspondent à aucun problème connu."
    }
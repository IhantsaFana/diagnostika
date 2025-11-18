import os
from dotenv import load_dotenv
import re

# Charge les variables d'environnement
load_dotenv()

def diagnostiquer_avec_ia(symptomes):
    """
    Utilise l'IA pour diagnostiquer un problème automobile quand aucune règle ne correspond.
    Retourne un diagnostic complet avec gravité, coût et explication.
    """
    print(f"[Assistant IA] Diagnostic IA pour symptômes non couverts : {symptomes}")
    
    # Vérifier si la clé API Gemini est configurée
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == '':
        print("[Assistant IA] Aucune clé API, diagnostic par défaut")
        return generer_diagnostic_par_defaut(symptomes)
    
    try:
        import google.generativeai as genai
        
        # Configuration de l'API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Créer le prompt structuré
        prompt = f"""Tu es un expert mécanicien automobile. Analyse ces symptômes et fournis un diagnostic.

Symptômes observés : {', '.join(symptomes)}

Réponds EXACTEMENT dans ce format (respecte les lignes) :
DIAGNOSTIC: [nom du problème en 3-5 mots]
GRAVITE: [Léger OU Moyen OU Critique]
COUT: [estimation en Ariary, format: XX XXXAr - XXX XXXAr]
EXPLICATION: [2-3 phrases expliquant le problème de manière simple]

Exemple de réponse :
DIAGNOSTIC: Problème de courroie de distribution
GRAVITE: Critique
COUT: 40 000Ar - 120 000Ar
EXPLICATION: La courroie de distribution relie le vilebrequin à l'arbre à cames. Si elle est usée, le moteur peut avoir des ratés ou ne pas démarrer. Un remplacement urgent est nécessaire pour éviter des dommages moteur graves."""
        
        # Appel à l'API
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.3,  # Plus déterministe
                'max_output_tokens': 300,
            }
        )
        
        texte = response.text.strip()
        print(f"[Assistant IA] Réponse brute Gemini reçue")
        
        # Parser la réponse
        diagnostic_parsed = parser_reponse_ia(texte)
        
        if diagnostic_parsed:
            print(f"[Assistant IA] Diagnostic IA généré : {diagnostic_parsed['diagnostic']}")
            return diagnostic_parsed
        else:
            print("[Assistant IA] Erreur de parsing, diagnostic par défaut")
            return generer_diagnostic_par_defaut(symptomes)
        
    except ImportError:
        print("[Assistant IA] Module google-generativeai non installé")
        return generer_diagnostic_par_defaut(symptomes)
    
    except Exception as e:
        print(f"[Assistant IA] Erreur lors de l'appel à Gemini: {e}")
        return generer_diagnostic_par_defaut(symptomes)

def parser_reponse_ia(texte):
    """
    Parse la réponse structurée de l'IA.
    """
    try:
        # Extraire les champs avec regex
        diagnostic_match = re.search(r'DIAGNOSTIC:\s*(.+)', texte, re.IGNORECASE)
        gravite_match = re.search(r'GRAVITE:\s*(.+)', texte, re.IGNORECASE)
        cout_match = re.search(r'COUT:\s*(.+)', texte, re.IGNORECASE)
        explication_match = re.search(r'EXPLICATION:\s*(.+)', texte, re.IGNORECASE | re.DOTALL)
        
        if diagnostic_match and gravite_match and cout_match and explication_match:
            return {
                "diagnostic": diagnostic_match.group(1).strip(),
                "gravite": gravite_match.group(1).strip(),
                "cout_estimatif": cout_match.group(1).strip(),
                "explication_ia": explication_match.group(1).strip()
            }
        return None
    except Exception as e:
        print(f"[Assistant IA] Erreur de parsing: {e}")
        return None

def generer_diagnostic_par_defaut(symptomes):
    """
    Génère un diagnostic par défaut quand l'IA n'est pas disponible.
    """
    return {
        "diagnostic": "Diagnostic nécessitant inspection",
        "gravite": "Moyen",
        "cout_estimatif": "200Ar - 800Ar",
        "explication_ia": f"Les symptômes observés ({', '.join(symptomes)}) ne correspondent pas aux pannes courantes de notre base de données. Une inspection approfondie par un mécanicien est recommandée pour identifier précisément le problème. Il pourrait s'agir d'une combinaison de plusieurs défaillances ou d'un problème moins fréquent."
    }

def generer_explication(diagnostic, symptomes):
    """
    Appelle une API IA pour obtenir une explication textuelle.
    Utilise Gemini si la clé API est configurée, sinon retourne une réponse simulée.
    """
    print(f"[Assistant IA] Demande d'explication pour : {diagnostic}")
    
    # Vérifier si la clé API Gemini est configurée
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == '':
        print("[Assistant IA] Aucune clé API configurée, mode simulation")
        return generer_explication_simulee(diagnostic, symptomes)
    
    # Tenter d'utiliser l'API Gemini
    try:
        import google.generativeai as genai
        
        # Configuration de l'API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Créer le prompt
        prompt = f"""Tu es un expert en mécanique automobile. Explique de manière simple et concise ce problème :

Diagnostic : {diagnostic}
Symptômes observés : {', '.join(symptomes)}

Fournis une explication en 2-3 phrases maximum, accessible à un non-expert."""
        
        # Appel à l'API avec timeout
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 200,
            }
        )
        
        explication = response.text.strip()
        print(f"[Assistant IA] Réponse Gemini générée avec succès")
        return explication
        
    except ImportError:
        print("[Assistant IA] Module google-generativeai non installé, mode simulation")
        return generer_explication_simulee(diagnostic, symptomes)
    
    except Exception as e:
        print(f"[Assistant IA] Erreur lors de l'appel à Gemini: {e}")
        return generer_explication_simulee(diagnostic, symptomes)

def generer_explication_simulee(diagnostic, symptomes):
    """
    Génère une explication simulée en cas d'indisponibilité de l'API.
    Basé sur les 3 diagnostics principaux du cahier des charges.
    """
    explications = {
        "Problème d'injection": "Un problème d'injection se manifeste par une combustion incomplète du carburant. Cela entraîne une surconsommation et des émissions de fumée noire. Une révision du système d'injection est nécessaire.",
        "Radiateur défectueux": "Un radiateur défectueux ne peut plus refroidir correctement le moteur. Les fuites de liquide de refroidissement aggravent le problème. Il faut remplacer le radiateur rapidement pour éviter une surchauffe moteur.",
        "Panne batterie": "Une batterie faible ou défectueuse ne fournit plus assez d'énergie pour démarrer le moteur. C'est un problème courant et généralement facile à résoudre. Un remplacement de batterie suffit souvent."
    }
    
    explication = explications.get(
        diagnostic,
        f"Le diagnostic '{diagnostic}' nécessite une inspection approfondie. Les symptômes observés ({', '.join(symptomes)}) indiquent un problème qui doit être examiné par un professionnel."
    )
    
    return explication
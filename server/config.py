"""Configuration centralisée de l'application"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG_MODE = os.getenv('FLASK_ENV', 'development') == 'development'

# Limites
MAX_SYMPTOMES_PAR_REQUETE = 5
MIN_SYMPTOMES_PAR_REQUETE = 1

# Seuils de confiance
SEUIL_CONFIANCE_HAUTE = 0.85  # Match quasi-parfait
SEUIL_CONFIANCE_MOYENNE = 0.60  # Match acceptable
SEUIL_CONFIANCE_BASSE = 0.40  # Match faible

# Chemins des fichiers de données
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SYMPTOMES_FILE = os.path.join(DATA_DIR, 'symptomes.json')
REGLES_FILE = os.path.join(DATA_DIR, 'regles.json')

# Configuration IA
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
USE_AI_EXPLANATION = bool(GEMINI_API_KEY)

# Modèle d'embeddings
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # Léger et performant

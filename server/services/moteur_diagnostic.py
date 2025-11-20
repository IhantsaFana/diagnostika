"""Moteur de diagnostic principal"""
import json
from typing import List, Dict
from models import Symptome, Diagnostic
from services.vectorisation import VectorisationService
import config

class MoteurDiagnostic:
    """Moteur de diagnostic basé sur les règles et la vectorisation"""
    
    def __init__(self):
        """Initialise le moteur avec les données et le service de vectorisation"""
        self.symptomes: Dict[str, Symptome] = {}
        self.diagnostics: List[Diagnostic] = []
        self.vectorisation = VectorisationService()
        self._charger_donnees()
    
    def _charger_donnees(self):
        """Charge les symptômes et règles depuis les fichiers JSON"""
        # Charger les symptômes
        try:
            with open(config.SYMPTOMES_FILE, 'r', encoding='utf-8') as f:
                symptomes_data = json.load(f)
                for data in symptomes_data:
                    symptome = Symptome.from_dict(data)
                    self.symptomes[symptome.id] = symptome
            print(f"[Moteur] {len(self.symptomes)} symptômes chargés")
        except Exception as e:
            print(f"[Moteur] Erreur chargement symptômes: {e}")
            raise
        
        # Charger les règles de diagnostic
        try:
            with open(config.REGLES_FILE, 'r', encoding='utf-8') as f:
                regles_data = json.load(f)
                for data in regles_data:
                    diagnostic = Diagnostic.from_dict(data)
                    self.diagnostics.append(diagnostic)
            print(f"[Moteur] {len(self.diagnostics)} règles de diagnostic chargées")
        except Exception as e:
            print(f"[Moteur] Erreur chargement règles: {e}")
            raise
        
        # Vectoriser les symptômes
        symptomes_list = [s.to_dict() for s in self.symptomes.values()]
        self.vectorisation.vectoriser_symptomes(symptomes_list)
    
    def get_symptomes_disponibles(self) -> List[Dict]:
        """Retourne la liste de tous les symptômes disponibles"""
        return [s.to_dict() for s in self.symptomes.values()]
    
    def rechercher_symptomes(self, texte: str, top_k: int = 5) -> List[Dict]:
        """
        Recherche des symptômes similaires à partir d'un texte libre
        
        Args:
            texte: Texte saisi par l'utilisateur
            top_k: Nombre de résultats
            
        Returns:
            Liste de symptômes avec leur score de similarité
        """
        resultats = self.vectorisation.trouver_symptomes_similaires(texte, top_k)
        
        symptomes_trouves = []
        for symptome_id, score in resultats:
            if symptome_id in self.symptomes:
                symptome_dict = self.symptomes[symptome_id].to_dict()
                symptome_dict['score_similarite'] = round(score, 3)
                symptomes_trouves.append(symptome_dict)
        
        return symptomes_trouves
    
    def diagnostiquer(self, symptomes_ids: List[str]) -> Dict:
        """
        Effectue un diagnostic basé sur les symptômes fournis
        Retourne : diagnostic, gravité, coût estimatif, description
        
        Args:
            symptomes_ids: Liste des IDs de symptômes
            
        Returns:
            Résultat du diagnostic
        """
        if not symptomes_ids:
            return {
                'succes': False,
                'erreur': 'Aucun symptôme fourni'
            }
        
        # Vérifier que les symptômes existent
        symptomes_valides = [sid for sid in symptomes_ids if sid in self.symptomes]
        if not symptomes_valides:
            return {
                'succes': False,
                'erreur': 'Aucun symptôme valide'
            }
        
        # Calculer les scores pour chaque règle
        resultats = []
        poids_symptomes = {sid: self.symptomes[sid].poids for sid in self.symptomes}
        
        for diagnostic in self.diagnostics:
            score = self.vectorisation.calculer_score_regle(
                symptomes_valides,
                diagnostic.symptomes_requis,
                diagnostic.symptomes_optionnels or [],
                poids_symptomes
            )
            
            if score > 0:
                resultats.append({
                    'diagnostic': diagnostic,
                    'score': score
                })
        
        # Trier par score décroissant
        resultats.sort(key=lambda x: x['score'], reverse=True)
        
        if not resultats:
            return self._diagnostic_incertain(symptomes_valides)
        
        # Meilleur diagnostic
        meilleur = resultats[0]
        score = meilleur['score']
        diagnostic = meilleur['diagnostic']
        
        # Déterminer le niveau de confiance
        if score >= config.SEUIL_CONFIANCE_HAUTE:
            confiance = 'Haute'
        elif score >= config.SEUIL_CONFIANCE_MOYENNE:
            confiance = 'Moyenne'
        else:
            confiance = 'Faible'
        
        # Préparer la réponse (seulement ce qui est demandé dans le sujet)
        reponse = {
            'succes': True,
            'diagnostic': diagnostic.nom,
            'description': diagnostic.description,
            'gravite': diagnostic.gravite,
            'cout_estimatif': diagnostic.to_dict()['cout_estimatif'],
            'conseils': diagnostic.conseils,
            'confiance': confiance,
            'score': round(score, 2),
            'symptomes_utilises': [self.symptomes[sid].nom for sid in symptomes_valides]
        }
        
        return reponse
    
    def _diagnostic_incertain(self, symptomes_ids: List[str]) -> Dict:
        """Génère une réponse pour un diagnostic incertain"""
        symptomes_noms = [self.symptomes[sid].nom for sid in symptomes_ids]
        
        return {
            'succes': True,
            'diagnostic': 'Diagnostic incertain',
            'description': 'Les symptômes observés ne correspondent pas clairement à un problème connu.',
            'gravite': 'Inconnu',
            'cout_estimatif': 'À déterminer',
            'conseils': 'Une inspection complète par un mécanicien est recommandée.',
            'confiance': 'Très faible',
            'score': 0.0,
            'symptomes_utilises': symptomes_noms
        }

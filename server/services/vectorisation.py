"""Service de vectorisation et calcul de similarité"""
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import config

class VectorisationService:
    """Gère la vectorisation des symptômes et le calcul de similarité"""
    
    def __init__(self):
        """Initialise le modèle d'embeddings"""
        print(f"[Vectorisation] Chargement du modèle {config.EMBEDDING_MODEL}...")
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.symptomes_vectors = {}
        print("[Vectorisation] Modèle chargé avec succès")
    
    def vectoriser_symptomes(self, symptomes: List[Dict]) -> None:
        """
        Pré-calcule les vecteurs pour tous les symptômes de la base
        
        Args:
            symptomes: Liste des symptômes avec id et nom
        """
        print(f"[Vectorisation] Vectorisation de {len(symptomes)} symptômes...")
        
        textes = [s['nom'] for s in symptomes]
        vectors = self.model.encode(textes, show_progress_bar=False)
        
        for symptome, vector in zip(symptomes, vectors):
            self.symptomes_vectors[symptome['id']] = vector
        
        print(f"[Vectorisation] {len(self.symptomes_vectors)} vecteurs créés")
    
    def trouver_symptomes_similaires(
        self, 
        texte_libre: str, 
        top_k: int = 5,
        seuil: float = 0.5
    ) -> List[Tuple[str, float]]:
        """
        Trouve les symptômes les plus similaires à un texte libre
        
        Args:
            texte_libre: Texte saisi par l'utilisateur
            top_k: Nombre de résultats à retourner
            seuil: Score minimum de similarité
            
        Returns:
            Liste de tuples (symptome_id, score)
        """
        if not texte_libre.strip():
            return []
        
        # Vectoriser le texte de l'utilisateur
        vector_utilisateur = self.model.encode([texte_libre], show_progress_bar=False)[0]
        
        # Calculer la similarité avec tous les symptômes
        similarites = []
        for symptome_id, symptome_vector in self.symptomes_vectors.items():
            score = cosine_similarity(
                vector_utilisateur.reshape(1, -1),
                symptome_vector.reshape(1, -1)
            )[0][0]
            
            if score >= seuil:
                similarites.append((symptome_id, float(score)))
        
        # Trier par score décroissant
        similarites.sort(key=lambda x: x[1], reverse=True)
        
        return similarites[:top_k]
    
    def calculer_score_regle(
        self,
        symptomes_utilisateur: List[str],
        symptomes_requis: List[str],
        symptomes_optionnels: List[str],
        poids_symptomes: Dict[str, float]
    ) -> float:
        """
        Calcule le score de correspondance entre symptômes utilisateur et une règle
        
        Args:
            symptomes_utilisateur: IDs des symptômes sélectionnés
            symptomes_requis: IDs des symptômes requis par la règle
            symptomes_optionnels: IDs des symptômes optionnels
            poids_symptomes: Poids de chaque symptôme
            
        Returns:
            Score entre 0 et 1
        """
        # Convertir en sets pour faciliter les opérations
        set_utilisateur = set(symptomes_utilisateur)
        set_requis = set(symptomes_requis)
        set_optionnels = set(symptomes_optionnels)
        
        # Symptômes requis présents
        requis_presents = set_utilisateur & set_requis
        
        # Si tous les symptômes requis ne sont pas présents, score faible
        if len(requis_presents) < len(set_requis):
            ratio_requis = len(requis_presents) / len(set_requis)
            return ratio_requis * 0.5  # Maximum 50% si incomplet
        
        # Tous les symptômes requis sont présents
        score_base = 0.8  # Score de base pour match complet des requis
        
        # Bonus pour les symptômes optionnels présents
        optionnels_presents = set_utilisateur & set_optionnels
        if set_optionnels:
            bonus_optionnels = (len(optionnels_presents) / len(set_optionnels)) * 0.2
            score_base += bonus_optionnels
        
        # Appliquer les poids des symptômes
        poids_total = sum(poids_symptomes.get(s, 1.0) for s in set_requis | set_optionnels)
        poids_presents = sum(poids_symptomes.get(s, 1.0) for s in requis_presents | optionnels_presents)
        
        if poids_total > 0:
            facteur_poids = poids_presents / poids_total
            score_final = score_base * facteur_poids
        else:
            score_final = score_base
        
        return min(score_final, 1.0)

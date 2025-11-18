"""Service d'assistance IA pour reformulation"""
import os
import config

class AssistantIA:
    """Gère l'intégration avec Gemini pour reformulation"""
    
    def __init__(self):
        """Initialise le service IA"""
        self.actif = config.USE_AI_EXPLANATION
        if self.actif:
            try:
                import google.generativeai as genai
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("[IA] Service Gemini activé")
            except Exception as e:
                print(f"[IA] Erreur initialisation Gemini: {e}")
                self.actif = False
        else:
            print("[IA] Service IA désactivé (pas de clé API)")
    
    def reformuler_diagnostic(self, diagnostic_data: dict) -> str:
        """
        Reformule un diagnostic en langage naturel
        
        Args:
            diagnostic_data: Données du diagnostic
            
        Returns:
            Explication reformulée ou description originale
        """
        if not self.actif:
            return diagnostic_data.get('description', '')
        
        try:
            prompt = f"""Tu es un mécanicien expert. Reformule ce diagnostic de manière claire et accessible.

Diagnostic : {diagnostic_data.get('diagnostic')}
Description technique : {diagnostic_data.get('description')}
Gravité : {diagnostic_data.get('gravite')}
Symptômes : {', '.join(diagnostic_data.get('symptomes_utilises', []))}

Fournis une explication en 2-3 phrases simples et rassurantes."""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'max_output_tokens': 200,
                }
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"[IA] Erreur reformulation: {e}")
            return diagnostic_data.get('description', '')

// Types pour l'application de diagnostic

export interface Symptome {
  id: string
  nom: string
  description?: string
  categorie?: string
  poids: number
  score_similarite?: number
}

export interface ResultatDiagnostic {
  succes: boolean
  diagnostic: string
  description: string
  gravite: string
  cout_estimatif: string
  conseils?: string
  confiance: string
  score: number
  symptomes_utilises: string[]
  explication_ia?: string
  erreur?: string
}

export interface ResultatRecherche {
  succes: boolean
  texte_recherche: string
  resultats: Symptome[]
}

// Service API pour communiquer avec le backend

const API_URL = 'http://localhost:5000'

export const api = {
  // Récupérer tous les symptômes
  async getSymptomes() {
    const response = await fetch(`${API_URL}/symptomes`)
    if (!response.ok) throw new Error('Erreur lors du chargement des symptômes')
    return response.json()
  },

  // Rechercher des symptômes par texte libre
  async rechercherSymptomes(texte: string) {
    const response = await fetch(`${API_URL}/rechercher`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texte })
    })
    if (!response.ok) throw new Error('Erreur lors de la recherche')
    return response.json()
  },

  // Effectuer un diagnostic
  async diagnostiquer(symptomes: string[]) {
    const response = await fetch(`${API_URL}/diagnostiquer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symptomes })
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.erreur || 'Erreur lors du diagnostic')
    return data
  }
}

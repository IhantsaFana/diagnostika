import { useState, useEffect } from 'react'
import './App.css'

interface DiagnosticResult {
  diagnostic: string
  gravite: string
  cout_estimatif: string
  explication_ia: string
  erreur?: string
}

const API_URL = 'http://localhost:5000'

function App() {
  const [symptomesDisponibles, setSymptomesDisponibles] = useState<string[]>([])
  const [symptomesSelectionnes, setSymptomesSelectionnes] = useState<string[]>([])
  const [resultat, setResultat] = useState<DiagnosticResult | null>(null)
  const [chargement, setChargement] = useState(false)
  const [erreur, setErreur] = useState<string>('')

  // Charger la liste des symptômes au démarrage
  useEffect(() => {
    fetch(`${API_URL}/symptomes`)
      .then(res => res.json())
      .then(data => setSymptomesDisponibles(data.symptomes))
      .catch(err => console.error('Erreur chargement symptômes:', err))
  }, [])

  const toggleSymptome = (symptome: string) => {
    setSymptomesSelectionnes(prev =>
      prev.includes(symptome)
        ? prev.filter(s => s !== symptome)
        : [...prev, symptome]
    )
    setErreur('')
  }

  const diagnostiquer = async () => {
    if (symptomesSelectionnes.length === 0) {
      setErreur('Veuillez sélectionner au moins un symptôme')
      return
    }

    setChargement(true)
    setErreur('')
    setResultat(null)

    try {
      const response = await fetch(`${API_URL}/diagnostiquer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptomes: symptomesSelectionnes })
      })

      const data = await response.json()

      if (!response.ok) {
        setErreur(data.erreur || 'Erreur lors du diagnostic')
      } else {
        setResultat(data)
      }
    } catch (err) {
      setErreur('Impossible de contacter le serveur. Vérifiez qu\'il est démarré.')
    } finally {
      setChargement(false)
    }
  }

  const reinitialiser = () => {
    setSymptomesSelectionnes([])
    setResultat(null)
    setErreur('')
  }

  const getGraviteColor = (gravite: string) => {
    switch (gravite.toLowerCase()) {
      case 'léger': return '#4caf50'
      case 'moyen': return '#ff9800'
      case 'critique': return '#f44336'
      default: return '#757575'
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🔧 Assistant de Diagnostic Automobile</h1>
        <p>Sélectionnez les symptômes observés sur le véhicule</p>
      </header>

      <main className="main">
        <section className="symptomes-section">
          <h2>Symptômes observés ({symptomesSelectionnes.length})</h2>
          <div className="symptomes-grid">
            {symptomesDisponibles.map(symptome => (
              <label key={symptome} className="symptome-checkbox">
                <input
                  type="checkbox"
                  checked={symptomesSelectionnes.includes(symptome)}
                  onChange={() => toggleSymptome(symptome)}
                />
                <span>{symptome}</span>
              </label>
            ))}
          </div>

          <div className="actions">
            <button
              onClick={diagnostiquer}
              disabled={chargement || symptomesSelectionnes.length === 0}
              className="btn-primary"
            >
              {chargement ? 'Analyse en cours...' : 'Diagnostiquer'}
            </button>
            <button onClick={reinitialiser} className="btn-secondary">
              Réinitialiser
            </button>
          </div>

          {erreur && (
            <div className="message error">
              ⚠️ {erreur}
            </div>
          )}
        </section>

        {resultat && (
          <section className="resultat-section">
            <h2>Résultat du diagnostic</h2>
            
            <div className="diagnostic-card">
              <div className="diagnostic-header">
                <h3>{resultat.diagnostic}</h3>
                <span
                  className="gravite-badge"
                  style={{ backgroundColor: getGraviteColor(resultat.gravite) }}
                >
                  {resultat.gravite}
                </span>
              </div>

              <div className="diagnostic-info">
                <div className="info-item">
                  <span className="label">💰 Coût estimatif :</span>
                  <span className="value">{resultat.cout_estimatif}</span>
                </div>
              </div>

              {resultat.explication_ia && (
                <div className="explication">
                  <h4>💡 Explication</h4>
                  <p>{resultat.explication_ia}</p>
                </div>
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App

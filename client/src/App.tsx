import { useState, useEffect } from 'react'
import { api } from './api'
import type { Symptome, ResultatDiagnostic } from './types'
import SearchBar from './components/SearchBar'
import SymptomesList from './components/SymptomesList'
import ResultatDiagnosticComponent from './components/ResultatDiagnostic'
import Modal from './components/Modal'
import { FaSearch, FaList, FaStethoscope, FaRedo } from 'react-icons/fa'
import { IoClose } from 'react-icons/io5'
import "./index.css"

const MAX_SYMPTOMES = 5

export default function App() {
  const [symptomes, setSymptomes] = useState<Symptome[]>([])
  const [symptomesSelectionnes, setSymptomesSelectionnes] = useState<string[]>([])
  const [resultatsRecherche, setResultatsRecherche] = useState<Symptome[]>([])
  const [resultatDiagnostic, setResultatDiagnostic] = useState<ResultatDiagnostic | null>(null)
  const [suggestionsAleatoires, setSuggestionsAleatoires] = useState<Symptome[]>([])
  
  const [isLoadingSymptomes, setIsLoadingSymptomes] = useState(true)
  const [isSearching, setIsSearching] = useState(false)
  const [isDiagnosing, setIsDiagnosing] = useState(false)
  const [error, setError] = useState<string>('')
  const [showModal, setShowModal] = useState(false)
  
  const [modeAffichage, setModeAffichage] = useState<'recherche' | 'liste'>('recherche')

  // Charger les symptômes au démarrage
  useEffect(() => {
    api.getSymptomes()
      .then(data => {
        setSymptomes(data.symptomes)
        // Générer suggestions aléatoires
        const shuffled = [...data.symptomes].sort(() => 0.5 - Math.random())
        setSuggestionsAleatoires(shuffled.slice(0, 6))
        setIsLoadingSymptomes(false)
      })
      .catch(() => {
        setError('Impossible de charger les symptômes. Vérifiez que le serveur est démarré.')
        setIsLoadingSymptomes(false)
      })
  }, [])

  // Recherche par texte libre
  const handleSearch = async (texte: string) => {
    setIsSearching(true)
    setError('')
    try {
      const data = await api.rechercherSymptomes(texte)
      setResultatsRecherche(data.resultats)
    } catch (err) {
      setError('Erreur lors de la recherche')
    } finally {
      setIsSearching(false)
    }
  }

  // Sélectionner un symptôme
  const handleSelectSymptome = (symptome: Symptome) => {
    if (symptomesSelectionnes.length >= MAX_SYMPTOMES) {
      setError(`Maximum ${MAX_SYMPTOMES} symptômes autorisés`)
      return
    }
    if (!symptomesSelectionnes.includes(symptome.id)) {
      setSymptomesSelectionnes([...symptomesSelectionnes, symptome.id])
      setResultatsRecherche([])
      setError('')
    }
  }

  // Toggle symptôme depuis la liste
  const handleToggleSymptome = (id: string) => {
    if (symptomesSelectionnes.includes(id)) {
      setSymptomesSelectionnes(symptomesSelectionnes.filter(s => s !== id))
    } else if (symptomesSelectionnes.length < MAX_SYMPTOMES) {
      setSymptomesSelectionnes([...symptomesSelectionnes, id])
    }
    setError('')
  }

  // Diagnostiquer
  const handleDiagnostiquer = async () => {
    if (symptomesSelectionnes.length === 0) {
      setError('Veuillez sélectionner au moins un symptôme')
      return
    }

    setIsDiagnosing(true)
    setError('')
    setResultatDiagnostic(null)

    try {
      const data = await api.diagnostiquer(symptomesSelectionnes)
      setResultatDiagnostic(data)
      setShowModal(true)
    } catch (err: any) {
      setError(err.message || 'Erreur lors du diagnostic')
    } finally {
      setIsDiagnosing(false)
    }
  }

  // Réinitialiser
  const handleReset = () => {
    setSymptomesSelectionnes([])
    setResultatsRecherche([])
    setResultatDiagnostic(null)
    setShowModal(false)
    setError('')
  }

  // Obtenir les noms des symptômes sélectionnés
  const getSymptomesSelectionnesNoms = () => {
    return symptomesSelectionnes
      .map(id => symptomes.find(s => s.id === id)?.nom)
      .filter(Boolean)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">🔧 Diagnostic Automobile</h1>
              <p className="text-gray-600 mt-1">Assistant intelligent de diagnostic</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Symptômes sélectionnés</p>
              <p className="text-2xl font-bold text-blue-600">{symptomesSelectionnes.length}/{MAX_SYMPTOMES}</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Message d'erreur global */}
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-700">⚠️ {error}</p>
          </div>
        )}

        {/* Loading initial */}
        {isLoadingSymptomes ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
            <p className="mt-4 text-gray-600">Chargement des symptômes...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Colonne gauche - Sélection */}
            <div className="lg:col-span-2 space-y-6">
              {/* Barre de recherche */}
              <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold text-gray-900">Rechercher des symptômes</h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setModeAffichage('recherche')}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        modeAffichage === 'recherche'
                          ? 'bg-blue-600 text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <FaSearch size={14} />
                      Recherche
                    </button>
                    <button
                      onClick={() => setModeAffichage('liste')}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        modeAffichage === 'liste'
                          ? 'bg-blue-600 text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <FaList size={14} />
                      Liste
                    </button>
                  </div>
                </div>

                {modeAffichage === 'recherche' ? (
                  <SearchBar
                    onSearch={handleSearch}
                    onSelectSymptome={handleSelectSymptome}
                    resultats={resultatsRecherche}
                    isLoading={isSearching}
                    suggestionsAleatoires={suggestionsAleatoires}
                  />
                ) : (
                  <div className="max-h-[600px] overflow-y-auto pr-2">
                    <SymptomesList
                      symptomes={symptomes}
                      symptomesSelectionnes={symptomesSelectionnes}
                      onToggle={handleToggleSymptome}
                      maxSelection={MAX_SYMPTOMES}
                    />
                  </div>
                )}
              </div>
            </div>

            {/* Colonne droite - Actions et Résultat */}
            <div className="space-y-6">
              {/* Symptômes sélectionnés */}
              <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-200">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Symptômes sélectionnés</h3>
                
                {symptomesSelectionnes.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">Aucun symptôme sélectionné</p>
                ) : (
                  <div className="space-y-2 mb-4">
                    {getSymptomesSelectionnesNoms().map((nom, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg border border-blue-200 shadow-sm">
                        <span className="text-sm text-gray-900 font-medium">{nom}</span>
                        <button
                          onClick={() => handleToggleSymptome(symptomesSelectionnes[index])}
                          className="text-red-600 hover:text-red-800 hover:bg-red-100 p-1 rounded transition-colors"
                        >
                          <IoClose size={20} />
                        </button>
                      </div>
                    ))}
                  </div>
                )}

                {/* Actions */}
                <div className="space-y-3 pt-4 border-t border-gray-200">
                  <button
                    onClick={handleDiagnostiquer}
                    disabled={symptomesSelectionnes.length === 0 || isDiagnosing}
                    className="w-full py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
                  >
                    {isDiagnosing ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                        Analyse en cours...
                      </>
                    ) : (
                      <>
                        <FaStethoscope size={18} />
                        Diagnostiquer
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleReset}
                    className="w-full py-3 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
                  >
                    <FaRedo size={16} />
                    Réinitialiser
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modal du résultat */}
        <Modal 
          isOpen={showModal} 
          onClose={() => setShowModal(false)}
        >
          {resultatDiagnostic && (
            <ResultatDiagnosticComponent resultat={resultatDiagnostic} />
          )}
        </Modal>
      </main>
    </div>
  )
}

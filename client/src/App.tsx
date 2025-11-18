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
        // Générer 7 suggestions aléatoires
        const shuffled = [...data.symptomes].sort(() => 0.5 - Math.random())
        setSuggestionsAleatoires(shuffled.slice(0, 7))
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
    } catch {
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
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white pb-6">
      {/* Header Principal */}
      <header>
        <div className="max-w-7xl mx-auto px-6 py-3">
          <div className="flex items-center gap-4">
            <img src="/diagnostika.svg" alt="Diagnostika" className="w-12 h-12" />
            <div>
              <h1 className="text-xl font-bold text-white">
                Assistant de Diagnostic
              </h1>
              <p className="text-slate-400 text-xs">Système expert automobile propulsé par IA</p>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-6">
          <div className="border-b border-slate-700"></div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6">
        {/* Message d'erreur */}
        {error && (
          <div className="mb-6 bg-red-500/10 border border-red-500/30 rounded-lg p-4 flex items-start gap-3">
            <div className="flex-shrink-0 mt-0.5">
              <div className="w-5 h-5 rounded-full bg-red-500/20 flex items-center justify-center">
                <span className="text-red-400 text-xs">!</span>
              </div>
            </div>
            <p className="text-red-300 text-sm flex-1">{error}</p>
            <button onClick={() => setError('')} className="text-red-400 hover:text-red-300">
              <IoClose size={18} />
            </button>
          </div>
        )}

        {/* Loading */}
        {isLoadingSymptomes ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-slate-700 border-t-blue-500 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <FaStethoscope className="text-blue-500" size={24} />
              </div>
            </div>
            <p className="mt-6 text-slate-400">Initialisation du système...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Zone principale */}
            <div className="lg:col-span-2 space-y-6">
              {/* Sélection des symptômes */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
                <div className="bg-slate-900/50 px-6 py-4 border-b border-slate-700 flex items-center justify-between">
                  <h2 className="font-semibold text-slate-200">Sélection des symptômes</h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setModeAffichage('recherche')}
                      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                        modeAffichage === 'recherche'
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-700/50 text-slate-400 hover:bg-slate-700'
                      }`}
                    >
                      <FaSearch size={12} />
                      Recherche
                    </button>
                    <button
                      onClick={() => setModeAffichage('liste')}
                      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                        modeAffichage === 'liste'
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-700/50 text-slate-400 hover:bg-slate-700'
                      }`}
                    >
                      <FaList size={12} />
                      Liste
                    </button>
                  </div>
                </div>

                <div className="p-6">
                  {modeAffichage === 'recherche' ? (
                    <SearchBar
                      onSearch={handleSearch}
                      onSelectSymptome={handleSelectSymptome}
                      resultats={resultatsRecherche}
                      isLoading={isSearching}
                      suggestionsAleatoires={suggestionsAleatoires}
                    />
                  ) : (
                    <div className="max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
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
            </div>

            {/* Panneau latéral */}
            <div className="space-y-6">
              {/* Symptômes sélectionnés */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 overflow-hidden">
                <div className="bg-slate-900/50 px-6 py-4 border-b border-slate-700">
                  <h3 className="font-semibold text-slate-200 text-sm">Symptômes actifs</h3>
                </div>
                
                <div className="p-6">
                  {symptomesSelectionnes.length === 0 ? (
                    <div className="text-center py-8">
                      <div className="w-12 h-12 rounded-full bg-slate-700/30 flex items-center justify-center mx-auto mb-3">
                        <FaStethoscope className="text-slate-600" size={20} />
                      </div>
                      <p className="text-slate-500 text-sm">Aucun symptôme sélectionné</p>
                    </div>
                  ) : (
                    <div className="space-y-2 mb-6">
                      {getSymptomesSelectionnesNoms().map((nom, index) => (
                        <div key={index} className="group flex items-center justify-between p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg hover:border-blue-500/50 transition-all">
                          <span className="text-sm text-slate-200 font-medium flex-1">{nom}</span>
                          <button
                            onClick={() => handleToggleSymptome(symptomesSelectionnes[index])}
                            className="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-300 hover:bg-red-500/10 p-1.5 rounded transition-all"
                          >
                            <IoClose size={16} />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="space-y-3 pt-4 border-t border-slate-700">
                    <button
                      onClick={handleDiagnostiquer}
                      disabled={symptomesSelectionnes.length === 0 || isDiagnosing}
                      className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
                    >
                      {isDiagnosing ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                          Analyse...
                        </>
                      ) : (
                        <>
                          <FaStethoscope size={16} />
                          Lancer le diagnostic
                        </>
                      )}
                    </button>
                    <button
                      onClick={handleReset}
                      className="w-full py-3 bg-slate-700 hover:bg-slate-600 text-slate-300 font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
                    >
                      <FaRedo size={14} />
                      Réinitialiser
                    </button>
                  </div>
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

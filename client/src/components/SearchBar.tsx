import { useState, useEffect, useRef } from 'react'
import type { Symptome } from '../types'

interface SearchBarProps {
  onSearch: (texte: string) => void
  onSelectSymptome: (symptome: Symptome) => void
  resultats: Symptome[]
  isLoading: boolean
  suggestionsAleatoires: Symptome[]
}

export default function SearchBar({ 
  onSearch, 
  onSelectSymptome, 
  resultats, 
  isLoading,
  suggestionsAleatoires 
}: SearchBarProps) {
  const [texte, setTexte] = useState('')
  const [showResults, setShowResults] = useState(false)
  const debounceTimer = useRef<number | null>(null)
  const searchBarRef = useRef<HTMLDivElement>(null)

  // Recherche automatique avec debounce
  useEffect(() => {
    if (debounceTimer.current !== null) {
      clearTimeout(debounceTimer.current)
    }

    if (texte.trim().length >= 3) {
      debounceTimer.current = window.setTimeout(() => {
        onSearch(texte)
        setShowResults(true)
      }, 300) // Attendre 300ms après la dernière frappe
    } else {
      setShowResults(false)
    }

    return () => {
      if (debounceTimer.current !== null) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [texte, onSearch])

  // Fermer les résultats si clic à l'extérieur
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchBarRef.current && !searchBarRef.current.contains(event.target as Node)) {
        setShowResults(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelectSymptome = (symptome: Symptome) => {
    onSelectSymptome(symptome)
    setTexte('')
    setShowResults(false)
  }

  const handleSuggestionClick = (symptome: Symptome) => {
    onSelectSymptome(symptome)
  }

  return (
    <div className="w-full" ref={searchBarRef}>
      {/* Champ de recherche */}
      <div className="relative">
        <input
          type="text"
          value={texte}
          onChange={(e) => setTexte(e.target.value)}
          onFocus={() => texte.length >= 3 && setShowResults(true)}
          placeholder="Décrivez le problème (ex: le moteur fait du bruit)..."
          className="w-full px-4 py-3 pr-12 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none text-gray-900 placeholder-gray-500 transition-colors"
          disabled={isLoading}
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2">
          {isLoading ? (
            <div className="animate-spin rounded-full h-5 w-5 border-2 border-blue-500 border-t-transparent"></div>
          ) : texte.length >= 3 ? (
            <span className="text-blue-600">🔍</span>
          ) : (
            <span className="text-gray-400">✏️</span>
          )}
        </div>
      </div>

      {/* Résultats de recherche (autocomplétion) */}
      {showResults && resultats.length > 0 && (
        <div className="mt-2 bg-white rounded-lg border-2 border-blue-300 shadow-xl max-h-80 overflow-y-auto animate-fadeIn">
          <div className="sticky top-0 bg-blue-50 px-4 py-2 border-b border-blue-200">
            <p className="text-sm font-medium text-blue-900">
              {resultats.length} résultat{resultats.length > 1 ? 's' : ''} trouvé{resultats.length > 1 ? 's' : ''}
            </p>
          </div>
          {resultats.map((symptome) => (
            <button
              key={symptome.id}
              onClick={() => handleSelectSymptome(symptome)}
              className="w-full text-left px-4 py-3 hover:bg-blue-50 border-b border-gray-100 last:border-b-0 transition-colors group"
            >
              <div className="flex items-center justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 group-hover:text-blue-700 transition-colors">
                    {symptome.nom}
                  </p>
                  {symptome.description && (
                    <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                      {symptome.description}
                    </p>
                  )}
                  {symptome.categorie && (
                    <span className="inline-block mt-1 text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
                      {symptome.categorie}
                    </span>
                  )}
                </div>
                {symptome.score_similarite && (
                  <div className="flex-shrink-0">
                    <div className="flex flex-col items-end">
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded">
                        {Math.round(symptome.score_similarite * 100)}%
                      </span>
                      <span className="text-xs text-gray-500 mt-1">pertinence</span>
                    </div>
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Message si recherche sans résultat */}
      {showResults && texte.length >= 3 && resultats.length === 0 && !isLoading && (
        <div className="mt-2 bg-yellow-50 border-2 border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800 text-sm">
            Aucun symptôme trouvé pour "{texte}". Essayez d'autres mots-clés.
          </p>
        </div>
      )}

      {/* Suggestions aléatoires */}
      {!showResults && suggestionsAleatoires.length > 0 && (
        <div className="mt-4">
          <p className="text-sm text-gray-600 mb-2 font-medium">💡 Suggestions rapides :</p>
          <div className="flex flex-wrap gap-2">
            {suggestionsAleatoires.map((symptome) => (
              <button
                key={symptome.id}
                onClick={() => handleSuggestionClick(symptome)}
                className="px-3 py-2 bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 border border-blue-200 rounded-lg text-sm text-gray-700 hover:text-gray-900 transition-all hover:shadow-md hover:scale-105"
              >
                {symptome.nom}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Aide */}
      <p className="text-xs text-gray-500 mt-3">
        💡 Tapez au moins 3 caractères pour rechercher automatiquement
      </p>
    </div>
  )
}

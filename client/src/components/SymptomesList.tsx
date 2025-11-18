import type { Symptome } from '../types'

interface SymptomesListProps {
  symptomes: Symptome[]
  symptomesSelectionnes: string[]
  onToggle: (id: string) => void
  maxSelection: number
}

export default function SymptomesList({ 
  symptomes, 
  symptomesSelectionnes, 
  onToggle,
  maxSelection 
}: SymptomesListProps) {
  // Grouper par catégorie
  const categories = symptomes.reduce((acc, symptome) => {
    const cat = symptome.categorie || 'Autre'
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(symptome)
    return acc
  }, {} as Record<string, Symptome[]>)

  const isMaxReached = symptomesSelectionnes.length >= maxSelection

  return (
    <div className="space-y-6">
      {Object.entries(categories).map(([categorie, symptomsInCat]) => (
        <div key={categorie} className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">{categorie}</h3>
          </div>
          <div className="p-2 grid grid-cols-1 md:grid-cols-2 gap-2">
            {symptomsInCat.map((symptome) => {
              const isSelected = symptomesSelectionnes.includes(symptome.id)
              const isDisabled = !isSelected && isMaxReached

              return (
                <label
                  key={symptome.id}
                  className={`
                    flex items-start gap-3 p-3 rounded-lg border-2 cursor-pointer transition-all
                    ${isSelected 
                      ? 'bg-blue-50 border-blue-500' 
                      : isDisabled
                        ? 'bg-gray-50 border-gray-200 opacity-50 cursor-not-allowed'
                        : 'bg-white border-gray-200 hover:border-blue-300 hover:bg-blue-50'
                    }
                  `}
                >
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => onToggle(symptome.id)}
                    disabled={isDisabled}
                    className="mt-1 w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 text-sm">{symptome.nom}</p>
                    {symptome.description && (
                      <p className="text-xs text-gray-600 mt-1">{symptome.description}</p>
                    )}
                  </div>
                </label>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}

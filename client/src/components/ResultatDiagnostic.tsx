import type { ResultatDiagnostic } from '../types'
import { 
  FaCheckCircle, 
  FaExclamationTriangle, 
  FaTimesCircle
} from 'react-icons/fa'
import { IoSparkles } from 'react-icons/io5'

interface ResultatDiagnosticProps {
  resultat: ResultatDiagnostic
}

export default function ResultatDiagnosticComponent({ resultat }: ResultatDiagnosticProps) {
  // Fonction pour formater le coût (ex: "12 000Ar - 25 000Ar" => "12K - 25K MGA")
  const formatCout = (cout: string) => {
    // Extraire les nombres et convertir en K
    const matches = cout.match(/(\d+)\s*(\d+)?/g)
    if (matches && matches.length >= 2) {
      const min = parseInt(matches[0].replace(/\s/g, ''))
      const max = parseInt(matches[1].replace(/\s/g, ''))
      return `${min / 1000}K - ${max / 1000}K MGA`
    }
    return cout
  }

  const getGraviteConfig = (gravite: string) => {
    switch (gravite.toLowerCase()) {
      case 'léger': 
        return {
          gradient: 'from-green-500 to-emerald-600',
          bgColor: 'bg-green-50',
          textColor: 'text-green-800',
          borderColor: 'border-green-200',
          icon: <FaCheckCircle size={32} />,
          iconBg: 'bg-green-100'
        }
      case 'moyen': 
        return {
          gradient: 'from-orange-500 to-amber-600',
          bgColor: 'bg-orange-50',
          textColor: 'text-orange-800',
          borderColor: 'border-orange-200',
          icon: <FaExclamationTriangle size={32} />,
          iconBg: 'bg-orange-100'
        }
      case 'critique': 
        return {
          gradient: 'from-red-500 to-rose-600',
          bgColor: 'bg-red-50',
          textColor: 'text-red-800',
          borderColor: 'border-red-200',
          icon: <FaTimesCircle size={32} />,
          iconBg: 'bg-red-100'
        }
      default: 
        return {
          gradient: 'from-gray-500 to-gray-600',
          bgColor: 'bg-gray-50',
          textColor: 'text-gray-800',
          borderColor: 'border-gray-200',
          icon: <FaExclamationTriangle size={32} />,
          iconBg: 'bg-gray-100'
        }
    }
  }

  const config = getGraviteConfig(resultat.gravite)
  const explication = resultat.explication_ia || resultat.description

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Diagnostic Principal */}
      <div className="relative overflow-hidden rounded-3xl shadow-2xl">
        {/* Vidéo en arrière-plan */}
        <video 
          autoPlay 
          loop 
          muted 
          playsInline
          className="absolute inset-0 w-full h-full object-cover rounded-3xl"
        >
          <source src="/voiture.mp4" type="video/mp4" />
        </video>
        
        {/* Overlay gradient blanc transparent pour la lisibilité (bas vers haut, 0 to 50%) */}
        <div className="absolute inset-0 bg-gradient-to-t from-white/50 to-transparent"></div>
        
        {/* Contenu */}
        <div className="relative p-8">
          <div className="flex items-start justify-between gap-6 h-full">
            {/* Informations principales - Gauche */}
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <span className={`px-4 py-1.5 ${config.bgColor} ${config.textColor} backdrop-blur-md rounded-full text-sm font-semibold ${config.borderColor} border-2 shadow-lg`}>
                  {resultat.gravite}
                </span>
                {resultat.confiance && (
                  <span className={`px-4 py-1.5 ${config.bgColor} ${config.textColor} backdrop-blur-md rounded-full text-sm font-semibold ${config.borderColor} border-2 shadow-lg`}>
                    {resultat.confiance}
                  </span>
                )}
              </div>
              
              <h2 className="text-4xl font-bold mb-2 drop-shadow-lg text-gray-900">
                {resultat.diagnostic}
              </h2>
              
              <p className="text-gray-900 text-lg font-medium mb-4">
                Diagnostic établi avec {resultat.score ? `${Math.round(resultat.score * 100)}%` : 'haute'} précision
              </p>
            </div>

            {/* Coût en bas à droite, aligné parallèlement */}
            <div className="flex flex-col justify-end pt-16">
              <p className="text-gray-800 text-sm font-medium mb-1 text-right">Coût estimatif</p>
              <p className="text-2xl font-bold text-gray-900 text-right">
                {formatCout(resultat.cout_estimatif)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Explication */}
      <div className="rounded-2xl p-8 bg-slate-50 border border-slate-200">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex-shrink-0">
            <img src="/diagnostika.svg" alt="Diagnostika" className="w-10 h-10" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-xl font-bold text-slate-900">
                Explication IA
              </h3>
              <IoSparkles className="text-blue-500 animate-pulse" size={20} />
            </div>
            <p className="text-slate-700 leading-relaxed text-lg text-justify">
              {explication}
            </p>
          </div>
        </div>

        {/* Conseils si disponibles */}
        {resultat.conseils && (
          <div className="mt-6 pt-6 border-t border-slate-300">
            <p className="text-slate-900 font-semibold mb-2 flex items-center gap-2">
              <span>💡</span>
              <span>Conseil</span>
            </p>
            <p className="text-slate-700 leading-relaxed">
              {resultat.conseils}
            </p>
          </div>
        )}
      </div>

      {/* Footer avec info */}
      <div className="text-center">
        <p className="text-gray-500 text-sm">
          Ce diagnostic est basé sur l'analyse de {resultat.symptomes_utilises?.length || 0} symptôme(s)
        </p>
      </div>
    </div>
  )
}

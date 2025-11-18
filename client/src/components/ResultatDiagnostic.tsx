import type { ResultatDiagnostic } from '../types'
import { 
  FaCheckCircle, 
  FaExclamationTriangle, 
  FaTimesCircle,
  FaMoneyBillWave,
  FaRobot
} from 'react-icons/fa'
import { IoSparkles } from 'react-icons/io5'

interface ResultatDiagnosticProps {
  resultat: ResultatDiagnostic
}

export default function ResultatDiagnosticComponent({ resultat }: ResultatDiagnosticProps) {
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
      <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${config.gradient} p-8 text-white shadow-2xl`}>
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32 blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-black/10 rounded-full -ml-24 -mb-24 blur-2xl"></div>
        
        <div className="relative flex items-start gap-6">
          <div className={`flex-shrink-0 ${config.iconBg} p-4 rounded-2xl shadow-lg backdrop-blur-sm`}>
            {config.icon}
          </div>
          
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-3">
              <span className="px-4 py-1.5 bg-white/20 backdrop-blur-md rounded-full text-sm font-semibold border border-white/30 shadow-lg">
                {resultat.gravite}
              </span>
              {resultat.confiance && (
                <span className="px-4 py-1.5 bg-white/20 backdrop-blur-md rounded-full text-sm font-semibold border border-white/30 shadow-lg">
                  {resultat.confiance}
                </span>
              )}
            </div>
            
            <h2 className="text-4xl font-bold mb-2 drop-shadow-lg">
              {resultat.diagnostic}
            </h2>
            
            <p className="text-white/90 text-lg">
              Diagnostic établi avec {resultat.score ? `${Math.round(resultat.score * 100)}%` : 'haute'} précision
            </p>
          </div>
        </div>
      </div>

      {/* Coût Estimatif */}
      <div className="bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 rounded-2xl p-8 border-2 border-green-200 shadow-xl hover:shadow-2xl transition-shadow">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-br from-green-400 to-emerald-500 p-4 rounded-2xl shadow-lg">
              <FaMoneyBillWave className="text-white" size={28} />
            </div>
            <div>
              <p className="text-gray-600 text-sm font-medium mb-1">Coût estimatif de la réparation</p>
              <p className="text-4xl font-bold text-green-700">
                {resultat.cout_estimatif}
              </p>
            </div>
          </div>
          <div className="hidden sm:block text-6xl opacity-10">💰</div>
        </div>
      </div>

      {/* Explication */}
      <div className="bg-gradient-to-br from-purple-50 via-pink-50 to-purple-50 rounded-2xl p-8 border-2 border-purple-200 shadow-xl">
        <div className="flex items-start gap-4 mb-4">
          <div className="flex-shrink-0 bg-gradient-to-br from-purple-400 to-pink-500 p-3 rounded-xl shadow-lg">
            <FaRobot className="text-white" size={24} />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-xl font-bold text-purple-900">
                {resultat.explication_ia ? 'Explication IA' : 'Explication'}
              </h3>
              {resultat.explication_ia && (
                <IoSparkles className="text-purple-500 animate-pulse" size={20} />
              )}
            </div>
            <p className="text-purple-800 leading-relaxed text-lg">
              {explication}
            </p>
          </div>
        </div>

        {/* Conseils si disponibles */}
        {resultat.conseils && (
          <div className="mt-6 pt-6 border-t-2 border-purple-200">
            <p className="text-purple-700 font-medium mb-2">💡 Conseil :</p>
            <p className="text-purple-800 leading-relaxed">
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

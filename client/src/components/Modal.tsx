import { useEffect } from 'react'
import { IoClose } from 'react-icons/io5'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
}

export default function Modal({ isOpen, onClose, children }: ModalProps) {
  // Fermer avec Escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Overlay */}
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-md animate-fadeIn"
        onClick={onClose}
      />
      
      {/* Modal Container */}
      <div className="relative z-10 w-full max-w-6xl">
        {/* Bouton fermer externe */}
        <button
          onClick={onClose}
          className="absolute -top-3 -right-3 z-20 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-full p-2 shadow-2xl transition-all hover:scale-110 border-2 border-slate-600"
          aria-label="Fermer"
        >
          <IoClose size={20} />
        </button>

        {/* Modal Content */}
        <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl shadow-2xl w-full max-h-[95vh] overflow-hidden animate-scaleIn border border-slate-700">
          <div className="overflow-y-auto max-h-[95vh] p-8 modal-scrollbar">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}

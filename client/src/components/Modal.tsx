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
        className="absolute inset-0 bg-black/60 backdrop-blur-sm animate-fadeIn"
        onClick={onClose}
      />
      
      {/* Modal Container */}
      <div className="relative z-10 w-full max-w-6xl">
        {/* Bouton fermer externe */}
        <button
          onClick={onClose}
          className="absolute -top-4 -right-4 z-20 bg-white hover:bg-gray-100 text-gray-700 hover:text-gray-900 rounded-full p-3 shadow-2xl transition-all hover:scale-110 border-2 border-gray-200"
          aria-label="Fermer"
        >
          <IoClose size={24} />
        </button>

        {/* Modal Content */}
        <div className="bg-white rounded-2xl shadow-2xl w-full max-h-[95vh] overflow-hidden animate-scaleIn">
          <div className="overflow-y-auto max-h-[95vh] p-8">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}

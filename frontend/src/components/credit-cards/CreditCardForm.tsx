import { useState, useEffect } from 'react'
import { CreditCard, CreateCreditCardData } from '../../types/creditCard'

interface CreditCardFormProps {
  card: CreditCard | null
  onSubmit: (data: CreateCreditCardData) => void
  onCancel: () => void
  isLoading: boolean
}

const CreditCardForm = ({ card, onSubmit, onCancel, isLoading }: CreditCardFormProps) => {
  const [formData, setFormData] = useState<CreateCreditCardData>({
    name: '',
    creditLimit: 0,
    currentBalance: 0
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (card) {
      setFormData({
        name: card.name,
        creditLimit: card.creditLimit,
        currentBalance: card.currentBalance
      })
    } else {
      setFormData({
        name: '',
        creditLimit: 0,
        currentBalance: 0
      })
    }
    setErrors({})
  }, [card])

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Card name is required'
    }

    if (formData.creditLimit <= 0) {
      newErrors.creditLimit = 'Credit limit must be greater than 0'
    }

    if (formData.currentBalance < 0) {
      newErrors.currentBalance = 'Current balance cannot be negative'
    }

    if (formData.currentBalance > formData.creditLimit) {
      newErrors.currentBalance = 'Current balance cannot exceed credit limit'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  const handleChange = (field: keyof CreateCreditCardData, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[field]
        return newErrors
      })
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">
        {card ? 'Edit Credit Card' : 'Add New Credit Card'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Card Name *
          </label>
          <input
            type="text"
            id="name"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., Chase Sapphire, Amex Gold"
            disabled={isLoading}
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-600">{errors.name}</p>
          )}
        </div>

        <div>
          <label htmlFor="creditLimit" className="block text-sm font-medium text-gray-700 mb-1">
            Credit Limit *
          </label>
          <input
            type="number"
            id="creditLimit"
            value={formData.creditLimit || ''}
            onChange={(e) => handleChange('creditLimit', parseFloat(e.target.value) || 0)}
            step="0.01"
            min="0"
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.creditLimit ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="0.00"
            disabled={isLoading}
          />
          {errors.creditLimit && (
            <p className="mt-1 text-sm text-red-600">{errors.creditLimit}</p>
          )}
        </div>

        <div>
          <label htmlFor="currentBalance" className="block text-sm font-medium text-gray-700 mb-1">
            Current Balance *
          </label>
          <input
            type="number"
            id="currentBalance"
            value={formData.currentBalance || ''}
            onChange={(e) => handleChange('currentBalance', parseFloat(e.target.value) || 0)}
            step="0.01"
            min="0"
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.currentBalance ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="0.00"
            disabled={isLoading}
          />
          {errors.currentBalance && (
            <p className="mt-1 text-sm text-red-600">{errors.currentBalance}</p>
          )}
        </div>

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Saving...' : card ? 'Update Card' : 'Add Card'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 disabled:bg-gray-100 disabled:cursor-not-allowed font-medium"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

export default CreditCardForm

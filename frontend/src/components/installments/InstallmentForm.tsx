import { useState } from 'react'
import { CreateInstallmentData } from '../../types/installment'

interface InstallmentFormProps {
  onSubmit: (data: CreateInstallmentData) => void
  onCancel: () => void
  isLoading: boolean
}

const InstallmentForm = ({ onSubmit, onCancel, isLoading }: InstallmentFormProps) => {
  const [formData, setFormData] = useState<CreateInstallmentData>({
    totalAmount: 0,
    numberOfPayments: 1,
    startDate: new Date().toISOString().split('T')[0],
    description: ''
  })

  const [errors, setErrors] = useState<Record<string, string>>({})
  const [monthlyPayment, setMonthlyPayment] = useState(0)

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (formData.totalAmount <= 0) {
      newErrors.totalAmount = 'Total amount must be greater than 0'
    }

    if (formData.numberOfPayments <= 0) {
      newErrors.numberOfPayments = 'Number of payments must be greater than 0'
    }

    if (!formData.startDate) {
      newErrors.startDate = 'Start date is required'
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required'
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

  const handleChange = (field: keyof CreateInstallmentData, value: string | number) => {
    const newFormData = { ...formData, [field]: value }
    setFormData(newFormData)
    
    // Calculate monthly payment
    if (field === 'totalAmount' || field === 'numberOfPayments') {
      const total = field === 'totalAmount' ? Number(value) : formData.totalAmount
      const payments = field === 'numberOfPayments' ? Number(value) : formData.numberOfPayments
      
      if (total > 0 && payments > 0) {
        setMonthlyPayment(total / payments)
      } else {
        setMonthlyPayment(0)
      }
    }
    
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[field]
        return newErrors
      })
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Add New Installment</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description *
          </label>
          <input
            type="text"
            id="description"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.description ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., iPhone 15 Pro, Laptop, Furniture"
            disabled={isLoading}
          />
          {errors.description && (
            <p className="mt-1 text-sm text-red-600">{errors.description}</p>
          )}
        </div>

        <div>
          <label htmlFor="totalAmount" className="block text-sm font-medium text-gray-700 mb-1">
            Total Amount *
          </label>
          <input
            type="number"
            id="totalAmount"
            value={formData.totalAmount || ''}
            onChange={(e) => handleChange('totalAmount', parseFloat(e.target.value) || 0)}
            step="0.01"
            min="0"
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.totalAmount ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="0.00"
            disabled={isLoading}
          />
          {errors.totalAmount && (
            <p className="mt-1 text-sm text-red-600">{errors.totalAmount}</p>
          )}
        </div>

        <div>
          <label htmlFor="numberOfPayments" className="block text-sm font-medium text-gray-700 mb-1">
            Number of Payments *
          </label>
          <input
            type="number"
            id="numberOfPayments"
            value={formData.numberOfPayments || ''}
            onChange={(e) => handleChange('numberOfPayments', parseInt(e.target.value) || 1)}
            min="1"
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.numberOfPayments ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="12"
            disabled={isLoading}
          />
          {errors.numberOfPayments && (
            <p className="mt-1 text-sm text-red-600">{errors.numberOfPayments}</p>
          )}
        </div>

        <div>
          <label htmlFor="startDate" className="block text-sm font-medium text-gray-700 mb-1">
            Start Date *
          </label>
          <input
            type="date"
            id="startDate"
            value={formData.startDate}
            onChange={(e) => handleChange('startDate', e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.startDate ? 'border-red-500' : 'border-gray-300'
            }`}
            disabled={isLoading}
          />
          {errors.startDate && (
            <p className="mt-1 text-sm text-red-600">{errors.startDate}</p>
          )}
        </div>

        {monthlyPayment > 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
            <p className="text-sm text-gray-700">
              Monthly Payment: <span className="font-semibold text-blue-700">{formatCurrency(monthlyPayment)}</span>
            </p>
          </div>
        )}

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Adding...' : 'Add Installment'}
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

export default InstallmentForm

import { useState, useEffect } from 'react'
import { MonthlyIncome, CreateIncomeData } from '../../types/income'

interface MonthlyIncomeFormProps {
  income: MonthlyIncome | null
  onSubmit: (data: CreateIncomeData) => void
  onCancel: () => void
  isLoading: boolean
}

const MonthlyIncomeForm = ({ income, onSubmit, onCancel, isLoading }: MonthlyIncomeFormProps) => {
  const currentDate = new Date()
  const [formData, setFormData] = useState<CreateIncomeData>({
    month: currentDate.getMonth() + 1,
    year: currentDate.getFullYear(),
    amount: 0
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (income) {
      setFormData({
        month: income.month,
        year: income.year,
        amount: income.amount
      })
    } else {
      setFormData({
        month: currentDate.getMonth() + 1,
        year: currentDate.getFullYear(),
        amount: 0
      })
    }
    setErrors({})
  }, [income])

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (formData.month < 1 || formData.month > 12) {
      newErrors.month = 'Month must be between 1 and 12'
    }

    if (formData.year < 1900 || formData.year > 9999) {
      newErrors.year = 'Year must be a valid 4-digit year'
    }

    if (formData.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
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

  const handleChange = (field: keyof CreateIncomeData, value: string | number) => {
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

  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">
        {income ? 'Update Monthly Income' : 'Set Monthly Income'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="month" className="block text-sm font-medium text-gray-700 mb-1">
              Month *
            </label>
            <select
              id="month"
              value={formData.month}
              onChange={(e) => handleChange('month', parseInt(e.target.value))}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.month ? 'border-red-500' : 'border-gray-300'
              }`}
              disabled={isLoading}
            >
              {months.map((month, index) => (
                <option key={index + 1} value={index + 1}>
                  {month}
                </option>
              ))}
            </select>
            {errors.month && (
              <p className="mt-1 text-sm text-red-600">{errors.month}</p>
            )}
          </div>

          <div>
            <label htmlFor="year" className="block text-sm font-medium text-gray-700 mb-1">
              Year *
            </label>
            <input
              type="number"
              id="year"
              value={formData.year}
              onChange={(e) => handleChange('year', parseInt(e.target.value) || currentDate.getFullYear())}
              min="1900"
              max="9999"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.year ? 'border-red-500' : 'border-gray-300'
              }`}
              disabled={isLoading}
            />
            {errors.year && (
              <p className="mt-1 text-sm text-red-600">{errors.year}</p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-1">
            Gross Income Amount *
          </label>
          <input
            type="number"
            id="amount"
            value={formData.amount || ''}
            onChange={(e) => handleChange('amount', parseFloat(e.target.value) || 0)}
            step="0.01"
            min="0"
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.amount ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="0.00"
            disabled={isLoading}
          />
          {errors.amount && (
            <p className="mt-1 text-sm text-red-600">{errors.amount}</p>
          )}
        </div>

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Saving...' : income ? 'Update Income' : 'Set Income'}
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

export default MonthlyIncomeForm

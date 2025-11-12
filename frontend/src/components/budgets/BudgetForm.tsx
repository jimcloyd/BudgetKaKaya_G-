import { useState, useEffect } from 'react'
import { Category } from '../../types/expense'
import { BudgetLimit, CreateBudgetData } from '../../types/budget'

interface BudgetFormProps {
  categories: Category[]
  budget?: BudgetLimit | null
  onSubmit: (data: CreateBudgetData) => void
  onCancel: () => void
  isLoading?: boolean
}

const BudgetForm = ({ categories, budget, onSubmit, onCancel, isLoading }: BudgetFormProps) => {
  const [formData, setFormData] = useState<CreateBudgetData>({
    categoryId: '',
    amount: 0,
    period: 'monthly'
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (budget) {
      setFormData({
        categoryId: budget.categoryId,
        amount: budget.amount,
        period: budget.period
      })
    }
  }, [budget])

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.categoryId) {
      newErrors.categoryId = 'Category is required'
    }

    if (!formData.amount || formData.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    }

    if (formData.amount && !/^\d+(\.\d{1,2})?$/.test(formData.amount.toString())) {
      newErrors.amount = 'Amount must have at most 2 decimal places'
    }

    if (!formData.period) {
      newErrors.period = 'Period is required'
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

  const handleChange = (field: keyof CreateBudgetData, value: string | number) => {
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
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow space-y-4">
      <h3 className="text-lg font-semibold mb-4">
        {budget ? 'Edit Budget Limit' : 'Set Budget Limit'}
      </h3>

      <div className="flex flex-col gap-2">
        <label htmlFor="categoryId" className="text-sm font-medium text-gray-700">
          Category <span className="text-red-500">*</span>
        </label>
        <select
          id="categoryId"
          value={formData.categoryId}
          onChange={(e) => handleChange('categoryId', e.target.value)}
          disabled={!!budget}
          className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.categoryId ? 'border-red-500' : 'border-gray-300'
          } ${budget ? 'bg-gray-100 cursor-not-allowed' : ''}`}
        >
          <option value="">Select a category</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
        {errors.categoryId && (
          <span className="text-sm text-red-500">{errors.categoryId}</span>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <label htmlFor="amount" className="text-sm font-medium text-gray-700">
          Budget Amount <span className="text-red-500">*</span>
        </label>
        <input
          type="number"
          id="amount"
          step="0.01"
          min="0"
          value={formData.amount || ''}
          onChange={(e) => handleChange('amount', parseFloat(e.target.value))}
          className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.amount ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="0.00"
        />
        {errors.amount && (
          <span className="text-sm text-red-500">{errors.amount}</span>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <label htmlFor="period" className="text-sm font-medium text-gray-700">
          Period <span className="text-red-500">*</span>
        </label>
        <select
          id="period"
          value={formData.period}
          onChange={(e) => handleChange('period', e.target.value as 'weekly' | 'monthly')}
          className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.period ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        {errors.period && (
          <span className="text-sm text-red-500">{errors.period}</span>
        )}
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={isLoading}
          className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Saving...' : budget ? 'Update Budget' : 'Set Budget'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}

export default BudgetForm

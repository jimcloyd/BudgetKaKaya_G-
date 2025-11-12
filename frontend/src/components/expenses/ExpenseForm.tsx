import { useState, useEffect } from 'react'
import { Category, CreateExpenseData, Expense } from '../../types/expense'

interface ExpenseFormProps {
  categories: Category[]
  expense?: Expense | null
  onSubmit: (data: CreateExpenseData) => void
  onCancel: () => void
  isLoading?: boolean
}

const ExpenseForm = ({ categories, expense, onSubmit, onCancel, isLoading }: ExpenseFormProps) => {
  const [formData, setFormData] = useState<CreateExpenseData>({
    amount: 0,
    categoryId: '',
    date: new Date().toISOString().split('T')[0],
    description: ''
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (expense) {
      setFormData({
        amount: expense.amount,
        categoryId: expense.categoryId,
        date: expense.date,
        description: expense.description
      })
    }
  }, [expense])

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.amount || formData.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0'
    }

    if (formData.amount && !/^\d+(\.\d{1,2})?$/.test(formData.amount.toString())) {
      newErrors.amount = 'Amount must have at most 2 decimal places'
    }

    if (!formData.categoryId) {
      newErrors.categoryId = 'Category is required'
    }

    if (!formData.date) {
      newErrors.date = 'Date is required'
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

  const handleChange = (field: keyof CreateExpenseData, value: string | number) => {
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
        {expense ? 'Edit Expense' : 'Add New Expense'}
      </h3>

      <div className="flex flex-col gap-2">
        <label htmlFor="amount" className="text-sm font-medium text-gray-700">
          Amount <span className="text-red-500">*</span>
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
        <label htmlFor="categoryId" className="text-sm font-medium text-gray-700">
          Category <span className="text-red-500">*</span>
        </label>
        <select
          id="categoryId"
          value={formData.categoryId}
          onChange={(e) => handleChange('categoryId', e.target.value)}
          className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.categoryId ? 'border-red-500' : 'border-gray-300'
          }`}
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
        <label htmlFor="date" className="text-sm font-medium text-gray-700">
          Date <span className="text-red-500">*</span>
        </label>
        <input
          type="date"
          id="date"
          value={formData.date}
          onChange={(e) => handleChange('date', e.target.value)}
          className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.date ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        {errors.date && (
          <span className="text-sm text-red-500">{errors.date}</span>
        )}
      </div>

      <div className="flex flex-col gap-2">
        <label htmlFor="description" className="text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(e) => handleChange('description', e.target.value)}
          rows={3}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Optional description"
        />
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={isLoading}
          className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Saving...' : expense ? 'Update Expense' : 'Add Expense'}
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

export default ExpenseForm

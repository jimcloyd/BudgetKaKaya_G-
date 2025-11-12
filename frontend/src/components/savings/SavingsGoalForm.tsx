import { useState, useEffect } from 'react'
import { SavingsGoal, CreateSavingsGoalData } from '../../types/savings'

interface SavingsGoalFormProps {
  goal: SavingsGoal | null
  onSubmit: (data: CreateSavingsGoalData) => void
  onCancel: () => void
  isLoading: boolean
}

const SavingsGoalForm = ({ goal, onSubmit, onCancel, isLoading }: SavingsGoalFormProps) => {
  const [formData, setFormData] = useState<CreateSavingsGoalData>({
    name: '',
    targetAmount: 0,
    targetDate: ''
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (goal) {
      setFormData({
        name: goal.name,
        targetAmount: goal.targetAmount,
        targetDate: goal.targetDate || ''
      })
    } else {
      setFormData({
        name: '',
        targetAmount: 0,
        targetDate: ''
      })
    }
    setErrors({})
  }, [goal])

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Goal name is required'
    }

    if (formData.targetAmount <= 0) {
      newErrors.targetAmount = 'Target amount must be greater than 0'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (validateForm()) {
      // Remove targetDate if empty
      const submitData = { ...formData }
      if (!submitData.targetDate) {
        delete submitData.targetDate
      }
      onSubmit(submitData)
    }
  }

  const handleChange = (field: keyof CreateSavingsGoalData, value: string | number) => {
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
        {goal ? 'Edit Savings Goal' : 'Add New Savings Goal'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Goal Name *
          </label>
          <input
            type="text"
            id="name"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="e.g., Emergency Fund, Vacation, New Car"
            disabled={isLoading}
          />
          {errors.name && (
            <p className="mt-1 text-sm text-red-600">{errors.name}</p>
          )}
        </div>

        <div>
          <label htmlFor="targetAmount" className="block text-sm font-medium text-gray-700 mb-1">
            Target Amount *
          </label>
          <input
            type="number"
            id="targetAmount"
            value={formData.targetAmount || ''}
            onChange={(e) => handleChange('targetAmount', parseFloat(e.target.value) || 0)}
            step="0.01"
            min="0"
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.targetAmount ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="0.00"
            disabled={isLoading}
          />
          {errors.targetAmount && (
            <p className="mt-1 text-sm text-red-600">{errors.targetAmount}</p>
          )}
        </div>

        <div>
          <label htmlFor="targetDate" className="block text-sm font-medium text-gray-700 mb-1">
            Target Date (Optional)
          </label>
          <input
            type="date"
            id="targetDate"
            value={formData.targetDate || ''}
            onChange={(e) => handleChange('targetDate', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <p className="mt-1 text-xs text-gray-500">
            Setting a target date will show suggested monthly contributions
          </p>
        </div>

        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? 'Saving...' : goal ? 'Update Goal' : 'Add Goal'}
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

export default SavingsGoalForm

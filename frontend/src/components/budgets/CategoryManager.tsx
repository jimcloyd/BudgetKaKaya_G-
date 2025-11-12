import { useState } from 'react'
import { Category } from '../../types/expense'

interface CategoryManagerProps {
  categories: Category[]
  onAddCategory: (name: string) => void
  isLoading?: boolean
}

const CategoryManager = ({ categories, onAddCategory, isLoading }: CategoryManagerProps) => {
  const [showAddForm, setShowAddForm] = useState(false)
  const [categoryName, setCategoryName] = useState('')
  const [error, setError] = useState('')

  const validateCategoryName = (name: string): boolean => {
    if (!name.trim()) {
      setError('Category name is required')
      return false
    }

    // Check for duplicate category names (case-insensitive)
    const isDuplicate = categories.some(
      cat => cat.name.toLowerCase() === name.trim().toLowerCase()
    )

    if (isDuplicate) {
      setError('A category with this name already exists')
      return false
    }

    return true
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (validateCategoryName(categoryName)) {
      onAddCategory(categoryName.trim())
      setCategoryName('')
      setError('')
      setShowAddForm(false)
    }
  }

  const handleCancel = () => {
    setCategoryName('')
    setError('')
    setShowAddForm(false)
  }

  const handleNameChange = (value: string) => {
    setCategoryName(value)
    if (error) {
      setError('')
    }
  }

  const customCategories = categories.filter(cat => cat.isCustom)
  const defaultCategories = categories.filter(cat => !cat.isCustom)

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Category Management</h2>
        {!showAddForm && (
          <button
            onClick={() => setShowAddForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm font-medium"
          >
            + Add Custom Category
          </button>
        )}
      </div>

      {/* Add Category Form */}
      {showAddForm && (
        <form onSubmit={handleSubmit} className="mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
          <h3 className="text-sm font-semibold mb-3">Add New Category</h3>
          
          <div className="flex flex-col gap-2 mb-3">
            <label htmlFor="categoryName" className="text-sm font-medium text-gray-700">
              Category Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="categoryName"
              value={categoryName}
              onChange={(e) => handleNameChange(e.target.value)}
              className={`px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                error ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., Pet Care, Hobbies"
              autoFocus
            />
            {error && (
              <span className="text-sm text-red-500">{error}</span>
            )}
          </div>

          <div className="flex gap-3">
            <button
              type="submit"
              disabled={isLoading}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
            >
              {isLoading ? 'Adding...' : 'Add Category'}
            </button>
            <button
              type="button"
              onClick={handleCancel}
              disabled={isLoading}
              className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-300 disabled:cursor-not-allowed text-sm"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Categories List */}
      <div className="space-y-6">
        {/* Default Categories */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Default Categories</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {defaultCategories.map((category) => (
              <div
                key={category.id}
                className="px-3 py-2 bg-gray-100 rounded-md text-sm text-gray-700"
              >
                {category.name}
              </div>
            ))}
          </div>
        </div>

        {/* Custom Categories */}
        {customCategories.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Custom Categories</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {customCategories.map((category) => (
                <div
                  key={category.id}
                  className="px-3 py-2 bg-blue-50 border border-blue-200 rounded-md text-sm text-blue-700 flex items-center justify-between"
                >
                  <span>{category.name}</span>
                  <span className="text-xs bg-blue-200 px-2 py-0.5 rounded">Custom</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default CategoryManager

import { useState, useEffect } from 'react'
import { budgetApi, categoryApi } from '../services/api'
import { Category } from '../types/expense'
import { BudgetLimit, BudgetStatus, CreateBudgetData } from '../types/budget'
import BudgetOverview from '../components/budgets/BudgetOverview'
import BudgetForm from '../components/budgets/BudgetForm'
import CategoryManager from '../components/budgets/CategoryManager'

const BudgetsPage = () => {
  const [budgets, setBudgets] = useState<BudgetLimit[]>([])
  const [budgetStatuses, setBudgetStatuses] = useState<BudgetStatus[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [isAddingCategory, setIsAddingCategory] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingBudget, setEditingBudget] = useState<BudgetLimit | null>(null)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      const [categoriesData, budgetsData, statusData] = await Promise.all([
        categoryApi.getCategories(),
        budgetApi.getBudgets(),
        budgetApi.getBudgetStatus()
      ])
      
      setCategories(categoriesData)
      setBudgets(budgetsData)
      setBudgetStatuses(statusData)
    } catch (error) {
      console.error('Failed to load budget data:', error)
      alert('Failed to load budget data. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const loadBudgets = async () => {
    try {
      const [budgetsData, statusData] = await Promise.all([
        budgetApi.getBudgets(),
        budgetApi.getBudgetStatus()
      ])
      
      setBudgets(budgetsData)
      setBudgetStatuses(statusData)
    } catch (error) {
      console.error('Failed to load budgets:', error)
    }
  }

  const handleSetBudget = () => {
    setEditingBudget(null)
    setShowForm(true)
  }

  const handleEditBudget = (categoryId: string) => {
    const budget = budgets.find(b => b.categoryId === categoryId)
    if (budget) {
      setEditingBudget(budget)
      setShowForm(true)
    }
  }

  const handleSubmitBudget = async (data: CreateBudgetData) => {
    setIsSaving(true)
    try {
      if (editingBudget) {
        await budgetApi.updateBudget(editingBudget.id, data)
      } else {
        await budgetApi.createBudget(data)
      }
      
      await loadBudgets()
      setShowForm(false)
      setEditingBudget(null)
    } catch (error) {
      console.error('Failed to save budget:', error)
      alert('Failed to save budget. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelForm = () => {
    setShowForm(false)
    setEditingBudget(null)
  }

  const handleAddCategory = async (name: string) => {
    setIsAddingCategory(true)
    try {
      await categoryApi.createCategory(name)
      const categoriesData = await categoryApi.getCategories()
      setCategories(categoriesData)
    } catch (error) {
      console.error('Failed to add category:', error)
      alert('Failed to add category. Please try again.')
    } finally {
      setIsAddingCategory(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Budget Management</h1>
          <p className="text-gray-600 mt-2">Set and track budget limits for your spending categories</p>
        </div>

        {/* Set Budget Button */}
        <div className="mb-6">
          <button
            onClick={handleSetBudget}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
          >
            + Set Budget Limit
          </button>
        </div>

        {/* Budget Form */}
        {showForm && (
          <div className="mb-6">
            <BudgetForm
              categories={categories}
              budget={editingBudget}
              onSubmit={handleSubmitBudget}
              onCancel={handleCancelForm}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Budget Overview */}
        <BudgetOverview
          budgetStatuses={budgetStatuses}
          onEdit={handleEditBudget}
          isLoading={isLoading}
        />

        {/* Category Manager */}
        <div className="mt-6">
          <CategoryManager
            categories={categories}
            onAddCategory={handleAddCategory}
            isLoading={isAddingCategory}
          />
        </div>
      </div>
    </div>
  )
}

export default BudgetsPage

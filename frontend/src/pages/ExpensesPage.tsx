import { useState, useEffect } from 'react'
import { expenseApi, categoryApi } from '../services/api'
import { Expense, Category, ExpenseFilters, CreateExpenseData } from '../types/expense'
import ExpenseList from '../components/expenses/ExpenseList'
import ExpenseForm from '../components/expenses/ExpenseForm'
import CategoryFilter from '../components/expenses/CategoryFilter'
import DateRangePicker from '../components/expenses/DateRangePicker'
import SpouseFilter from '../components/expenses/SpouseFilter'
import DeleteConfirmationDialog from '../components/expenses/DeleteConfirmationDialog'
import ExpenseSummary from '../components/expenses/ExpenseSummary'

interface User {
  id: string
  name: string
}

const ExpensesPage = () => {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingExpense, setEditingExpense] = useState<Expense | null>(null)
  const [deleteConfirmation, setDeleteConfirmation] = useState<{
    isOpen: boolean
    expenseId: string
    expenseName: string
  }>({
    isOpen: false,
    expenseId: '',
    expenseName: ''
  })

  // Filters
  const [filters, setFilters] = useState<ExpenseFilters>({
    categoryId: '',
    startDate: '',
    endDate: '',
    userId: ''
  })

  const [totalAmount, setTotalAmount] = useState(0)

  useEffect(() => {
    loadInitialData()
  }, [])

  useEffect(() => {
    loadExpenses()
  }, [filters])

  useEffect(() => {
    // Recalculate total when expenses change
    const total = expenses.reduce((sum, expense) => sum + expense.amount, 0)
    setTotalAmount(total)
  }, [expenses])

  const loadInitialData = async () => {
    try {
      const [categoriesData, expensesData] = await Promise.all([
        categoryApi.getCategories(),
        expenseApi.getExpenses()
      ])
      
      setCategories(categoriesData)
      setExpenses(expensesData)
      
      // Extract unique users from expenses
      const uniqueUsers = Array.from(
        new Map(expensesData.map(exp => [exp.userId, { id: exp.userId, name: exp.userName }])).values()
      )
      setUsers(uniqueUsers)
    } catch (error) {
      console.error('Failed to load initial data:', error)
      alert('Failed to load data. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const loadExpenses = async () => {
    try {
      const data = await expenseApi.getExpenses(filters)
      setExpenses(data)
      
      // Update users list if needed
      const uniqueUsers = Array.from(
        new Map(data.map(exp => [exp.userId, { id: exp.userId, name: exp.userName }])).values()
      )
      setUsers(uniqueUsers)
    } catch (error) {
      console.error('Failed to load expenses:', error)
    }
  }

  const handleAddExpense = () => {
    setEditingExpense(null)
    setShowForm(true)
  }

  const handleEditExpense = (expense: Expense) => {
    setEditingExpense(expense)
    setShowForm(true)
  }

  const handleSubmitExpense = async (data: CreateExpenseData) => {
    setIsSaving(true)
    try {
      if (editingExpense) {
        await expenseApi.updateExpense(editingExpense.id, data)
      } else {
        await expenseApi.createExpense(data)
      }
      
      await loadExpenses()
      setShowForm(false)
      setEditingExpense(null)
    } catch (error) {
      console.error('Failed to save expense:', error)
      alert('Failed to save expense. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleDeleteClick = (expenseId: string) => {
    const expense = expenses.find(exp => exp.id === expenseId)
    if (expense) {
      setDeleteConfirmation({
        isOpen: true,
        expenseId: expense.id,
        expenseName: `${expense.categoryName} - $${expense.amount.toFixed(2)}`
      })
    }
  }

  const handleConfirmDelete = async () => {
    setIsDeleting(true)
    try {
      await expenseApi.deleteExpense(deleteConfirmation.expenseId)
      await loadExpenses()
      setDeleteConfirmation({ isOpen: false, expenseId: '', expenseName: '' })
    } catch (error) {
      console.error('Failed to delete expense:', error)
      alert('Failed to delete expense. Please try again.')
    } finally {
      setIsDeleting(false)
    }
  }

  const handleCancelDelete = () => {
    setDeleteConfirmation({ isOpen: false, expenseId: '', expenseName: '' })
  }

  const handleCancelForm = () => {
    setShowForm(false)
    setEditingExpense(null)
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Expense Management</h1>
          <p className="text-gray-600 mt-2">Track and manage your household expenses</p>
        </div>

        {/* Filters Section */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h2 className="text-lg font-semibold mb-4">Filters</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <CategoryFilter
              categories={categories}
              selectedCategoryId={filters.categoryId || ''}
              onCategoryChange={(categoryId) => setFilters(prev => ({ ...prev, categoryId }))}
            />
            
            <SpouseFilter
              users={users}
              selectedUserId={filters.userId || ''}
              onUserChange={(userId) => setFilters(prev => ({ ...prev, userId }))}
            />
            
            <DateRangePicker
              startDate={filters.startDate || ''}
              endDate={filters.endDate || ''}
              onStartDateChange={(startDate) => setFilters(prev => ({ ...prev, startDate }))}
              onEndDateChange={(endDate) => setFilters(prev => ({ ...prev, endDate }))}
            />
          </div>
          
          <div className="mt-4 flex justify-between items-center">
            <button
              onClick={() => setFilters({ categoryId: '', startDate: '', endDate: '', userId: '' })}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              Clear Filters
            </button>
            <div className="text-lg font-semibold">
              Total: {formatCurrency(totalAmount)}
            </div>
          </div>
        </div>

        {/* Add Expense Button */}
        <div className="mb-6">
          <button
            onClick={handleAddExpense}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
          >
            + Add Expense
          </button>
        </div>

        {/* Expense Form */}
        {showForm && (
          <div className="mb-6">
            <ExpenseForm
              categories={categories}
              expense={editingExpense}
              onSubmit={handleSubmitExpense}
              onCancel={handleCancelForm}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Expense Summary */}
        <div className="mb-6">
          <ExpenseSummary filters={filters} />
        </div>

        {/* Expense List */}
        <ExpenseList
          expenses={expenses}
          onEdit={handleEditExpense}
          onDelete={handleDeleteClick}
          isLoading={isLoading}
        />

        {/* Delete Confirmation Dialog */}
        <DeleteConfirmationDialog
          isOpen={deleteConfirmation.isOpen}
          expenseName={deleteConfirmation.expenseName}
          onConfirm={handleConfirmDelete}
          onCancel={handleCancelDelete}
          isDeleting={isDeleting}
        />
      </div>
    </div>
  )
}

export default ExpensesPage

import { useState, useEffect } from 'react'
import { incomeApi } from '../services/api'
import { MonthlyIncome, CreateIncomeData } from '../types/income'
import IncomeList from '../components/income/IncomeList'
import MonthlyIncomeForm from '../components/income/MonthlyIncomeForm'

const IncomePage = () => {
  const [incomes, setIncomes] = useState<MonthlyIncome[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingIncome, setEditingIncome] = useState<MonthlyIncome | null>(null)

  useEffect(() => {
    loadIncomes()
  }, [])

  const loadIncomes = async () => {
    try {
      const data = await incomeApi.getMonthlyIncomes()
      setIncomes(data)
    } catch (error) {
      console.error('Failed to load monthly incomes:', error)
      alert('Failed to load monthly incomes. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSetIncome = () => {
    setEditingIncome(null)
    setShowForm(true)
  }

  const handleEditIncome = (income: MonthlyIncome) => {
    setEditingIncome(income)
    setShowForm(true)
  }

  const handleSubmitIncome = async (data: CreateIncomeData) => {
    setIsSaving(true)
    try {
      if (editingIncome) {
        await incomeApi.updateMonthlyIncome(editingIncome.id, data)
      } else {
        await incomeApi.createMonthlyIncome(data)
      }
      
      await loadIncomes()
      setShowForm(false)
      setEditingIncome(null)
    } catch (error: any) {
      console.error('Failed to save monthly income:', error)
      
      // Handle conflict error (duplicate month/year)
      if (error.response?.status === 409) {
        alert('Income for this month and year already exists. Please edit the existing record instead.')
      } else {
        alert('Failed to save monthly income. Please try again.')
      }
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelForm = () => {
    setShowForm(false)
    setEditingIncome(null)
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  // Get current month income
  const currentDate = new Date()
  const currentMonthIncome = incomes.find(
    income => income.month === currentDate.getMonth() + 1 && income.year === currentDate.getFullYear()
  )

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Monthly Income</h1>
          <p className="text-gray-600 mt-2">Track your household gross income by month</p>
        </div>

        {/* Current Month Income Card */}
        {currentMonthIncome && (
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 mb-6 text-white">
            <h3 className="text-sm font-medium mb-2 opacity-90">Current Month Income</h3>
            <p className="text-4xl font-bold">{formatCurrency(currentMonthIncome.amount)}</p>
            <p className="text-sm mt-2 opacity-90">
              {new Date(currentDate.getFullYear(), currentDate.getMonth()).toLocaleDateString('en-US', {
                month: 'long',
                year: 'numeric'
              })}
            </p>
          </div>
        )}

        {!currentMonthIncome && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <p className="text-yellow-800 text-sm">
              No income set for the current month. Set your income to see it reflected in the dashboard.
            </p>
          </div>
        )}

        {/* Set Income Button */}
        <div className="mb-6">
          <button
            onClick={handleSetIncome}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
          >
            + Set Monthly Income
          </button>
        </div>

        {/* Income Form */}
        {showForm && (
          <div className="mb-6">
            <MonthlyIncomeForm
              income={editingIncome}
              onSubmit={handleSubmitIncome}
              onCancel={handleCancelForm}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Income List */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Income History</h2>
          <IncomeList
            incomes={incomes}
            onEdit={handleEditIncome}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  )
}

export default IncomePage

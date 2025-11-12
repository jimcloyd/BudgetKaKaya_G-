import { useState, useEffect } from 'react'
import { savingsApi } from '../services/api'
import { SavingsGoal, CreateSavingsGoalData, CreateContributionData } from '../types/savings'
import SavingsGoalList from '../components/savings/SavingsGoalList'
import SavingsGoalForm from '../components/savings/SavingsGoalForm'
import ContributionForm from '../components/savings/ContributionForm'

const SavingsPage = () => {
  const [goals, setGoals] = useState<SavingsGoal[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [showGoalForm, setShowGoalForm] = useState(false)
  const [editingGoal, setEditingGoal] = useState<SavingsGoal | null>(null)
  const [showContributionForm, setShowContributionForm] = useState(false)
  const [selectedGoal, setSelectedGoal] = useState<SavingsGoal | null>(null)

  useEffect(() => {
    loadGoals()
  }, [])

  const loadGoals = async () => {
    try {
      const data = await savingsApi.getSavingsGoals()
      setGoals(data)
    } catch (error) {
      console.error('Failed to load savings goals:', error)
      alert('Failed to load savings goals. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddGoal = () => {
    setEditingGoal(null)
    setShowGoalForm(true)
  }

  const handleEditGoal = (goal: SavingsGoal) => {
    setEditingGoal(goal)
    setShowGoalForm(true)
  }

  const handleSubmitGoal = async (data: CreateSavingsGoalData) => {
    setIsSaving(true)
    try {
      if (editingGoal) {
        await savingsApi.updateSavingsGoal(editingGoal.id, data)
      } else {
        await savingsApi.createSavingsGoal(data)
      }
      
      await loadGoals()
      setShowGoalForm(false)
      setEditingGoal(null)
    } catch (error) {
      console.error('Failed to save savings goal:', error)
      alert('Failed to save savings goal. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelGoalForm = () => {
    setShowGoalForm(false)
    setEditingGoal(null)
  }

  const handleAddContribution = (goal: SavingsGoal) => {
    setSelectedGoal(goal)
    setShowContributionForm(true)
  }

  const handleSubmitContribution = async (data: CreateContributionData) => {
    if (!selectedGoal) return

    setIsSaving(true)
    try {
      await savingsApi.addContribution(selectedGoal.id, data)
      
      await loadGoals()
      setShowContributionForm(false)
      setSelectedGoal(null)
    } catch (error) {
      console.error('Failed to add contribution:', error)
      alert('Failed to add contribution. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelContribution = () => {
    setShowContributionForm(false)
    setSelectedGoal(null)
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const totalSaved = goals.reduce((sum, goal) => sum + goal.currentBalance, 0)
  const totalTarget = goals.reduce((sum, goal) => sum + goal.targetAmount, 0)
  const totalRemaining = goals.reduce((sum, goal) => sum + goal.remainingAmount, 0)

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Savings Goals</h1>
          <p className="text-gray-600 mt-2">Track your progress toward financial goals</p>
        </div>

        {/* Summary Cards */}
        {goals.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Saved</h3>
              <p className="text-2xl font-bold text-green-600">{formatCurrency(totalSaved)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Target</h3>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalTarget)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Remaining</h3>
              <p className="text-2xl font-bold text-orange-600">{formatCurrency(totalRemaining)}</p>
            </div>
          </div>
        )}

        {/* Add Goal Button */}
        <div className="mb-6">
          <button
            onClick={handleAddGoal}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
          >
            + Add Savings Goal
          </button>
        </div>

        {/* Goal Form */}
        {showGoalForm && (
          <div className="mb-6">
            <SavingsGoalForm
              goal={editingGoal}
              onSubmit={handleSubmitGoal}
              onCancel={handleCancelGoalForm}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Contribution Form */}
        {showContributionForm && selectedGoal && (
          <div className="mb-6">
            <ContributionForm
              goalName={selectedGoal.name}
              onSubmit={handleSubmitContribution}
              onCancel={handleCancelContribution}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Goals List */}
        <SavingsGoalList
          goals={goals}
          onEdit={handleEditGoal}
          onAddContribution={handleAddContribution}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}

export default SavingsPage

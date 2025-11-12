import { SavingsGoal } from '../../types/savings'

interface SavingsGoalListProps {
  goals: SavingsGoal[]
  onEdit: (goal: SavingsGoal) => void
  onAddContribution: (goal: SavingsGoal) => void
  isLoading: boolean
}

const SavingsGoalList = ({ goals, onEdit, onAddContribution, isLoading }: SavingsGoalListProps) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getProgressColor = (percentage: number) => {
    if (percentage >= 100) return 'bg-green-500'
    if (percentage >= 75) return 'bg-blue-500'
    if (percentage >= 50) return 'bg-yellow-500'
    return 'bg-orange-500'
  }

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-center items-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    )
  }

  if (goals.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-center text-gray-500">No savings goals added yet</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {goals.map((goal) => {
        const isCompleted = goal.percentageCompleted >= 100
        
        return (
          <div key={goal.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">{goal.name}</h3>
                {goal.targetDate && (
                  <p className="text-sm text-gray-600">
                    Target: {formatDate(goal.targetDate)}
                  </p>
                )}
              </div>
              {isCompleted && (
                <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
                  Completed
                </span>
              )}
            </div>

            <div className="space-y-3 mb-4">
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Current Balance</span>
                  <span className="font-semibold text-gray-900">
                    {formatCurrency(goal.currentBalance)}
                  </span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Target Amount</span>
                  <span className="font-semibold text-gray-900">
                    {formatCurrency(goal.targetAmount)}
                  </span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Remaining</span>
                  <span className="font-semibold text-orange-600">
                    {formatCurrency(goal.remainingAmount)}
                  </span>
                </div>
              </div>

              {goal.suggestedMonthlyContribution && (
                <div className="bg-blue-50 border border-blue-200 rounded-md p-2">
                  <p className="text-xs text-gray-700">
                    Suggested monthly: <span className="font-semibold text-blue-700">
                      {formatCurrency(goal.suggestedMonthlyContribution)}
                    </span>
                  </p>
                </div>
              )}
            </div>

            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Progress</span>
                <span className="font-semibold text-gray-900">
                  {goal.percentageCompleted.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all ${getProgressColor(goal.percentageCompleted)}`}
                  style={{ width: `${Math.min(goal.percentageCompleted, 100)}%` }}
                ></div>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => onAddContribution(goal)}
                className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 text-sm font-medium"
              >
                Add Contribution
              </button>
              <button
                onClick={() => onEdit(goal)}
                className="px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 text-sm font-medium text-gray-700"
              >
                Edit
              </button>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default SavingsGoalList

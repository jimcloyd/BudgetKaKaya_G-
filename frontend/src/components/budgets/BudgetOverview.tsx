import { BudgetStatus } from '../../types/budget'

interface BudgetOverviewProps {
  budgetStatuses: BudgetStatus[]
  onEdit: (categoryId: string) => void
  isLoading?: boolean
}

const BudgetOverview = ({ budgetStatuses, onEdit, isLoading }: BudgetOverviewProps) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'exceeded':
        return 'bg-red-500'
      case 'warning':
        return 'bg-yellow-500'
      default:
        return 'bg-green-500'
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'exceeded':
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800">
            Over Budget
          </span>
        )
      case 'warning':
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
            Warning (80%+)
          </span>
        )
      default:
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
            On Track
          </span>
        )
    }
  }

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  if (budgetStatuses.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-500 text-center">No budget limits set. Click "Set Budget Limit" to get started.</p>
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Budget Overview</h2>
      
      <div className="space-y-4">
        {budgetStatuses.map((budget) => (
          <div key={budget.categoryId} className="border border-gray-200 rounded-lg p-4">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-semibold text-lg">{budget.categoryName}</h3>
                <p className="text-sm text-gray-500 capitalize">{budget.period} Budget</p>
              </div>
              <div className="flex items-center gap-2">
                {getStatusBadge(budget.status)}
                <button
                  onClick={() => onEdit(budget.categoryId)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Edit
                </button>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Spent</span>
                <span className="font-medium">{formatCurrency(budget.spentAmount)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Budget</span>
                <span className="font-medium">{formatCurrency(budget.budgetAmount)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Remaining</span>
                <span className={`font-medium ${budget.remainingAmount < 0 ? 'text-red-600' : 'text-green-600'}`}>
                  {formatCurrency(budget.remainingAmount)}
                </span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mt-3">
              <div className="flex justify-between text-xs text-gray-600 mb-1">
                <span>{budget.percentage.toFixed(1)}% used</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${getStatusColor(budget.status)}`}
                  style={{ width: `${Math.min(budget.percentage, 100)}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default BudgetOverview

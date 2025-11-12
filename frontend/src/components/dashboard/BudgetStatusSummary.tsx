import { BudgetStatus } from '../../types/dashboard'

interface BudgetStatusSummaryProps {
  budgetStatus: BudgetStatus[]
}

const BudgetStatusSummary = ({ budgetStatus }: BudgetStatusSummaryProps) => {
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

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case 'exceeded':
        return '🔴'
      case 'warning':
        return '⚠️'
      default:
        return '✅'
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Budget Status</h3>
      
      {budgetStatus.length === 0 ? (
        <p className="text-gray-500 text-sm">No budget limits set</p>
      ) : (
        <div className="space-y-4">
          {budgetStatus.map((budget) => (
            <div key={budget.categoryId} className="border-b pb-4 last:border-b-0">
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{getStatusIndicator(budget.status)}</span>
                  <span className="font-medium">{budget.categoryName}</span>
                </div>
                <span className="text-sm text-gray-600">
                  {formatCurrency(budget.spent)} / {formatCurrency(budget.budgetLimit)}
                </span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className={`h-2.5 rounded-full ${getStatusColor(budget.status)}`}
                  style={{ width: `${Math.min(budget.percentage, 100)}%` }}
                ></div>
              </div>
              
              <div className="flex justify-between items-center mt-2">
                <span className="text-xs text-gray-500">
                  {budget.percentage.toFixed(1)}% used
                </span>
                <span className={`text-xs font-medium ${budget.remaining < 0 ? 'text-red-600' : 'text-gray-700'}`}>
                  {budget.remaining < 0 ? 'Over by ' : 'Remaining: '}
                  {formatCurrency(Math.abs(budget.remaining))}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default BudgetStatusSummary

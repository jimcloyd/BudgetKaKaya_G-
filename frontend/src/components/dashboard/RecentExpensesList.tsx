import { Expense } from '../../types/dashboard'

interface RecentExpensesListProps {
  expenses: Expense[]
}

const RecentExpensesList = ({ expenses }: RecentExpensesListProps) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    }).format(date)
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Recent Expenses</h3>
      
      {expenses.length === 0 ? (
        <p className="text-gray-500 text-sm">No expenses recorded yet</p>
      ) : (
        <div className="space-y-3">
          {expenses.map((expense) => (
            <div key={expense.id} className="flex justify-between items-start border-b pb-3 last:border-b-0">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-900">{expense.description}</span>
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                    {expense.categoryName}
                  </span>
                </div>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs text-gray-500">{formatDate(expense.date)}</span>
                  <span className="text-xs text-gray-400">•</span>
                  <span className="text-xs text-gray-500">by {expense.userName}</span>
                </div>
              </div>
              <span className="font-semibold text-gray-900">{formatCurrency(expense.amount)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default RecentExpensesList

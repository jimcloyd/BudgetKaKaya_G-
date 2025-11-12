import { CreditCard } from '../../types/creditCard'

interface CreditCardListProps {
  creditCards: CreditCard[]
  onEdit: (card: CreditCard) => void
  onAddTransaction: (card: CreditCard) => void
  isLoading: boolean
}

const CreditCardList = ({ creditCards, onEdit, onAddTransaction, isLoading }: CreditCardListProps) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const getUtilizationPercentage = (balance: number, limit: number) => {
    return limit > 0 ? (balance / limit) * 100 : 0
  }

  const getUtilizationColor = (percentage: number) => {
    if (percentage >= 90) return 'text-red-600'
    if (percentage >= 70) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getProgressBarColor = (percentage: number) => {
    if (percentage >= 90) return 'bg-red-500'
    if (percentage >= 70) return 'bg-yellow-500'
    return 'bg-blue-500'
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

  if (creditCards.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-center text-gray-500">No credit cards added yet</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {creditCards.map((card) => {
        const utilization = getUtilizationPercentage(card.currentBalance, card.creditLimit)
        
        return (
          <div key={card.id} className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
            <div className="mb-4">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-semibold text-gray-900">{card.name}</h3>
                <button
                  onClick={() => onEdit(card)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  Edit
                </button>
              </div>
              <button
                onClick={() => onAddTransaction(card)}
                className="w-full bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 text-sm font-medium"
              >
                Record Transaction
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Current Balance</span>
                  <span className="font-semibold text-gray-900">
                    {formatCurrency(card.currentBalance)}
                  </span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Credit Limit</span>
                  <span className="font-semibold text-gray-900">
                    {formatCurrency(card.creditLimit)}
                  </span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Available Credit</span>
                  <span className="font-semibold text-green-600">
                    {formatCurrency(card.availableCredit)}
                  </span>
                </div>
              </div>

              <div className="pt-2">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Utilization</span>
                  <span className={`font-semibold ${getUtilizationColor(utilization)}`}>
                    {utilization.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${getProgressBarColor(utilization)}`}
                    style={{ width: `${Math.min(utilization, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default CreditCardList

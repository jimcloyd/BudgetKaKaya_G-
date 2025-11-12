import { Installment } from '../../types/installment'

interface InstallmentListProps {
  installments: Installment[]
  onMarkPaid: (installment: Installment) => void
  isLoading: boolean
}

const InstallmentList = ({ installments, onMarkPaid, isLoading }: InstallmentListProps) => {
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

  const getProgressPercentage = (paid: number, total: number) => {
    return total > 0 ? (paid / total) * 100 : 0
  }

  const isPaymentDue = (nextPaymentDate: string | null) => {
    if (!nextPaymentDate) return false
    const today = new Date()
    const paymentDate = new Date(nextPaymentDate)
    return paymentDate <= today
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

  if (installments.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-center text-gray-500">No installments added yet</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {installments.map((installment) => {
        const progress = getProgressPercentage(installment.paidPayments, installment.numberOfPayments)
        const isCompleted = installment.paidPayments >= installment.numberOfPayments
        const isDue = isPaymentDue(installment.nextPaymentDate)
        
        return (
          <div key={installment.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {installment.description}
                </h3>
                <p className="text-sm text-gray-600">
                  Added by {installment.userName} on {formatDate(installment.createdAt)}
                </p>
              </div>
              {isCompleted && (
                <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
                  Completed
                </span>
              )}
              {!isCompleted && isDue && (
                <span className="bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded">
                  Payment Due
                </span>
              )}
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <p className="text-sm text-gray-600">Total Amount</p>
                <p className="text-lg font-semibold text-gray-900">
                  {formatCurrency(installment.totalAmount)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Monthly Payment</p>
                <p className="text-lg font-semibold text-gray-900">
                  {formatCurrency(installment.monthlyPayment)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Remaining Balance</p>
                <p className="text-lg font-semibold text-gray-900">
                  {formatCurrency(installment.remainingBalance)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Next Payment</p>
                <p className="text-lg font-semibold text-gray-900">
                  {installment.nextPaymentDate ? formatDate(installment.nextPaymentDate) : 'N/A'}
                </p>
              </div>
            </div>

            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">
                  Progress: {installment.paidPayments} of {installment.numberOfPayments} payments
                </span>
                <span className="font-semibold text-gray-900">
                  {progress.toFixed(0)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all ${
                    isCompleted ? 'bg-green-500' : 'bg-blue-500'
                  }`}
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>

            {!isCompleted && (
              <button
                onClick={() => onMarkPaid(installment)}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 font-medium"
              >
                Mark Payment as Paid
              </button>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default InstallmentList

import { Installment } from '../../types/dashboard'

interface UpcomingInstallmentsProps {
  installments: Installment[]
}

const UpcomingInstallments = ({ installments }: UpcomingInstallmentsProps) => {
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
      <h3 className="text-lg font-semibold mb-4">Upcoming Installments</h3>
      
      {installments.length === 0 ? (
        <p className="text-gray-500 text-sm">No upcoming installment payments</p>
      ) : (
        <div className="space-y-3">
          {installments.map((installment) => (
            <div key={installment.id} className="border-b pb-3 last:border-b-0">
              <div className="flex justify-between items-start mb-2">
                <span className="font-medium text-gray-900">{installment.description}</span>
                <span className="font-semibold text-gray-900">
                  {formatCurrency(installment.monthlyPayment)}
                </span>
              </div>
              
              <div className="flex justify-between items-center text-xs text-gray-500">
                <span>Due: {formatDate(installment.nextPaymentDate)}</span>
                <span>{installment.remainingPayments} payments left</span>
              </div>
              
              <div className="mt-2 text-xs text-gray-600">
                Remaining balance: {formatCurrency(installment.remainingBalance)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default UpcomingInstallments

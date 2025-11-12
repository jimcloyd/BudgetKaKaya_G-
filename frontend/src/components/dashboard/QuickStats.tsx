interface QuickStatsProps {
  totalSpent: number
  monthlyIncome: number
  netIncome: number
  remaining: number
}

const QuickStats = ({ totalSpent, monthlyIncome, netIncome, remaining }: QuickStatsProps) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-sm font-medium text-gray-500 mb-2">Total Spent</h3>
        <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalSpent)}</p>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-sm font-medium text-gray-500 mb-2">Monthly Income</h3>
        <p className="text-2xl font-bold text-gray-900">{formatCurrency(monthlyIncome)}</p>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-sm font-medium text-gray-500 mb-2">Net Income</h3>
        <p className={`text-2xl font-bold ${netIncome < 0 ? 'text-red-600' : 'text-green-600'}`}>
          {formatCurrency(netIncome)}
        </p>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-sm font-medium text-gray-500 mb-2">Remaining Budget</h3>
        <p className="text-2xl font-bold text-gray-900">{formatCurrency(remaining)}</p>
      </div>
    </div>
  )
}

export default QuickStats

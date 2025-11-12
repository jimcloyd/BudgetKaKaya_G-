import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

interface IncomeVsExpensesChartProps {
  monthlyIncome: number
  totalExpenses: number
  monthOverMonth: {
    currentMonth: number
    previousMonth: number
    percentageChange: number
  }
}

const IncomeVsExpensesChart = ({ monthlyIncome, totalExpenses, monthOverMonth }: IncomeVsExpensesChartProps) => {
  const data = {
    labels: ['Current Month'],
    datasets: [
      {
        label: 'Income',
        data: [monthlyIncome],
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 1
      },
      {
        label: 'Expenses',
        data: [totalExpenses],
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 1
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const
      },
      title: {
        display: true,
        text: 'Income vs Expenses'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value: number | string) {
            return '$' + value.toLocaleString()
          }
        }
      }
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const netIncome = monthlyIncome - totalExpenses

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="h-64 mb-4">
        <Bar data={data} options={options} />
      </div>
      
      <div className="mb-4 p-4 bg-gray-50 rounded">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Net Income:</span>
          <span className={`text-lg font-bold ${netIncome < 0 ? 'text-red-600' : 'text-green-600'}`}>
            {formatCurrency(netIncome)}
          </span>
        </div>
        {netIncome < 0 && (
          <p className="text-xs text-red-600 mt-2">
            ⚠️ You are spending more than your income this month
          </p>
        )}
      </div>
      
      {monthOverMonth.previousMonth > 0 && (
        <div className="mt-4 p-4 bg-gray-50 rounded">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Month-over-Month Comparison</h4>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Previous Month:</span>
            <span className="text-sm font-semibold">{formatCurrency(monthOverMonth.previousMonth)}</span>
          </div>
          <div className="flex justify-between items-center mt-1">
            <span className="text-sm text-gray-600">Current Month:</span>
            <span className="text-sm font-semibold">{formatCurrency(monthOverMonth.currentMonth)}</span>
          </div>
          <div className="flex justify-between items-center mt-1">
            <span className="text-sm text-gray-600">Change:</span>
            <span className={`text-sm font-semibold ${monthOverMonth.percentageChange > 0 ? 'text-red-600' : 'text-green-600'}`}>
              {monthOverMonth.percentageChange > 0 ? '+' : ''}{monthOverMonth.percentageChange.toFixed(1)}%
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default IncomeVsExpensesChart

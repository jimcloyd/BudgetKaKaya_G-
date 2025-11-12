import { useEffect, useState } from 'react'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'react-chartjs-2'
import { ExpenseSummary as ExpenseSummaryType, ExpenseFilters } from '../../types/expense'
import { expenseApi } from '../../services/api'

ChartJS.register(ArcElement, Tooltip, Legend)

interface ExpenseSummaryProps {
  filters?: ExpenseFilters
}

const ExpenseSummary = ({ filters }: ExpenseSummaryProps) => {
  const [summary, setSummary] = useState<ExpenseSummaryType[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [totalAmount, setTotalAmount] = useState(0)

  useEffect(() => {
    loadSummary()
  }, [filters])

  const loadSummary = async () => {
    setIsLoading(true)
    try {
      const data = await expenseApi.getExpenseSummary(filters)
      setSummary(data)
      
      const total = data.reduce((sum, item) => sum + item.totalAmount, 0)
      setTotalAmount(total)
    } catch (error) {
      console.error('Failed to load expense summary:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const generateColors = (count: number) => {
    const colors = [
      '#3B82F6', // blue
      '#10B981', // green
      '#F59E0B', // amber
      '#EF4444', // red
      '#8B5CF6', // purple
      '#EC4899', // pink
      '#14B8A6', // teal
      '#F97316', // orange
      '#6366F1', // indigo
      '#84CC16', // lime
    ]
    
    return colors.slice(0, count)
  }

  const chartData = {
    labels: summary.map(item => item.categoryName),
    datasets: [
      {
        data: summary.map(item => item.totalAmount),
        backgroundColor: generateColors(summary.length),
        borderColor: '#ffffff',
        borderWidth: 2,
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            const label = context.label || ''
            const value = context.parsed || 0
            const percentage = ((value / totalAmount) * 100).toFixed(1)
            return `${label}: ${formatCurrency(value)} (${percentage}%)`
          }
        }
      }
    },
  }

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    )
  }

  if (summary.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Spending Summary</h3>
        <p className="text-center text-gray-500">No expenses to summarize</p>
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-6">Spending Summary by Category</h3>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart */}
        <div className="flex items-center justify-center">
          <div className="w-full h-64">
            <Pie data={chartData} options={chartOptions} />
          </div>
        </div>

        {/* Category List */}
        <div className="space-y-3">
          {summary.map((item, index) => (
            <div key={item.categoryId} className="border-b pb-3 last:border-b-0">
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded"
                    style={{ backgroundColor: generateColors(summary.length)[index] }}
                  ></div>
                  <span className="font-medium">{item.categoryName}</span>
                </div>
                <span className="font-semibold">{formatCurrency(item.totalAmount)}</span>
              </div>
              
              <div className="flex justify-between items-center text-sm text-gray-600">
                <span>{item.expenseCount} expense{item.expenseCount !== 1 ? 's' : ''}</span>
                <span className="font-medium">{item.percentage.toFixed(1)}% of total</span>
              </div>
              
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="h-2 rounded-full"
                  style={{ 
                    width: `${item.percentage}%`,
                    backgroundColor: generateColors(summary.length)[index]
                  }}
                ></div>
              </div>
            </div>
          ))}
          
          <div className="pt-3 border-t-2 border-gray-300">
            <div className="flex justify-between items-center">
              <span className="font-bold text-lg">Total</span>
              <span className="font-bold text-lg">{formatCurrency(totalAmount)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExpenseSummary

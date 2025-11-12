import { useAuth } from '../contexts/AuthContext'
import { useState, useEffect } from 'react'
import { dashboardApi } from '../services/api'
import { DashboardData } from '../types/dashboard'
import QuickStats from '../components/dashboard/QuickStats'
import IncomeVsExpensesChart from '../components/dashboard/IncomeVsExpensesChart'
import BudgetStatusSummary from '../components/dashboard/BudgetStatusSummary'
import RecentExpensesList from '../components/dashboard/RecentExpensesList'
import UpcomingInstallments from '../components/dashboard/UpcomingInstallments'
import Footer from '../components/Footer'

const Dashboard = () => {
  const { user, logout } = useAuth()
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await dashboardApi.getDashboardData()
      setDashboardData(data)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load dashboard data')
      console.error('Error fetching dashboard data:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // const calculateTotalBudget = () => {
  //   if (!dashboardData) return 0
  //   return dashboardData.budgetStatus.reduce((sum, budget) => sum + budget.budgetLimit, 0)
  // }

  const calculateRemainingBudget = () => {
    if (!dashboardData) return 0
    return dashboardData.budgetStatus.reduce((sum, budget) => sum + budget.remaining, 0)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Family Budget Tracker</h1>
          <div className="flex items-center gap-4">
            <span>Welcome, {user?.name}</span>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-semibold mb-6">Dashboard</h2>
        
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}
        
        {!isLoading && !error && dashboardData && (
          <>
            <QuickStats
              totalSpent={dashboardData.totalExpenses}
              monthlyIncome={dashboardData.monthlyIncome}
              netIncome={dashboardData.netIncome}
              remaining={calculateRemainingBudget()}
            />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <IncomeVsExpensesChart
                monthlyIncome={dashboardData.monthlyIncome}
                totalExpenses={dashboardData.totalExpenses}
                monthOverMonth={dashboardData.monthOverMonthComparison}
              />
              
              <BudgetStatusSummary budgetStatus={dashboardData.budgetStatus} />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <RecentExpensesList expenses={dashboardData.recentExpenses} />
              <UpcomingInstallments installments={dashboardData.upcomingInstallments} />
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  )
}

export default Dashboard

export interface DashboardData {
  totalExpenses: number
  monthlyIncome: number
  netIncome: number
  budgetStatus: BudgetStatus[]
  recentExpenses: Expense[]
  upcomingInstallments: Installment[]
  monthOverMonthComparison: {
    currentMonth: number
    previousMonth: number
    percentageChange: number
  }
}

export interface BudgetStatus {
  categoryId: string
  categoryName: string
  budgetLimit: number
  spent: number
  remaining: number
  percentage: number
  status: 'ok' | 'warning' | 'exceeded'
}

export interface Expense {
  id: string
  amount: number
  categoryName: string
  date: string
  description: string
  userName: string
}

export interface Installment {
  id: string
  description: string
  monthlyPayment: number
  nextPaymentDate: string
  remainingBalance: number
  remainingPayments: number
}

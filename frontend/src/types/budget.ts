export interface BudgetLimit {
  id: string
  categoryId: string
  categoryName: string
  amount: number
  period: 'weekly' | 'monthly'
  createdAt: string
  updatedAt: string
}

export interface BudgetStatus {
  categoryId: string
  categoryName: string
  budgetAmount: number
  spentAmount: number
  remainingAmount: number
  percentage: number
  period: 'weekly' | 'monthly'
  status: 'normal' | 'warning' | 'exceeded'
}

export interface CreateBudgetData {
  categoryId: string
  amount: number
  period: 'weekly' | 'monthly'
}

export interface UpdateBudgetData {
  amount?: number
  period?: 'weekly' | 'monthly'
}

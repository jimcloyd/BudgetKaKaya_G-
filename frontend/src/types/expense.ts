export interface Expense {
  id: string
  amount: number
  categoryId: string
  categoryName: string
  date: string
  description: string
  userId: string
  userName: string
  createdAt: string
  updatedAt: string
}

export interface Category {
  id: string
  name: string
  isCustom: boolean
}

export interface ExpenseFilters {
  categoryId?: string
  startDate?: string
  endDate?: string
  userId?: string
}

export interface ExpenseSummary {
  categoryId: string
  categoryName: string
  totalAmount: number
  percentage: number
  expenseCount: number
}

export interface CreateExpenseData {
  amount: number
  categoryId: string
  date: string
  description: string
}

export interface UpdateExpenseData {
  amount?: number
  categoryId?: string
  date?: string
  description?: string
}

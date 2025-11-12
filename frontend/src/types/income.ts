export interface MonthlyIncome {
  id: string
  month: number
  year: number
  amount: number
  createdAt: string
  updatedAt: string
}

export interface CreateIncomeData {
  month: number
  year: number
  amount: number
}

export interface UpdateIncomeData {
  month?: number
  year?: number
  amount?: number
}

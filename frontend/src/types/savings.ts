export interface SavingsGoal {
  id: string
  name: string
  targetAmount: number
  currentBalance: number
  targetDate: string | null
  percentageCompleted: number
  remainingAmount: number
  suggestedMonthlyContribution: number | null
  createdAt: string
  updatedAt: string
}

export interface CreateSavingsGoalData {
  name: string
  targetAmount: number
  targetDate?: string
}

export interface UpdateSavingsGoalData {
  name?: string
  targetAmount?: number
  targetDate?: string | null
}

export interface SavingsContribution {
  id: string
  amount: number
  date: string
  userId: string
  userName: string
  createdAt: string
}

export interface CreateContributionData {
  amount: number
  date: string
}

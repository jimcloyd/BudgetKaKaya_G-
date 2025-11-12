import axios from 'axios'
import { DashboardData } from '../types/dashboard'
import { 
  Expense, 
  Category, 
  ExpenseFilters, 
  ExpenseSummary, 
  CreateExpenseData, 
  UpdateExpenseData 
} from '../types/expense'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Configure axios to include JWT token
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const dashboardApi = {
  getDashboardData: async (): Promise<DashboardData> => {
    const response = await axios.get(`${API_BASE_URL}/dashboard`)
    return response.data
  }
}

// Helper function to convert snake_case to camelCase
const toCamelCase = (obj: any): any => {
  if (Array.isArray(obj)) {
    return obj.map(item => toCamelCase(item))
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
      acc[camelKey] = toCamelCase(obj[key])
      return acc
    }, {} as any)
  }
  return obj
}

// Helper function to convert camelCase to snake_case
const toSnakeCase = (obj: any): any => {
  if (Array.isArray(obj)) {
    return obj.map(item => toSnakeCase(item))
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
      acc[snakeKey] = toSnakeCase(obj[key])
      return acc
    }, {} as any)
  }
  return obj
}

export const expenseApi = {
  getExpenses: async (filters?: ExpenseFilters): Promise<Expense[]> => {
    const params = new URLSearchParams()
    if (filters?.categoryId) params.append('category_id', filters.categoryId)
    if (filters?.startDate) params.append('start_date', filters.startDate)
    if (filters?.endDate) params.append('end_date', filters.endDate)
    if (filters?.userId) params.append('user_id', filters.userId)
    
    const response = await axios.get(`${API_BASE_URL}/expenses?${params.toString()}`)
    return toCamelCase(response.data.expenses)
  },

  createExpense: async (data: CreateExpenseData): Promise<Expense> => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/expenses`, snakeData)
    return toCamelCase(response.data.expense)
  },

  updateExpense: async (id: string, data: UpdateExpenseData): Promise<Expense> => {
    const snakeData = toSnakeCase(data)
    const response = await axios.put(`${API_BASE_URL}/expenses/${id}`, snakeData)
    return toCamelCase(response.data.expense)
  },

  deleteExpense: async (id: string): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/expenses/${id}`)
  },

  getExpenseSummary: async (filters?: ExpenseFilters): Promise<ExpenseSummary[]> => {
    const params = new URLSearchParams()
    if (filters?.startDate) params.append('start_date', filters.startDate)
    if (filters?.endDate) params.append('end_date', filters.endDate)
    
    const response = await axios.get(`${API_BASE_URL}/expenses/summary?${params.toString()}`)
    return toCamelCase(response.data.summary)
  }
}

export const categoryApi = {
  getCategories: async (): Promise<Category[]> => {
    const response = await axios.get(`${API_BASE_URL}/categories`)
    return toCamelCase(response.data.categories || response.data)
  },

  createCategory: async (name: string): Promise<Category> => {
    const response = await axios.post(`${API_BASE_URL}/categories`, { name })
    return toCamelCase(response.data.category || response.data)
  }
}

export const budgetApi = {
  getBudgets: async () => {
    const response = await axios.get(`${API_BASE_URL}/budgets`)
    return toCamelCase(response.data.budgets || response.data)
  },

  createBudget: async (data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/budgets`, snakeData)
    return toCamelCase(response.data.budget || response.data)
  },

  updateBudget: async (id: string, data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.put(`${API_BASE_URL}/budgets/${id}`, snakeData)
    return toCamelCase(response.data.budget || response.data)
  },

  deleteBudget: async (id: string) => {
    await axios.delete(`${API_BASE_URL}/budgets/${id}`)
  },

  getBudgetStatus: async () => {
    const response = await axios.get(`${API_BASE_URL}/budgets/status`)
    return toCamelCase(response.data.status || response.data)
  }
}

export const creditCardApi = {
  getCreditCards: async () => {
    const response = await axios.get(`${API_BASE_URL}/credit-cards`)
    return toCamelCase(response.data.creditCards || response.data)
  },

  createCreditCard: async (data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/credit-cards`, snakeData)
    return toCamelCase(response.data.creditCard || response.data)
  },

  updateCreditCard: async (id: string, data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.put(`${API_BASE_URL}/credit-cards/${id}`, snakeData)
    return toCamelCase(response.data.creditCard || response.data)
  },

  createTransaction: async (cardId: string, data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/credit-cards/${cardId}/transactions`, snakeData)
    return {
      transaction: toCamelCase(response.data.transaction),
      creditCard: toCamelCase(response.data.creditCard)
    }
  }
}


export const installmentApi = {
  getInstallments: async () => {
    const response = await axios.get(`${API_BASE_URL}/installments`)
    return toCamelCase(response.data.installments || response.data)
  },

  createInstallment: async (data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/installments`, snakeData)
    return toCamelCase(response.data.installment || response.data)
  },

  markPayment: async (id: string) => {
    const response = await axios.post(`${API_BASE_URL}/installments/${id}/pay`)
    return toCamelCase(response.data.installment || response.data)
  }
}


export const savingsApi = {
  getSavingsGoals: async () => {
    const response = await axios.get(`${API_BASE_URL}/savings-goals`)
    return toCamelCase(response.data.savingsGoals || response.data)
  },

  createSavingsGoal: async (data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/savings-goals`, snakeData)
    return toCamelCase(response.data.savingsGoal || response.data)
  },

  updateSavingsGoal: async (id: string, data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.put(`${API_BASE_URL}/savings-goals/${id}`, snakeData)
    return toCamelCase(response.data.savingsGoal || response.data)
  },

  addContribution: async (goalId: string, data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/savings-goals/${goalId}/contributions`, snakeData)
    return {
      contribution: toCamelCase(response.data.contribution),
      savingsGoal: toCamelCase(response.data.savingsGoal)
    }
  }
}


export const incomeApi = {
  getMonthlyIncomes: async (month?: number, year?: number) => {
    const params = new URLSearchParams()
    if (month) params.append('month', month.toString())
    if (year) params.append('year', year.toString())
    
    const response = await axios.get(`${API_BASE_URL}/income?${params.toString()}`)
    return toCamelCase(response.data.monthlyIncomes || response.data)
  },

  createMonthlyIncome: async (data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.post(`${API_BASE_URL}/income`, snakeData)
    return toCamelCase(response.data.monthlyIncome || response.data)
  },

  updateMonthlyIncome: async (id: string, data: any) => {
    const snakeData = toSnakeCase(data)
    const response = await axios.put(`${API_BASE_URL}/income/${id}`, snakeData)
    return toCamelCase(response.data.monthlyIncome || response.data)
  }
}


export const accountApi = {
  inviteSpouse: async (email: string) => {
    const response = await axios.post(`${API_BASE_URL}/account/invite`, { email })
    return toCamelCase(response.data.invitation || response.data)
  },

  acceptInvite: async (invitationId: string) => {
    const snakeData = toSnakeCase({ invitationId })
    const response = await axios.post(`${API_BASE_URL}/account/accept-invite`, snakeData)
    return response.data
  },

  getSharedAccount: async () => {
    const response = await axios.get(`${API_BASE_URL}/account/shared`)
    return toCamelCase(response.data.sharedAccount || response.data)
  }
}

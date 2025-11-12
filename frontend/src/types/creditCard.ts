export interface CreditCard {
  id: string
  name: string
  creditLimit: number
  currentBalance: number
  availableCredit: number
  createdAt: string
  updatedAt: string
}

export interface CreateCreditCardData {
  name: string
  creditLimit: number
  currentBalance: number
}

export interface UpdateCreditCardData {
  name?: string
  creditLimit?: number
  currentBalance?: number
}

export interface CreditCardTransaction {
  id: string
  creditCardId: string
  amount: number
  type: 'payment' | 'charge'
  date: string
  description: string | null
  userId: string
  userName: string
  createdAt: string
}

export interface CreateTransactionData {
  amount: number
  type: 'payment' | 'charge'
  date: string
  description?: string
}

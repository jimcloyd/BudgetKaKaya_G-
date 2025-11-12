export interface Installment {
  id: string
  totalAmount: number
  numberOfPayments: number
  monthlyPayment: number
  startDate: string
  description: string
  paidPayments: number
  remainingBalance: number
  nextPaymentDate: string | null
  userId: string
  userName: string
  createdAt: string
  updatedAt: string
}

export interface CreateInstallmentData {
  totalAmount: number
  numberOfPayments: number
  startDate: string
  description: string
}

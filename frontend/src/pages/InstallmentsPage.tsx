import { useState, useEffect } from 'react'
import { installmentApi } from '../services/api'
import { Installment, CreateInstallmentData } from '../types/installment'
import InstallmentList from '../components/installments/InstallmentList'
import InstallmentForm from '../components/installments/InstallmentForm'

const InstallmentsPage = () => {
  const [installments, setInstallments] = useState<Installment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    loadInstallments()
  }, [])

  const loadInstallments = async () => {
    try {
      const data = await installmentApi.getInstallments()
      setInstallments(data)
    } catch (error) {
      console.error('Failed to load installments:', error)
      alert('Failed to load installments. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddInstallment = () => {
    setShowForm(true)
  }

  const handleSubmitInstallment = async (data: CreateInstallmentData) => {
    setIsSaving(true)
    try {
      await installmentApi.createInstallment(data)
      
      await loadInstallments()
      setShowForm(false)
    } catch (error) {
      console.error('Failed to create installment:', error)
      alert('Failed to create installment. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelForm = () => {
    setShowForm(false)
  }

  const handleMarkPaid = async (installment: Installment) => {
    if (!confirm(`Mark payment as paid for "${installment.description}"?`)) {
      return
    }

    try {
      await installmentApi.markPayment(installment.id)
      await loadInstallments()
    } catch (error) {
      console.error('Failed to mark payment:', error)
      alert('Failed to mark payment. Please try again.')
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const totalRemaining = installments
    .filter(inst => inst.paidPayments < inst.numberOfPayments)
    .reduce((sum, inst) => sum + inst.remainingBalance, 0)

  const activeInstallments = installments.filter(
    inst => inst.paidPayments < inst.numberOfPayments
  ).length

  const completedInstallments = installments.filter(
    inst => inst.paidPayments >= inst.numberOfPayments
  ).length

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Installment Tracking</h1>
          <p className="text-gray-600 mt-2">Track your installment payments and remaining balances</p>
        </div>

        {/* Summary Cards */}
        {installments.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Active Installments</h3>
              <p className="text-2xl font-bold text-gray-900">{activeInstallments}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Remaining</h3>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalRemaining)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Completed</h3>
              <p className="text-2xl font-bold text-green-600">{completedInstallments}</p>
            </div>
          </div>
        )}

        {/* Add Installment Button */}
        <div className="mb-6">
          <button
            onClick={handleAddInstallment}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
          >
            + Add Installment
          </button>
        </div>

        {/* Installment Form */}
        {showForm && (
          <div className="mb-6">
            <InstallmentForm
              onSubmit={handleSubmitInstallment}
              onCancel={handleCancelForm}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Installment List */}
        <InstallmentList
          installments={installments}
          onMarkPaid={handleMarkPaid}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}

export default InstallmentsPage

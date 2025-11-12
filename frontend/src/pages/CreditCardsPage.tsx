import { useState, useEffect } from 'react'
import { creditCardApi } from '../services/api'
import { CreditCard, CreateCreditCardData, CreateTransactionData } from '../types/creditCard'
import CreditCardList from '../components/credit-cards/CreditCardList'
import CreditCardForm from '../components/credit-cards/CreditCardForm'
import TransactionForm from '../components/credit-cards/TransactionForm'

const CreditCardsPage = () => {
  const [creditCards, setCreditCards] = useState<CreditCard[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editingCard, setEditingCard] = useState<CreditCard | null>(null)
  const [showTransactionForm, setShowTransactionForm] = useState(false)
  const [selectedCard, setSelectedCard] = useState<CreditCard | null>(null)

  useEffect(() => {
    loadCreditCards()
  }, [])

  const loadCreditCards = async () => {
    try {
      const data = await creditCardApi.getCreditCards()
      setCreditCards(data)
    } catch (error) {
      console.error('Failed to load credit cards:', error)
      alert('Failed to load credit cards. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleAddCard = () => {
    setEditingCard(null)
    setShowForm(true)
  }

  const handleEditCard = (card: CreditCard) => {
    setEditingCard(card)
    setShowForm(true)
  }

  const handleSubmitCard = async (data: CreateCreditCardData) => {
    setIsSaving(true)
    try {
      if (editingCard) {
        await creditCardApi.updateCreditCard(editingCard.id, data)
      } else {
        await creditCardApi.createCreditCard(data)
      }
      
      await loadCreditCards()
      setShowForm(false)
      setEditingCard(null)
    } catch (error) {
      console.error('Failed to save credit card:', error)
      alert('Failed to save credit card. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelForm = () => {
    setShowForm(false)
    setEditingCard(null)
  }

  const handleAddTransaction = (card: CreditCard) => {
    setSelectedCard(card)
    setShowTransactionForm(true)
  }

  const handleSubmitTransaction = async (data: CreateTransactionData) => {
    if (!selectedCard) return

    setIsSaving(true)
    try {
      await creditCardApi.createTransaction(selectedCard.id, data)
      
      await loadCreditCards()
      setShowTransactionForm(false)
      setSelectedCard(null)
    } catch (error) {
      console.error('Failed to record transaction:', error)
      alert('Failed to record transaction. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancelTransaction = () => {
    setShowTransactionForm(false)
    setSelectedCard(null)
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const totalBalance = creditCards.reduce((sum, card) => sum + card.currentBalance, 0)
  const totalLimit = creditCards.reduce((sum, card) => sum + card.creditLimit, 0)
  const totalAvailable = creditCards.reduce((sum, card) => sum + card.availableCredit, 0)

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Credit Card Management</h1>
          <p className="text-gray-600 mt-2">Track your credit card balances and available credit</p>
        </div>

        {/* Summary Cards */}
        {creditCards.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Balance</h3>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalBalance)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Credit Limit</h3>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalLimit)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-600 mb-2">Total Available</h3>
              <p className="text-2xl font-bold text-green-600">{formatCurrency(totalAvailable)}</p>
            </div>
          </div>
        )}

        {/* Add Card Button */}
        <div className="mb-6">
          <button
            onClick={handleAddCard}
            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 font-medium"
          >
            + Add Credit Card
          </button>
        </div>

        {/* Card Form */}
        {showForm && (
          <div className="mb-6">
            <CreditCardForm
              card={editingCard}
              onSubmit={handleSubmitCard}
              onCancel={handleCancelForm}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Transaction Form */}
        {showTransactionForm && selectedCard && (
          <div className="mb-6">
            <TransactionForm
              cardName={selectedCard.name}
              onSubmit={handleSubmitTransaction}
              onCancel={handleCancelTransaction}
              isLoading={isSaving}
            />
          </div>
        )}

        {/* Card List */}
        <CreditCardList
          creditCards={creditCards}
          onEdit={handleEditCard}
          onAddTransaction={handleAddTransaction}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}

export default CreditCardsPage

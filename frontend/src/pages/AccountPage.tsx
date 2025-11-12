import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { accountApi } from '../services/api'
import { SharedAccount } from '../types/account'
import InviteSpouse from '../components/account/InviteSpouse'
import SharedAccountView from '../components/account/SharedAccountView'

const AccountPage = () => {
  const { user } = useAuth()
  const [sharedAccount, setSharedAccount] = useState<SharedAccount | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSending, setIsSending] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    loadSharedAccount()
  }, [])

  const loadSharedAccount = async () => {
    try {
      const data = await accountApi.getSharedAccount()
      setSharedAccount(data)
    } catch (error: any) {
      // 404 means user doesn't have a shared account yet
      if (error.response?.status !== 404) {
        console.error('Failed to load shared account:', error)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleInvite = async (email: string) => {
    setIsSending(true)
    setSuccessMessage('')
    setErrorMessage('')

    try {
      await accountApi.inviteSpouse(email)
      setSuccessMessage(`Invitation sent successfully to ${email}!`)
      
      // Reload shared account data
      await loadSharedAccount()
    } catch (error: any) {
      console.error('Failed to send invitation:', error)
      
      const message = error.response?.data?.message || 'Failed to send invitation. Please try again.'
      setErrorMessage(message)
    } finally {
      setIsSending(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Account Settings</h1>
          <p className="text-gray-600 mt-2">Manage your shared account and invitations</p>
        </div>

        {/* Success Message */}
        {successMessage && (
          <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
            {successMessage}
          </div>
        )}

        {/* Error Message */}
        {errorMessage && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {errorMessage}
          </div>
        )}

        {/* Shared Account View or Invite Form */}
        {sharedAccount && sharedAccount.users.length === 2 ? (
          <SharedAccountView sharedAccount={sharedAccount} currentUserId={user?.id || ''} />
        ) : (
          <>
            {sharedAccount && sharedAccount.users.length === 1 && (
              <div className="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800 text-sm">
                  You have created a shared account but haven't invited your spouse yet. 
                  Send an invitation below to start sharing your budget.
                </p>
              </div>
            )}
            
            <InviteSpouse onInvite={handleInvite} isLoading={isSending} />
            
            <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-2">How it works:</h3>
              <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                <li>Your spouse must create an account first</li>
                <li>Send them an invitation using their email address</li>
                <li>They will need to log in and accept the invitation</li>
                <li>Once accepted, you'll both have access to the same budget data</li>
              </ol>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default AccountPage

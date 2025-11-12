import { SharedAccount } from '../../types/account'

interface SharedAccountViewProps {
  sharedAccount: SharedAccount
  currentUserId: string
}

const SharedAccountView = ({ sharedAccount, currentUserId }: SharedAccountViewProps) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Shared Account</h2>
      <p className="text-gray-600 mb-4">
        You are sharing your budget with {sharedAccount.users.length === 2 ? 'your spouse' : 'another user'}.
      </p>

      <div className="space-y-4">
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">Account Members</h3>
          <div className="space-y-2">
            {sharedAccount.users.map((user) => (
              <div
                key={user.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
              >
                <div>
                  <p className="font-medium text-gray-900">
                    {user.name}
                    {user.id === currentUserId && (
                      <span className="ml-2 text-xs text-blue-600 font-medium">(You)</span>
                    )}
                  </p>
                  <p className="text-sm text-gray-600">{user.email}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-500">Joined</p>
                  <p className="text-xs text-gray-600">{formatDate(user.createdAt)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
          <p className="text-sm text-blue-800">
            <strong>Note:</strong> All financial data (expenses, budgets, income, etc.) is shared between both users. 
            Any changes made by one user will be visible to the other.
          </p>
        </div>
      </div>
    </div>
  )
}

export default SharedAccountView

interface User {
  id: string
  name: string
}

interface SpouseFilterProps {
  users: User[]
  selectedUserId: string
  onUserChange: (userId: string) => void
}

const SpouseFilter = ({ users, selectedUserId, onUserChange }: SpouseFilterProps) => {
  return (
    <div className="flex flex-col gap-2">
      <label htmlFor="spouse-filter" className="text-sm font-medium text-gray-700">
        Filter by Spouse
      </label>
      <select
        id="spouse-filter"
        value={selectedUserId}
        onChange={(e) => onUserChange(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Both Spouses</option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.name}
          </option>
        ))}
      </select>
    </div>
  )
}

export default SpouseFilter

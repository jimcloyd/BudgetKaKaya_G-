import { Category } from '../../types/expense'

interface CategoryFilterProps {
  categories: Category[]
  selectedCategoryId: string
  onCategoryChange: (categoryId: string) => void
}

const CategoryFilter = ({ categories, selectedCategoryId, onCategoryChange }: CategoryFilterProps) => {
  return (
    <div className="flex flex-col gap-2">
      <label htmlFor="category-filter" className="text-sm font-medium text-gray-700">
        Filter by Category
      </label>
      <select
        id="category-filter"
        value={selectedCategoryId}
        onChange={(e) => onCategoryChange(e.target.value)}
        className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Categories</option>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>
    </div>
  )
}

export default CategoryFilter

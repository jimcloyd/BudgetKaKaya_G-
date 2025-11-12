# Expense Management Components

This directory contains all components related to expense management functionality.

## Components

### ExpensesPage (Main Page)
- **Location**: `src/pages/ExpensesPage.tsx`
- **Purpose**: Main page that integrates all expense management features
- **Features**:
  - Expense filtering (by category, date range, spouse)
  - Add/Edit expense functionality
  - Delete expense with confirmation
  - Real-time total calculation
  - Expense summary visualization

### ExpenseList
- **Purpose**: Displays expenses in table or card view
- **Features**:
  - Toggle between table and card layouts
  - Shows expense details (date, category, amount, description, creator)
  - Edit and delete actions for each expense
  - Responsive design

### ExpenseForm
- **Purpose**: Form for creating and editing expenses
- **Features**:
  - Amount validation (positive, 2 decimal places)
  - Category selection
  - Date picker
  - Description field
  - Form validation with error messages
  - Loading states

### ExpenseSummary
- **Purpose**: Visual summary of spending by category
- **Features**:
  - Pie chart visualization using Chart.js
  - Category breakdown with percentages
  - Total spending calculation
  - Progress bars for each category
  - Expense count per category

### CategoryFilter
- **Purpose**: Filter expenses by category
- **Features**:
  - Dropdown with all categories
  - "All Categories" option

### DateRangePicker
- **Purpose**: Filter expenses by date range
- **Features**:
  - Start and end date inputs
  - Responsive layout

### SpouseFilter
- **Purpose**: Filter expenses by spouse
- **Features**:
  - Dropdown with both spouses
  - "Both Spouses" option

### DeleteConfirmationDialog
- **Purpose**: Confirm expense deletion
- **Features**:
  - Modal dialog
  - Shows expense details
  - Confirm/Cancel actions
  - Loading state during deletion

## API Integration

All components use the `expenseApi` and `categoryApi` from `src/services/api.ts`:

- `getExpenses(filters)` - Fetch expenses with optional filters
- `createExpense(data)` - Create new expense
- `updateExpense(id, data)` - Update existing expense
- `deleteExpense(id)` - Delete expense
- `getExpenseSummary(filters)` - Get spending summary by category
- `getCategories()` - Fetch all categories

## Types

All TypeScript types are defined in `src/types/expense.ts`:
- `Expense` - Expense entity
- `Category` - Category entity
- `ExpenseFilters` - Filter parameters
- `ExpenseSummary` - Summary data structure
- `CreateExpenseData` - Data for creating expense
- `UpdateExpenseData` - Data for updating expense

## Routing

The ExpensesPage is accessible at `/expenses` route (configured in `App.tsx`).

## Requirements Covered

This implementation covers the following requirements:
- **3.1-3.5**: Recording and displaying expenses
- **4.4-4.5**: Spending summary by category with percentages
- **6.3**: Filtering by category, date range, and spouse
- **7.1-7.5**: Edit and delete expense operations

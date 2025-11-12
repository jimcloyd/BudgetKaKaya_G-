# Dashboard Components

This directory contains all the components used in the main dashboard view of the Family Budget Tracker.

## Components

### QuickStats
Displays four key metrics in a grid layout:
- Total Spent (current month)
- Monthly Income
- Net Income (highlighted in red if negative)
- Remaining Budget

### IncomeVsExpensesChart
A bar chart comparing monthly income vs expenses using Chart.js:
- Visual comparison of income and expenses
- Month-over-month spending comparison
- Percentage change indicator (red for increase, green for decrease)

### BudgetStatusSummary
Shows budget status for all categories with limits:
- Visual indicators: ✅ (ok), ⚠️ (warning at 80%+), 🔴 (exceeded at 100%+)
- Color-coded progress bars (green/yellow/red)
- Percentage used and remaining amount
- Handles negative remaining amounts (over budget)

### RecentExpensesList
Displays the most recent expenses:
- Expense description and category badge
- Date and user who created it
- Amount formatted as currency

### UpcomingInstallments
Shows upcoming installment payments:
- Monthly payment amount
- Next payment due date
- Remaining payments count
- Remaining balance

## API Integration

All components receive data from the `/api/dashboard` endpoint which returns:
```typescript
{
  totalExpenses: number
  monthlyIncome: number
  netIncome: number
  budgetStatus: BudgetStatus[]
  recentExpenses: Expense[]
  upcomingInstallments: Installment[]
  monthOverMonthComparison: {
    currentMonth: number
    previousMonth: number
    percentageChange: number
  }
}
```

## Requirements Covered

- **Requirement 6.4**: Dashboard displays total spent, total budget, and remaining budget
- **Requirement 11.3**: Chart comparing monthly income to total expenses
- **Requirement 11.4**: Net income calculation (income - expenses)
- **Requirement 11.5**: Net income displayed in red when negative
- **Requirement 5.3**: Warning indicator at 80% budget
- **Requirement 5.4**: Alert indicator when exceeding budget
- **Requirement 5.5**: Remaining budget amounts displayed

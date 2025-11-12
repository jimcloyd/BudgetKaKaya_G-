# Dashboard Implementation

## Overview
The dashboard endpoint provides a comprehensive summary of the household's financial status, including expenses, income, budget status, and upcoming payments.

## Endpoint

### GET /api/dashboard

Returns a comprehensive dashboard summary for the authenticated user's shared account.

**Authentication Required:** Yes (JWT token)

**Authorization:** User must be part of a shared account

**Response (200 OK):**
```json
{
  "total_expenses": 225.75,
  "monthly_income": 5000.00,
  "net_income": 4774.25,
  "budget_status": [
    {
      "category_id": "uuid",
      "category_name": "Groceries",
      "budget_amount": 500.00,
      "spent": 225.75,
      "remaining": 274.25,
      "percentage": 45.15,
      "status": "ok"
    }
  ],
  "recent_expenses": [
    {
      "id": "uuid",
      "amount": 150.50,
      "category_name": "Groceries",
      "date": "2025-11-10",
      "description": "Weekly shopping",
      "user_name": "John Doe"
    }
  ],
  "upcoming_installments": [
    {
      "id": "uuid",
      "description": "Laptop purchase",
      "monthly_payment": 100.00,
      "next_payment_date": "2025-11-15",
      "paid_payments": 3,
      "total_payments": 12
    }
  ],
  "spending_comparison": {
    "current_month": 225.75,
    "previous_month": 200.00,
    "change_amount": 25.75,
    "change_percentage": 12.88
  },
  "current_month": 11,
  "current_year": 2025
}
```

## Implementation Details

### 1. Total Expenses Calculation
- Calculates the sum of all expenses for the current month
- Uses the shared account ID to filter expenses
- Date range: First day to last day of current month

### 2. Monthly Income
- Retrieves the monthly income record for the current month and year
- Returns 0 if no income record exists for the current month

### 3. Net Income
- Calculated as: `monthly_income - total_expenses`
- Can be negative if expenses exceed income

### 4. Budget Status Summary
- Retrieves all budget limits for the shared account
- For each budget limit:
  - Calculates the appropriate date range (weekly or monthly)
  - Sums expenses in that category for the period
  - Calculates percentage used and remaining amount
  - Determines status:
    - `ok`: Less than 80% of budget used
    - `warning`: 80-99% of budget used
    - `exceeded`: 100% or more of budget used

### 5. Recent Expenses
- Returns the 10 most recent expenses
- Ordered by date (descending) and creation time (descending)
- Includes expense details and the user who created it

### 6. Upcoming Installments
- Retrieves all active installments (not fully paid)
- Filters for installments with next payment due in current month
- Includes payment details and progress

### 7. Month-over-Month Comparison
- Calculates total expenses for previous month
- Compares with current month expenses
- Calculates absolute change and percentage change
- Percentage change formula:
  - If previous month > 0: `((current - previous) / previous) * 100`
  - If previous month = 0 and current = 0: `0%`
  - If previous month = 0 and current > 0: `100%`

## Requirements Mapping

This implementation satisfies the following requirements:

- **Requirement 6.1**: Calculate total expenses for the current month
- **Requirement 6.4**: Display summary showing total spent
- **Requirement 11.3**: Display chart comparing monthly income to total expenses
- **Requirement 11.4**: Calculate net income by subtracting total expenses from monthly income
- **Requirement 11.5**: Display negative net income in red (frontend responsibility, but data provided)

## Usage Example

```bash
# Get dashboard summary
curl -X GET http://localhost:5000/api/dashboard \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Error Responses

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "User not found"
}
```

**403 Forbidden:**
```json
{
  "error": "Forbidden",
  "message": "User must be part of a shared account to access this resource"
}
```

## Notes

- All monetary values are returned as floats with 2 decimal places
- Dates are returned in ISO format (YYYY-MM-DD)
- The endpoint uses the current UTC date/time for calculations
- Budget status is calculated based on the current period (weekly or monthly)
- Only installments due in the current month are included in upcoming payments

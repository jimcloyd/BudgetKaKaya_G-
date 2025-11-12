# Savings Goals Implementation

## Overview
This document describes the implementation of the savings goals feature for the Family Budget Tracker application.

## Implemented Endpoints

### 1. GET /api/savings-goals
**Description:** Retrieve all savings goals for the shared account

**Authentication:** Required (JWT)

**Response:**
```json
{
  "savings_goals": [
    {
      "id": "uuid",
      "name": "Emergency Fund",
      "target_amount": 10000.00,
      "current_balance": 4000.00,
      "target_date": "2025-12-31",
      "percentage_completed": 40.00,
      "remaining_amount": 6000.00,
      "suggested_monthly_contribution": 500.00,
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-15T00:00:00"
    }
  ]
}
```

### 2. POST /api/savings-goals
**Description:** Create a new savings goal

**Authentication:** Required (JWT)

**Request Body:**
```json
{
  "name": "Emergency Fund",
  "target_amount": 10000.00,
  "target_date": "2025-12-31"  // Optional
}
```

**Response:** 201 Created
```json
{
  "message": "Savings goal created successfully",
  "savings_goal": {
    "id": "uuid",
    "name": "Emergency Fund",
    "target_amount": 10000.00,
    "current_balance": 0.00,
    "target_date": "2025-12-31",
    "percentage_completed": 0.00,
    "remaining_amount": 10000.00,
    "suggested_monthly_contribution": 833.33,
    "created_at": "2025-01-01T00:00:00"
  }
}
```

### 3. PUT /api/savings-goals/:id
**Description:** Update an existing savings goal

**Authentication:** Required (JWT)

**Request Body:** (all fields optional)
```json
{
  "name": "Updated Emergency Fund",
  "target_amount": 15000.00,
  "target_date": "2026-01-31"
}
```

**Response:** 200 OK
```json
{
  "message": "Savings goal updated successfully",
  "savings_goal": {
    "id": "uuid",
    "name": "Updated Emergency Fund",
    "target_amount": 15000.00,
    "current_balance": 4000.00,
    "target_date": "2026-01-31",
    "percentage_completed": 26.67,
    "remaining_amount": 11000.00,
    "suggested_monthly_contribution": 916.67,
    "updated_at": "2025-01-15T00:00:00"
  }
}
```

### 4. POST /api/savings-goals/:id/contributions
**Description:** Add a contribution to a savings goal

**Authentication:** Required (JWT)

**Request Body:**
```json
{
  "amount": 500.00,
  "date": "2025-01-15"
}
```

**Response:** 201 Created
```json
{
  "message": "Contribution added successfully",
  "contribution": {
    "id": "uuid",
    "amount": 500.00,
    "date": "2025-01-15",
    "user_id": "uuid",
    "user_name": "John Doe",
    "created_at": "2025-01-15T00:00:00"
  },
  "savings_goal": {
    "id": "uuid",
    "name": "Emergency Fund",
    "target_amount": 10000.00,
    "current_balance": 4500.00,
    "target_date": "2025-12-31",
    "percentage_completed": 45.00,
    "remaining_amount": 5500.00,
    "suggested_monthly_contribution": 458.33,
    "updated_at": "2025-01-15T00:00:00"
  }
}
```

## Features Implemented

### Requirement 9.1: Create Savings Goal
- ✅ Requires goal name and target amount
- ✅ Optional target date field
- ✅ Initializes current_balance to 0

### Requirement 9.2: Record Savings Contributions
- ✅ Allows users to record contributions with amount and date
- ✅ Automatically updates savings goal current_balance
- ✅ Tracks which user made the contribution

### Requirement 9.3: Display Progress
- ✅ Calculates and displays percentage completed (current / target * 100)
- ✅ Caps percentage at 100% even if contributions exceed target

### Requirement 9.4: Calculate Remaining Amount
- ✅ Calculates remaining amount needed (target - current)
- ✅ Returns 0 if current balance exceeds target

### Requirement 9.5: Suggested Monthly Contribution
- ✅ Calculates suggested monthly contribution when target date exists
- ✅ Formula: remaining_amount / months_remaining
- ✅ Returns null if no target date or goal already reached

## Validation Rules

### Amount Validation
- Must be positive
- Maximum 2 decimal places
- Proper decimal handling to avoid floating-point errors

### Date Validation
- Format: YYYY-MM-DD
- Required for contributions
- Optional for savings goals

### Name Validation
- Cannot be empty
- Whitespace is trimmed

## Security
- All endpoints require JWT authentication
- Shared account access verification
- Users can only access savings goals in their shared account
- Both spouses can view and contribute to all goals

## Database Models

### SavingsGoal
- id (UUID)
- shared_account_id (FK)
- name (String)
- target_amount (Decimal)
- current_balance (Decimal)
- target_date (Date, nullable)
- created_at (DateTime)
- updated_at (DateTime)

### SavingsContribution
- id (UUID)
- savings_goal_id (FK)
- user_id (FK)
- amount (Decimal)
- date (Date)
- created_at (DateTime)

## Testing

A manual test script is provided in `test_savings_manual.py` that tests:
1. Creating savings goals with and without target dates
2. Adding contributions
3. Updating savings goals
4. Verifying calculations (percentage, remaining, suggested monthly)

To run the tests:
```bash
# Start the Flask server
python run.py

# In another terminal, run the test script
python test_savings_manual.py
```

## Error Handling

### 401 Unauthorized
- Invalid or expired JWT token

### 403 Forbidden
- User not part of a shared account
- Attempting to access another account's savings goals

### 404 Not Found
- Savings goal ID doesn't exist

### 422 Validation Error
- Missing required fields
- Invalid amount format
- Invalid date format
- Empty name field

## Future Enhancements
- Delete savings goal endpoint
- Get contribution history for a goal
- Set contribution reminders
- Goal completion notifications
- Export savings history to CSV

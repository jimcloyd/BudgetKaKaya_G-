# Installment Tracking Implementation

## Overview
This document describes the implementation of installment tracking endpoints for the Family Budget Tracker application.

## Features Implemented

### 1. Create Installment (POST /api/installments)
Creates a new installment plan for tracking recurring payments.

**Request Body:**
```json
{
  "total_amount": 12000.00,
  "number_of_payments": 12,
  "start_date": "2024-01-01",
  "description": "New laptop purchase"
}
```

**Response (201 Created):**
```json
{
  "message": "Installment created successfully",
  "installment": {
    "id": "uuid",
    "total_amount": 12000.00,
    "number_of_payments": 12,
    "monthly_payment": 1000.00,
    "start_date": "2024-01-01",
    "description": "New laptop purchase",
    "paid_payments": 0,
    "remaining_balance": 12000.00,
    "next_payment_date": "2024-01-01",
    "user_id": "uuid",
    "user_name": "John Doe",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Features:**
- Automatically calculates monthly payment (total_amount / number_of_payments)
- Rounds monthly payment to 2 decimal places
- Validates all required fields
- Validates amount is positive with max 2 decimal places
- Validates number_of_payments is positive integer
- Validates date format (YYYY-MM-DD)
- Associates installment with current user and shared account

### 2. Get All Installments (GET /api/installments)
Retrieves all installments for the shared account.

**Response (200 OK):**
```json
{
  "installments": [
    {
      "id": "uuid",
      "total_amount": 12000.00,
      "number_of_payments": 12,
      "monthly_payment": 1000.00,
      "start_date": "2024-01-01",
      "description": "New laptop purchase",
      "paid_payments": 3,
      "remaining_balance": 9000.00,
      "next_payment_date": "2024-04-01",
      "user_id": "uuid",
      "user_name": "John Doe",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-03-01T00:00:00"
    }
  ]
}
```

**Features:**
- Returns all installments for the shared account
- Calculates remaining balance dynamically
- Calculates next payment date based on paid payments
- Shows which user created the installment
- Ordered by creation date (newest first)

### 3. Mark Payment as Completed (POST /api/installments/:id/pay)
Marks an installment payment as completed.

**Response (200 OK):**
```json
{
  "message": "Payment marked as completed",
  "installment": {
    "id": "uuid",
    "total_amount": 12000.00,
    "number_of_payments": 12,
    "monthly_payment": 1000.00,
    "start_date": "2024-01-01",
    "description": "New laptop purchase",
    "paid_payments": 4,
    "remaining_balance": 8000.00,
    "next_payment_date": "2024-05-01",
    "user_id": "uuid",
    "user_name": "John Doe",
    "updated_at": "2024-04-01T00:00:00"
  }
}
```

**Features:**
- Increments paid_payments counter
- Validates installment exists and user has access
- Prevents marking payment when all payments are completed
- Updates remaining balance and next payment date automatically
- Updates the updated_at timestamp

## Calculations

### Monthly Payment
```python
monthly_payment = total_amount / number_of_payments
# Rounded to 2 decimal places
```

### Remaining Balance
```python
remaining_payments = number_of_payments - paid_payments
remaining_balance = monthly_payment * remaining_payments
```

### Next Payment Date
```python
# Next payment is start_date + paid_payments months
next_payment_date = start_date + relativedelta(months=paid_payments)
# Returns None if all payments are completed
```

## Authentication & Authorization
All endpoints require:
- Valid JWT token (`@jwt_required()`)
- User must be part of a shared account (`@shared_account_required`)
- User can only access installments from their shared account

## Validation Rules

### Create Installment
- `total_amount`: Required, positive number with max 2 decimal places
- `number_of_payments`: Required, positive integer
- `start_date`: Required, valid date in YYYY-MM-DD format
- `description`: Required, non-empty string

### Mark Payment
- Installment must exist
- User must have access to the shared account
- Cannot mark payment if all payments are already completed

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "User not found"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Access denied to this resource"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Installment not found"
}
```

### 422 Validation Error
```json
{
  "error": "Validation Error",
  "message": "Missing required fields: total_amount, number_of_payments"
}
```

## Database Schema
The Installment model includes:
- `id`: UUID primary key
- `shared_account_id`: Foreign key to shared_accounts
- `user_id`: Foreign key to users (who created it)
- `total_amount`: Decimal(10, 2)
- `number_of_payments`: Integer
- `monthly_payment`: Decimal(10, 2)
- `start_date`: Date
- `description`: Text
- `paid_payments`: Integer (default 0)
- `created_at`: DateTime
- `updated_at`: DateTime

## Dependencies
- `python-dateutil`: For date calculations (relativedelta)

## Testing
Run the manual test script:
```bash
python backend/test_installments_manual.py
```

Make sure to:
1. Start the Flask server
2. Update test credentials in the script
3. Have a test user with shared account access

## Requirements Satisfied
- **Requirement 8.1**: Create installment with total amount, number of payments, start date, and description
- **Requirement 8.2**: Calculate monthly payment by dividing total amount by number of payments
- **Requirement 8.3**: Track which installment payments have been completed
- **Requirement 8.4**: Track which payments remain outstanding
- **Requirement 8.5**: Display remaining balance, next payment date, and monthly payment amount

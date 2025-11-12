# Category Management Implementation

## Overview
This document describes the implementation of task 5.1: Create category endpoints for the Family Budget Tracker application.

## Implementation Details

### 1. Category Endpoints (backend/app/routes/categories.py)

#### GET /api/categories
- **Purpose**: Retrieve all categories for the user's shared account
- **Authentication**: Requires JWT token and shared account membership
- **Response**: Returns list of categories sorted alphabetically by name
- **Status Codes**:
  - 200: Success
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user not part of shared account)

#### POST /api/categories
- **Purpose**: Create a custom category for the user's shared account
- **Authentication**: Requires JWT token and shared account membership
- **Request Body**: `{ "name": "category_name" }`
- **Validation**:
  - Category name is required
  - Category name cannot be empty (after trimming)
  - Category name must be unique per shared account (case-insensitive)
- **Response**: Returns created category with id, name, is_custom flag, and created_at timestamp
- **Status Codes**:
  - 201: Category created successfully
  - 401: Unauthorized (invalid/missing token)
  - 403: Forbidden (user not part of shared account)
  - 409: Conflict (category name already exists)
  - 422: Validation error (missing or empty name)

### 2. Default Categories Seeding (backend/app/category_utils.py)

Created a utility module with:
- **DEFAULT_CATEGORIES**: List of 6 default categories
  - groceries
  - utilities
  - transportation
  - entertainment
  - healthcare
  - miscellaneous

- **seed_default_categories(shared_account_id)**: Function that:
  - Seeds default categories when a new shared account is created
  - Checks for existing categories to avoid duplicates
  - Marks default categories with `is_custom=False`

### 3. Integration with Account Creation (backend/app/routes/account.py)

Updated the `/api/account/invite` endpoint to:
- Automatically seed default categories when a new shared account is created
- This happens when a user sends their first invitation (creating a shared account)

## Requirements Satisfied

✅ **Requirement 4.1**: The Budget Tracker provides predefined categories including groceries, utilities, transportation, entertainment, healthcare, and miscellaneous

✅ **Requirement 4.2**: When a User creates an expense, the Budget Tracker requires selection of exactly one category (enforced by database schema and future expense endpoints)

✅ **Requirement 4.3**: The Budget Tracker allows Users to add custom categories with unique names (validated case-insensitively per shared account)

## Database Schema

The Category model (already in migrations) includes:
- `id`: UUID primary key
- `shared_account_id`: Foreign key to shared_accounts table
- `name`: Category name (max 100 characters)
- `is_custom`: Boolean flag (False for default, True for custom)
- `created_at`: Timestamp

## Testing

A manual test script has been created at `backend/test_categories_manual.py` that tests:
1. User registration and authentication
2. Category access without shared account (should fail)
3. Shared account creation via invitation
4. Retrieving default categories
5. Creating custom categories
6. Duplicate category validation
7. Empty name validation

To run the test:
```bash
# Start the Flask server
cd backend
python run.py

# In another terminal, run the test
python test_categories_manual.py
```

## API Examples

### Get Categories
```bash
curl -X GET http://localhost:5000/api/categories \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "categories": [
    {
      "id": "uuid-here",
      "name": "groceries",
      "is_custom": false,
      "created_at": "2025-11-10T12:00:00"
    },
    {
      "id": "uuid-here",
      "name": "Dining Out",
      "is_custom": true,
      "created_at": "2025-11-10T12:30:00"
    }
  ]
}
```

### Create Custom Category
```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Dining Out"}'
```

Response:
```json
{
  "message": "Category created successfully",
  "category": {
    "id": "uuid-here",
    "name": "Dining Out",
    "is_custom": true,
    "created_at": "2025-11-10T12:30:00"
  }
}
```

## Files Modified/Created

### Created:
- `backend/app/category_utils.py` - Utility functions for category management
- `backend/test_categories_manual.py` - Manual test script
- `backend/CATEGORY_IMPLEMENTATION.md` - This documentation

### Modified:
- `backend/app/routes/categories.py` - Implemented GET and POST endpoints
- `backend/app/routes/account.py` - Added default category seeding on shared account creation

## Next Steps

The category management system is now complete and ready for use. Future tasks will:
- Use these categories in expense management (Task 6)
- Use these categories in budget management (Task 7)
- Build the frontend UI for category management (Task 16)

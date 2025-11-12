# Income Tracking Implementation

## Overview
This document describes the implementation of the monthly income tracking feature for the Family Budget Tracker application.

## Requirements Implemented
- **Requirement 11.1**: Set monthly income for a specific month and year
- **Requirement 11.2**: Update monthly income for any month

## API Endpoints

### 1. GET /api/income
Get monthly income records with optional filtering.

**Authentication**: Required (JWT)

**Query Parameters**:
- `month` (optional): Filter by month (1-12)
- `year` (optional): Filter by year (4-digit year)

**Response** (200 OK):
```json
{
  "monthly_incomes": [
    {
      "id": "uuid",
      "month": 11,
      "year": 2025,
      "amount": 5000.00,
      "created_at": "2025-11-10T12:00:00",
      "updated_at": "2025-11-10T12:00:00"
    }
  ]
}
```

**Example Usage**:
```bash
# Get all incomes
GET /api/income

# Get income for specific month/year
GET /api/income?month=11&year=2025

# Get all incomes for a year
GET /api/income?year=2025
```

### 2. POST /api/income
Create a new monthly income record.

**Authentication**: Required (JWT)

**Request Body**:
```json
{
  "month": 11,
  "year": 2025,
  "amount": 5000.00
}
```

**Validation Rules**:
- `month`: Required, integer between 1-12
- `year`: Required, valid 4-digit year (1900-9999)
- `amount`: Required, positive number with max 2 decimal places
- Unique constraint: Only one income record per shared account, month, and year

**Response** (201 Created):
```json
{
  "message": "Monthly income created successfully",
  "monthly_income": {
    "id": "uuid",
    "month": 11,
    "year": 2025,
    "amount": 5000.00,
    "created_at": "2025-11-10T12:00:00"
  }
}
```

**Error Response** (409 Conflict):
```json
{
  "error": "Conflict",
  "message": "Monthly income for 11/2025 already exists. Use PUT to update."
}
```

### 3. PUT /api/income/:id
Update an existing monthly income record.

**Authentication**: Required (JWT)

**URL Parameters**:
- `id`: The UUID of the monthly income record

**Request Body** (all fields optional):
```json
{
  "month": 12,
  "year": 2025,
  "amount": 5500.00
}
```

**Validation Rules**:
- `month`: Optional, integer between 1-12
- `year`: Optional, valid 4-digit year (1900-9999)
- `amount`: Optional, positive number with max 2 decimal places
- If month/year is updated, must not conflict with existing records

**Response** (200 OK):
```json
{
  "message": "Monthly income updated successfully",
  "monthly_income": {
    "id": "uuid",
    "month": 12,
    "year": 2025,
    "amount": 5500.00,
    "updated_at": "2025-11-10T13:00:00"
  }
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Not Found",
  "message": "Monthly income not found"
}
```

**Error Response** (403 Forbidden):
```json
{
  "error": "Forbidden",
  "message": "Access denied to this resource"
}
```

## Database Model

The `MonthlyIncome` model is defined in `app/models.py`:

```python
class MonthlyIncome(db.Model):
    __tablename__ = 'monthly_income'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    shared_account_id = db.Column(db.String(36), db.ForeignKey('shared_accounts.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('shared_account_id', 'month', 'year'),)
```

**Key Features**:
- Unique constraint ensures only one income record per shared account, month, and year
- Amount stored as Numeric(10, 2) for precise decimal handling
- Automatic timestamp tracking with created_at and updated_at

## Security & Authorization

All endpoints require:
1. **JWT Authentication**: Valid JWT token in Authorization header
2. **Shared Account Access**: User must be part of a shared account
3. **Resource Ownership**: Users can only access income records for their own shared account

## Validation

The implementation includes comprehensive validation:

### Amount Validation
- Must be positive
- Maximum 2 decimal places
- Proper decimal handling to avoid floating-point errors

### Month Validation
- Must be integer between 1 and 12
- Clear error messages for invalid values

### Year Validation
- Must be valid 4-digit year (1900-9999)
- Prevents unrealistic year values

### Unique Constraint
- Database-level constraint prevents duplicate entries
- Returns 409 Conflict with helpful message directing to PUT endpoint

## Testing

### Manual Testing
Run the manual test script:

```bash
# Make sure Flask server is running
python run.py

# In another terminal, run the test script
python test_income_manual.py
```

The test script covers:
- Creating monthly income records
- Duplicate prevention (409 error)
- Retrieving all incomes
- Filtering by month and year
- Updating income records
- Validation error handling
- Authorization checks

### Test Scenarios Covered
1. ✅ Create monthly income for current month
2. ✅ Attempt duplicate creation (should fail)
3. ✅ Get all monthly incomes
4. ✅ Filter by month and year
5. ✅ Create income for different month
6. ✅ Update income amount
7. ✅ Invalid month validation (13)
8. ✅ Invalid amount validation (negative)
9. ✅ Missing required fields validation

## Error Handling

The implementation handles various error scenarios:

| Status Code | Scenario | Response |
|------------|----------|----------|
| 200 | Successful GET or PUT | Income data |
| 201 | Successful POST | Created income data |
| 401 | Missing/invalid JWT token | Unauthorized error |
| 403 | User not in shared account | Forbidden error |
| 404 | Income record not found | Not found error |
| 409 | Duplicate month/year | Conflict error |
| 422 | Validation error | Validation error with details |

## Integration with Dashboard

The income endpoints are designed to integrate with:
- **Dashboard endpoint** (Task 12): Provides income data for income vs expenses comparison
- **Monthly comparison charts**: Shows income against spending
- **Net income calculation**: Income - expenses for financial health indicator

## Future Enhancements

Potential improvements for future iterations:
- Income categories (salary, bonus, investment, etc.)
- Multiple income sources per month
- Income history and trends
- Automatic income rollover for recurring salaries
- Income forecasting based on historical data

## Files Modified/Created

1. **backend/app/routes/income.py** - Complete implementation of income endpoints
2. **backend/test_income_manual.py** - Manual test script
3. **backend/INCOME_IMPLEMENTATION.md** - This documentation file

## Dependencies

No new dependencies required. Uses existing:
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Decimal (Python standard library)

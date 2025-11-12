# Family Budget Tracker - API Documentation

Complete API reference for the Family Budget Tracker REST API.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Error Handling](#error-handling)
5. [Testing the API](#testing-the-api)

---

## Getting Started

### Base URL

```
Development: http://localhost:5000/api
Production: https://api.yourdomain.com/api
```

### Content Type

All requests and responses use JSON:
```
Content-Type: application/json
```

### Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production using Flask-Limiter.

---

## Authentication

### Overview

The API uses JWT (JSON Web Tokens) for authentication. Tokens are valid for 24 hours.

### Public Endpoints

These endpoints do not require authentication:
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### Protected Endpoints

All other endpoints require a valid JWT token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### Getting a Token

1. Register a user or login
2. Extract the `access_token` from the response
3. Include it in subsequent requests

**Example:**
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {...}
}

# Use token in subsequent requests
curl http://localhost:5000/api/expenses \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Token Expiration

Tokens expire after 24 hours. When a token expires:
- API returns `401 Unauthorized`
- User must login again to get a new token

---

## API Endpoints

---

## Authentication Endpoints

### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "jwt-token-here",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Get Current User
```http
GET /auth/me
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "shared_account_id": "uuid"
}
```

---

## Account Endpoints

### Invite Spouse
```http
POST /account/invite
```

**Request Body:**
```json
{
  "email": "spouse@example.com"
}
```

**Response:** `201 Created`

### Accept Invitation
```http
POST /account/accept-invite
```

**Request Body:**
```json
{
  "invitation_id": "uuid"
}
```

**Response:** `200 OK`

### Get Shared Account
```http
GET /account/shared
```

**Response:** `200 OK`
```json
{
  "shared_account": {
    "id": "uuid",
    "users": [
      {
        "id": "uuid",
        "email": "user@example.com",
        "name": "John Doe"
      }
    ]
  }
}
```

---

## Category Endpoints

### Get Categories
```http
GET /categories
```

**Response:** `200 OK`
```json
{
  "categories": [
    {
      "id": "uuid",
      "name": "Groceries",
      "is_custom": false
    }
  ]
}
```

### Create Category
```http
POST /categories
```

**Request Body:**
```json
{
  "name": "Custom Category"
}
```

**Response:** `201 Created`

---

## Expense Endpoints

### Get Expenses
```http
GET /expenses?category_id=uuid&start_date=2024-01-01&end_date=2024-12-31&user_id=uuid
```

**Query Parameters:**
- `category_id` (optional): Filter by category
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `user_id` (optional): Filter by user

**Response:** `200 OK`
```json
{
  "expenses": [
    {
      "id": "uuid",
      "amount": 50.00,
      "category_id": "uuid",
      "category_name": "Groceries",
      "date": "2024-01-15",
      "description": "Weekly shopping",
      "user_id": "uuid",
      "user_name": "John Doe"
    }
  ]
}
```

### Create Expense
```http
POST /expenses
```

**Request Body:**
```json
{
  "amount": 50.00,
  "category_id": "uuid",
  "date": "2024-01-15",
  "description": "Weekly shopping"
}
```

**Response:** `201 Created`

### Update Expense
```http
PUT /expenses/:id
```

**Request Body:**
```json
{
  "amount": 55.00,
  "description": "Updated description"
}
```

**Response:** `200 OK`

### Delete Expense
```http
DELETE /expenses/:id
```

**Response:** `200 OK`

### Get Expense Summary
```http
GET /expenses/summary?start_date=2024-01-01&end_date=2024-12-31
```

**Response:** `200 OK`
```json
{
  "summary": [
    {
      "category_id": "uuid",
      "category_name": "Groceries",
      "total_amount": 500.00,
      "percentage": 25.5,
      "expense_count": 10
    }
  ]
}
```

---

## Budget Endpoints

### Get Budgets
```http
GET /budgets
```

**Response:** `200 OK`

### Create Budget
```http
POST /budgets
```

**Request Body:**
```json
{
  "category_id": "uuid",
  "limit_amount": 500.00,
  "period": "monthly"
}
```

**Response:** `201 Created`

### Update Budget
```http
PUT /budgets/:id
```

**Response:** `200 OK`

### Delete Budget
```http
DELETE /budgets/:id
```

**Response:** `200 OK`

### Get Budget Status
```http
GET /budgets/status
```

**Response:** `200 OK`
```json
{
  "status": [
    {
      "category_name": "Groceries",
      "budget_limit": 500.00,
      "spent": 350.00,
      "remaining": 150.00,
      "percentage_used": 70.0,
      "status": "warning"
    }
  ]
}
```

---

## Credit Card Endpoints

### Get Credit Cards
```http
GET /credit-cards
```

**Response:** `200 OK`

### Create Credit Card
```http
POST /credit-cards
```

**Request Body:**
```json
{
  "name": "Chase Sapphire",
  "credit_limit": 5000.00,
  "current_balance": 1200.00
}
```

**Response:** `201 Created`

### Update Credit Card
```http
PUT /credit-cards/:id
```

**Response:** `200 OK`

### Create Transaction
```http
POST /credit-cards/:id/transactions
```

**Request Body:**
```json
{
  "amount": 100.00,
  "type": "payment",
  "date": "2024-01-15",
  "description": "Monthly payment"
}
```

**Response:** `201 Created`

---

## Installment Endpoints

### Get Installments
```http
GET /installments
```

**Response:** `200 OK`

### Create Installment
```http
POST /installments
```

**Request Body:**
```json
{
  "total_amount": 1200.00,
  "number_of_payments": 12,
  "start_date": "2024-01-01",
  "description": "iPhone 15 Pro"
}
```

**Response:** `201 Created`

### Mark Payment
```http
POST /installments/:id/pay
```

**Response:** `200 OK`

---

## Savings Goal Endpoints

### Get Savings Goals
```http
GET /savings-goals
```

**Response:** `200 OK`

### Create Savings Goal
```http
POST /savings-goals
```

**Request Body:**
```json
{
  "name": "Emergency Fund",
  "target_amount": 10000.00,
  "target_date": "2024-12-31"
}
```

**Response:** `201 Created`

### Update Savings Goal
```http
PUT /savings-goals/:id
```

**Response:** `200 OK`

### Add Contribution
```http
POST /savings-goals/:id/contributions
```

**Request Body:**
```json
{
  "amount": 500.00,
  "date": "2024-01-15"
}
```

**Response:** `201 Created`

---

## Income Endpoints

### Get Monthly Incomes
```http
GET /income?month=1&year=2024
```

**Response:** `200 OK`

### Create Monthly Income
```http
POST /income
```

**Request Body:**
```json
{
  "month": 1,
  "year": 2024,
  "amount": 5000.00
}
```

**Response:** `201 Created`

### Update Monthly Income
```http
PUT /income/:id
```

**Response:** `200 OK`

---

## Dashboard Endpoint

### Get Dashboard Data
```http
GET /dashboard
```

**Response:** `200 OK`
```json
{
  "total_expenses": 2500.00,
  "monthly_income": 5000.00,
  "net_income": 2500.00,
  "budget_status": [...],
  "recent_expenses": [...],
  "upcoming_installments": [...],
  "month_over_month_comparison": {
    "current_month": 2500.00,
    "previous_month": 2300.00,
    "percentage_change": 8.7
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid request format"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Access denied"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 409 Conflict
```json
{
  "error": "Conflict",
  "message": "Resource already exists"
}
```

### 422 Validation Error
```json
{
  "error": "Validation Error",
  "message": "Invalid input data"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

---

---

## Testing the API

### Using cURL

**Register a user:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Create an expense:**
```bash
TOKEN="your-jwt-token-here"

curl -X POST http://localhost:5000/api/expenses \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "category_id": "category-uuid",
    "date": "2024-01-15",
    "description": "Grocery shopping"
  }'
```

**Get expenses:**
```bash
curl http://localhost:5000/api/expenses \
  -H "Authorization: Bearer $TOKEN"
```

### Using Postman

1. **Import Collection:**
   - Create a new collection: "Family Budget Tracker"
   - Set base URL variable: `{{base_url}}` = `http://localhost:5000/api`

2. **Setup Authentication:**
   - Collection → Authorization → Type: Bearer Token
   - Token: `{{access_token}}`

3. **Create Requests:**
   - Add requests for each endpoint
   - Use variables for dynamic values

4. **Environment Variables:**
   ```json
   {
     "base_url": "http://localhost:5000/api",
     "access_token": "",
     "user_id": "",
     "shared_account_id": ""
   }
   ```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@example.com",
    "password": "password123"
})
token = response.json()["access_token"]

# Create expense
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/expenses", 
    headers=headers,
    json={
        "amount": 50.00,
        "category_id": "category-uuid",
        "date": "2024-01-15",
        "description": "Grocery shopping"
    }
)
print(response.json())

# Get expenses
response = requests.get(f"{BASE_URL}/expenses", headers=headers)
print(response.json())
```

### Using JavaScript/Axios

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:5000/api';
let token = '';

// Register
async function register() {
  const response = await axios.post(`${BASE_URL}/auth/register`, {
    email: 'test@example.com',
    password: 'password123',
    name: 'Test User'
  });
  console.log(response.data);
}

// Login
async function login() {
  const response = await axios.post(`${BASE_URL}/auth/login`, {
    email: 'test@example.com',
    password: 'password123'
  });
  token = response.data.access_token;
  return token;
}

// Create expense
async function createExpense() {
  const response = await axios.post(`${BASE_URL}/expenses`, {
    amount: 50.00,
    category_id: 'category-uuid',
    date: '2024-01-15',
    description: 'Grocery shopping'
  }, {
    headers: { Authorization: `Bearer ${token}` }
  });
  console.log(response.data);
}

// Get expenses
async function getExpenses() {
  const response = await axios.get(`${BASE_URL}/expenses`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  console.log(response.data);
}

// Run
(async () => {
  await register();
  await login();
  await createExpense();
  await getExpenses();
})();
```

---

## Additional Information

### Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting in production using Flask-Limiter.

**Example implementation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/expenses")
@limiter.limit("10 per minute")
def get_expenses():
    pass
```

### Pagination

Currently not implemented. All list endpoints return all results. Consider adding pagination for large datasets.

**Recommended implementation:**
```
GET /api/expenses?page=1&per_page=20
```

**Response:**
```json
{
  "expenses": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

### API Versioning

API version: v1 (implicit in base URL)

Future versions can be added as `/api/v2/...`

### CORS Configuration

CORS is configured to allow requests from the frontend domain. Update `CORS_ORIGINS` environment variable to add additional domains.

```bash
# Development
CORS_ORIGINS=http://localhost:3000

# Production
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## Related Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Environment setup instructions
- [DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md) - Database management
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide

---

**Last Updated:** November 2024  
**API Version:** 1.0

# Family Budget Tracker

A collaborative budget tracking application for couples to manage household finances together.

## 🎯 Overview

Complete full-stack application for managing family finances with real-time collaboration between spouses.

## ✨ Features

✅ **User Authentication** - Secure JWT-based authentication
✅ **Account Sharing** - Invite spouse to share budget data
✅ **Expense Tracking** - Record and categorize expenses with filtering
✅ **Budget Management** - Set limits with 80% warning and 100% alert indicators
✅ **Credit Card Tracking** - Monitor balances, limits, and transactions
✅ **Installment Tracking** - Track payment plans with automatic calculations
✅ **Savings Goals** - Set targets with progress tracking and suggested contributions
✅ **Income Tracking** - Record monthly income with dashboard integration
✅ **Interactive Dashboard** - Visual charts and summaries
✅ **Responsive Design** - Works on mobile, tablet, and desktop
✅ **Real-time Collaboration** - All data shared between spouses

## Project Structure

```
family-budget-tracker/
├── backend/          # Flask REST API
│   ├── app/          # Application code
│   ├── migrations/   # Database migrations
│   ├── config.py     # Configuration
│   └── run.py        # Entry point
├── frontend/         # React + TypeScript frontend
│   ├── src/          # Source code
│   └── public/       # Static assets
└── README.md
```

## 📚 Documentation

### Documentation Structure

This project includes comprehensive documentation organized by purpose:

**Getting Started** → **Development** → **Deployment** → **Maintenance**

### Getting Started
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete step-by-step setup instructions for local development
  - Prerequisites installation (Python, Node.js, PostgreSQL)
  - Project setup and configuration
  - Database creation and initialization
  - Running the application locally

### Development
- **[DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md)** - Database migration management
  - Creating and applying migrations
  - Common migration tasks
  - Production migration strategy
  - Troubleshooting migration issues

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
  - Authentication endpoints
  - All API endpoints with request/response examples
  - Error handling
  - Testing the API with cURL, Postman, and code examples

### Deployment

**🚀 New to AWS?** Start here:
- **[AWS_GETTING_STARTED.md](AWS_GETTING_STARTED.md)** - Complete AWS deployment walkthrough
  - AWS account setup and configuration
  - Step-by-step Elastic Beanstalk deployment
  - Database setup with RDS
  - Frontend deployment to S3
  - Complete in ~30-45 minutes

- **[AWS_QUICK_START.md](AWS_QUICK_START.md)** - Fast track deployment commands
  - Copy-paste commands for quick deployment
  - Minimal explanation, maximum speed
  - Perfect for experienced AWS users

**📖 Comprehensive Guides:**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
  - Environment setup for production
  - AWS deployment options (Elastic Beanstalk, EC2, ECS)
  - Database setup with AWS RDS
  - Security and monitoring
  - Troubleshooting common issues
  - Quick reference commands

- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment checklist
  - Pre-deployment preparation
  - Infrastructure setup
  - Testing procedures
  - Post-deployment verification

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### Setup in 5 Minutes

1. **Clone and setup database:**
   ```bash
   git clone <repository-url>
   cd family-budget-tracker
   
   # Create PostgreSQL database
   psql -U postgres -c "CREATE DATABASE budget_tracker;"
   ```

2. **Setup backend:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Edit with your database credentials
   flask db upgrade
   python run.py
   ```

3. **Setup frontend (new terminal):**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```

4. **Open browser:**
   ```
   http://localhost:3000
   ```

**For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

## Development

- Backend API: `http://localhost:5000`
- Frontend: `http://localhost:3000`
- Frontend proxies API requests to backend automatically

## API Endpoints Overview

The application provides a comprehensive REST API. Here are the main endpoint categories:

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login (returns JWT token)
- `GET /api/auth/me` - Get current user info

### Account Management
- `POST /api/account/invite` - Invite spouse to shared account
- `POST /api/account/accept-invite` - Accept invitation
- `GET /api/account/shared` - Get shared account details

### Expenses
- `GET /api/expenses` - List expenses (with filters)
- `POST /api/expenses` - Create expense
- `PUT /api/expenses/:id` - Update expense
- `DELETE /api/expenses/:id` - Delete expense
- `GET /api/expenses/summary` - Get spending summary by category

### Budgets
- `GET /api/budgets` - List budget limits
- `POST /api/budgets` - Create budget limit
- `PUT /api/budgets/:id` - Update budget limit
- `GET /api/budgets/status` - Get budget status with warnings

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create custom category

### Credit Cards
- `GET /api/credit-cards` - List credit cards
- `POST /api/credit-cards` - Add credit card
- `POST /api/credit-cards/:id/transactions` - Record payment/charge

### Installments
- `GET /api/installments` - List installments
- `POST /api/installments` - Create installment plan
- `POST /api/installments/:id/pay` - Mark payment as completed

### Savings Goals
- `GET /api/savings-goals` - List savings goals
- `POST /api/savings-goals` - Create savings goal
- `POST /api/savings-goals/:id/contributions` - Add contribution

### Income
- `GET /api/income` - Get monthly income records
- `POST /api/income` - Set monthly income
- `PUT /api/income/:id` - Update monthly income

### Dashboard
- `GET /api/dashboard` - Get dashboard summary (expenses, income, budget status, recent activity)

**For detailed API documentation with request/response examples, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

## Tech Stack

### Backend
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-JWT-Extended
- Flask-Migrate

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Chart.js

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete AWS deployment instructions.

### Quick Deploy Options

1. **AWS Elastic Beanstalk** (Recommended for beginners)
   - Backend: Elastic Beanstalk
   - Frontend: S3 + CloudFront
   - Database: RDS PostgreSQL

2. **AWS EC2** (More control)
   - Backend: EC2 with Nginx
   - Frontend: S3 + CloudFront
   - Database: RDS PostgreSQL

3. **AWS ECS** (Containerized)
   - Backend: ECS Fargate
   - Frontend: S3 + CloudFront
   - Database: RDS PostgreSQL

**Estimated AWS Cost:** ~$25-35/month (Free tier eligible for 12 months)

### Additional Documentation

See the documentation links at the top of this README for:
- Complete setup instructions
- Database migration guide
- API endpoint reference
- AWS deployment strategies

## License

Private project for personal use.

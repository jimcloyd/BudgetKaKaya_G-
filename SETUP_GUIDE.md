# Family Budget Tracker - Setup Guide

Complete step-by-step guide for setting up the Family Budget Tracker application from scratch.

## Table of Contents

1. [Prerequisites Installation](#prerequisites-installation)
2. [Project Setup](#project-setup)
3. [Database Configuration](#database-configuration)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Verification](#verification)

---

## Prerequisites Installation

### 1. Install Python 3.9+

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

**Mac:**
```bash
# Using Homebrew
brew install python@3.9

# Verify
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
python3 --version
```

### 2. Install Node.js 18+

**Windows:**
1. Download from [nodejs.org](https://nodejs.org/)
2. Run installer
3. Follow installation wizard
4. Verify:
   ```bash
   node --version
   npm --version
   ```

**Mac:**
```bash
# Using Homebrew
brew install node@18

# Verify
node --version
npm --version
```

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

### 3. Install PostgreSQL 14+

**Windows:**
1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer
3. Remember the password you set for `postgres` user
4. Default port: 5432
5. Verify:
   ```bash
   psql --version
   ```

**Mac:**
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14

# Verify
psql --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify
psql --version
```

### 4. Install Git

**Windows:**
- Download from [git-scm.com](https://git-scm.com/download/win)
- Run installer with default options

**Mac:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

Verify:
```bash
git --version
```

---

## Project Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>
cd family-budget-tracker

# Check project structure
ls -la
```

You should see:
```
family-budget-tracker/
├── backend/
├── frontend/
├── README.md
├── DEPLOYMENT.md
└── ...
```

---

## Database Configuration

### 1. Start PostgreSQL Service

**Windows:**
```bash
# Check if running
sc query postgresql-x64-14

# Start if not running
sc start postgresql-x64-14
```

**Mac:**
```bash
brew services start postgresql@14
```

**Linux:**
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### 2. Create Database

**Option A: Using psql (Command Line)**

```bash
# Connect to PostgreSQL
# Windows/Linux
psql -U postgres

# Mac (if no password set)
psql postgres

# Inside psql, run:
CREATE DATABASE budget_tracker;

# Create a dedicated user (recommended)
CREATE USER budget_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE budget_tracker TO budget_user;

# List databases to verify
\l

# Exit psql
\q
```

**Option B: Using pgAdmin (GUI)**

1. Open pgAdmin
2. Connect to PostgreSQL server
3. Right-click "Databases" → "Create" → "Database"
4. Database name: `budget_tracker`
5. Owner: `postgres` (or `budget_user` if created)
6. Click "Save"

### 3. Verify Database Connection

```bash
# Test connection
psql -U postgres -d budget_tracker -c "SELECT version();"

# Or with custom user
psql -U budget_user -d budget_tracker -c "SELECT version();"
```

---

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Flask-Migrate (database migrations)
- Flask-JWT-Extended (authentication)
- PostgreSQL adapter
- And more...

### 5. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Windows (if cp doesn't work)
copy .env.example .env
```

Edit `.env` file with your settings:

```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/budget_tracker

# Or with custom user
# DATABASE_URL=postgresql://budget_user:your_secure_password@localhost:5432/budget_tracker

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# JWT Configuration
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=86400

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Server Configuration
PORT=5000
HOST=0.0.0.0
```

**Important:** Replace `your_password` with your actual PostgreSQL password.

### 6. Generate Secure Keys (for Production)

```python
# Run in Python
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

Copy the generated keys to your `.env` file.

### 7. Initialize Database Migrations

```bash
# Initialize migrations (if not already done)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations to create tables
flask db upgrade
```

### 8. Verify Database Tables

```bash
# Check tables were created
psql -U postgres -d budget_tracker -c "\dt"
```

You should see tables:
- users
- shared_accounts
- invitations
- categories
- expenses
- budget_limits
- credit_cards
- credit_card_transactions
- installments
- savings_goals
- savings_contributions
- monthly_income
- alembic_version

### 9. Test Backend Server

```bash
# Start the server
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Test the API:
```bash
# In a new terminal
curl http://localhost:5000/api/auth/me
```

Expected response: `{"msg":"Missing Authorization Header"}` (this is correct!)

**Keep the backend server running** and open a new terminal for frontend setup.

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
# Open a new terminal
cd family-budget-tracker/frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This installs:
- React (UI library)
- TypeScript (type safety)
- Vite (build tool)
- React Router (routing)
- Axios (HTTP client)
- Chart.js (charts)
- Tailwind CSS (styling)

Installation may take a few minutes.

### 3. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Windows (if cp doesn't work)
copy .env.example .env
```

Edit `.env` file:

```bash
# Development
VITE_API_BASE_URL=http://localhost:5000/api
```

**Note:** The `VITE_` prefix is required for Vite to expose the variable to the client.

### 4. Test Frontend Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

---

## Running the Application

### Start Both Servers

You need **two terminal windows**:

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application

Open your browser and go to:
```
http://localhost:3000
```

You should see the Family Budget Tracker login/register page.

---

## Verification

### 1. Test User Registration

1. Open http://localhost:3000
2. Click "Register" or "Sign Up"
3. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
4. Click "Register"
5. You should be redirected to the dashboard

### 2. Verify Database Entry

```bash
# Check user was created
psql -U postgres -d budget_tracker -c "SELECT id, email, name FROM users;"
```

You should see your test user.

### 3. Test API Endpoints

**Register a user:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test2@example.com","password":"password123","name":"Test User 2"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test2@example.com","password":"password123"}'
```

You should receive a JWT token.

### 4. Test Frontend Features

1. **Login** with your test account
2. **Create an expense**:
   - Go to Expenses
   - Click "Add Expense"
   - Fill in details
   - Save
3. **Set a budget**:
   - Go to Budgets
   - Set a limit for a category
4. **View dashboard**:
   - Should show your expense
   - Should show budget status

---

## Common Setup Issues

### Issue: "python: command not found"

**Solution:**
- Windows: Use `python` instead of `python3`
- Mac/Linux: Use `python3` instead of `python`
- Or add Python to PATH

### Issue: "psql: command not found"

**Solution:**
- Add PostgreSQL bin directory to PATH
- Windows: `C:\Program Files\PostgreSQL\14\bin`
- Mac: Usually automatic with Homebrew
- Linux: `sudo apt install postgresql-client`

### Issue: "pip: command not found"

**Solution:**
```bash
# Windows
python -m pip install --upgrade pip

# Mac/Linux
python3 -m pip install --upgrade pip
```

### Issue: "Permission denied" when activating venv

**Windows PowerShell:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Issue: "Cannot connect to database"

**Solution:**
1. Check PostgreSQL is running
2. Verify DATABASE_URL in `.env`
3. Test connection: `psql -U postgres -d budget_tracker`
4. Check password is correct

### Issue: "Module not found" errors

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## Next Steps

After successful setup:

1. **Read the API Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. **Explore the Features**: Try all functionality
3. **Review the Code**: Understand the architecture
4. **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Quick Reference

### Start Development

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Stop Development

- Press `Ctrl+C` in both terminals
- Deactivate venv: `deactivate`

### Database Commands

```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade

# Check current version
flask db current
```

### Useful Commands

```bash
# Backend
pip list                    # List installed packages
pip freeze > requirements.txt  # Update requirements
flask routes                # List all API routes

# Frontend
npm list                    # List installed packages
npm run build              # Build for production
npm run preview            # Preview production build

# Database
psql -U postgres -d budget_tracker  # Connect to database
\dt                        # List tables
\d table_name             # Describe table
```

---

## Support

If you encounter issues:

1. Check this guide's "Common Setup Issues" section
2. Review error messages carefully
3. Check application logs
4. Verify all prerequisites are installed
5. Ensure all environment variables are set correctly

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md).

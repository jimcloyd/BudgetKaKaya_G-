# Testing the Family Budget Tracker

## Quick Test Setup

I've prepared the environment files for you. Follow these steps to test the application:

### Step 1: Install Backend Dependencies

Open a terminal and run:

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Create Database

Make sure PostgreSQL is running, then create the database:

```powershell
# Option 1: Using psql
psql -U postgres -c "CREATE DATABASE budget_tracker;"

# Option 2: Using pgAdmin
# Open pgAdmin → Right-click Databases → Create → Database
# Name: budget_tracker
```

### Step 3: Run Database Migrations

```powershell
# Still in backend directory with venv activated
flask db upgrade
```

### Step 4: Start Backend Server

```powershell
# In backend directory
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 5: Install Frontend Dependencies

Open a NEW terminal and run:

```powershell
cd frontend
npm install
```

### Step 6: Start Frontend Server

```powershell
# In frontend directory
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 500 ms
  ➜  Local:   http://localhost:3000/
```

### Step 7: Test the Application

1. Open your browser to: **http://localhost:3000**

2. You should see the Family Budget Tracker login/register page

3. **Test User Registration:**
   - Click "Register" or "Sign Up"
   - Fill in:
     - Name: Test User
     - Email: test@example.com
     - Password: password123
   - Click "Register"
   - You should be redirected to the dashboard

4. **Test Features:**
   - ✅ Create an expense
   - ✅ Set a budget limit
   - ✅ View dashboard
   - ✅ Invite spouse (use a different email)
   - ✅ Create savings goal
   - ✅ Add credit card
   - ✅ Track installment

## Quick API Test

Test the API directly with curl:

```powershell
# Test registration
curl -X POST http://localhost:5000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test2@example.com\",\"password\":\"password123\",\"name\":\"Test User 2\"}'

# Test login
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"email\":\"test2@example.com\",\"password\":\"password123\"}'
```

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `sc query postgresql-x64-14`
- Check database exists: `psql -U postgres -l | findstr budget_tracker`
- Check .env file has correct DATABASE_URL

### Frontend won't start
- Delete node_modules and reinstall: `rm -r node_modules; npm install`
- Check .env file exists in frontend directory

### Database connection error
- Verify PostgreSQL password in backend/.env
- Default is usually `postgres` for both username and password
- Update DATABASE_URL if different

### CORS errors
- Make sure backend CORS_ORIGINS includes http://localhost:3000
- Restart backend server after changing .env

## What's Already Set Up

✅ Backend .env file created with development settings
✅ Frontend .env file created
✅ Backend virtual environment created
✅ Configuration files ready

## Next Steps After Testing

Once you've tested the application locally:
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- See [DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md) for database management

## Need Help?

Check the comprehensive guides:
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide

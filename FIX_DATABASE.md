# Fix Database Issue - Run Migrations

## Problem
The database tables haven't been created yet, so account registration fails with a 500 error.

## Solution
Run the database migrations to create all the necessary tables.

---

## Steps to Fix

### Step 1: Get Your Database Password

You need the password you set when creating the RDS database. If you don't remember it, you'll need to reset it in AWS Console.

### Step 2: Run These Commands

Open PowerShell and run:

```powershell
# Navigate to backend
cd F:\MyProject\BudgetKaKaya_G-\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Set database connection (REPLACE YOUR_PASSWORD with actual password)
$env:DATABASE_URL = "postgresql://budget_admin:YOUR_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
$env:FLASK_APP = "run.py"

# Run migrations
flask db upgrade
```

### Step 3: Verify

You should see output like:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Initial migration
```

---

## Alternative: Quick Fix Command

Copy and paste this (replace YOUR_PASSWORD):

```powershell
cd F:\MyProject\BudgetKaKaya_G-\backend; .\venv\Scripts\Activate.ps1; $env:DATABASE_URL = "postgresql://budget_admin:YOUR_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"; $env:FLASK_APP = "run.py"; flask db upgrade
```

---

## After Running Migrations

1. Go back to the website: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com
2. Try creating an account again
3. It should work now!

---

## If You Don't Remember the Database Password

### Option 1: Check your notes
Look for where you saved it when creating the RDS database.

### Option 2: Reset the password
1. Go to AWS Console: https://console.aws.amazon.com/rds
2. Click on "budget-tracker-db"
3. Click "Modify"
4. Scroll to "Settings" → "New master password"
5. Enter a new password
6. Click "Continue" → "Modify DB instance"
7. Wait 5-10 minutes for the change to apply
8. Use the new password in the commands above

---

## Troubleshooting

### Error: "psycopg2" not found
```powershell
pip install psycopg2-binary
```

### Error: "flask: command not found"
Make sure you activated the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

### Error: Connection timeout
- Check your internet connection
- Verify the RDS database is running in AWS Console
- Make sure the security group allows your IP address

---

**Once migrations are complete, your app will work perfectly!** ✅

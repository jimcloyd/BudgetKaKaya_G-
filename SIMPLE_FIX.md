# Simple Fix - Create Database Tables

## The Problem
The database exists but has NO TABLES. That's why you can't create accounts.

## The Solution
Run these commands ONE BY ONE in PowerShell:

### Step 1: Go to backend folder
```powershell
cd F:\MyProject\BudgetKaKaya_G-\backend
```

### Step 2: Set your database password
**Replace YOUR_PASSWORD with your actual RDS password:**
```powershell
$env:DATABASE_URL = "postgresql://budget_admin:YOUR_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
$env:FLASK_APP = "run.py"
```

### Step 3: Run migrations to create tables
```powershell
python -m flask db upgrade
```

You should see:
```
INFO  [alembic.runtime.migration] Running upgrade  -> xxxxx, Initial migration
```

### Step 4: Create your user
```powershell
python -c "from app import create_app, db; from app.models import User; import bcrypt; app = create_app(); ctx = app.app_context(); ctx.push(); password_hash = bcrypt.hashpw('jimcloyd'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'); user = User(email='jimcloyd@gmail.com', password=password_hash, name='Jim Cloyd'); db.session.add(user); db.session.commit(); print('User created!'); ctx.pop()"
```

### Step 5: Test it
Open: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com

Login with:
- Email: jimcloyd@gmail.com
- Password: jimcloyd

---

## All Commands in One Block

Copy and paste this (replace YOUR_PASSWORD):

```powershell
cd F:\MyProject\BudgetKaKaya_G-\backend
$env:DATABASE_URL = "postgresql://budget_admin:YOUR_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
$env:FLASK_APP = "run.py"
python -m flask db upgrade
python -c "from app import create_app, db; from app.models import User; import bcrypt; app = create_app(); ctx = app.app_context(); ctx.push(); password_hash = bcrypt.hashpw('jimcloyd'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'); user = User(email='jimcloyd@gmail.com', password=password_hash, name='Jim Cloyd'); db.session.add(user); db.session.commit(); print('User created!'); ctx.pop()"
```

---

## What This Does

1. **Creates all database tables**: users, expenses, categories, budgets, credit_cards, installments, savings_goals, monthly_income, etc.
2. **Creates your test user**: jimcloyd@gmail.com
3. **Makes the app work**: You and your wife can now register and use the app!

---

**After this, the app will be fully functional!** ✅

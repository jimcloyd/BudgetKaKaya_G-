# Family Budget Tracker - Backend

Flask-based REST API for the Family Budget Tracker application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the database URL and secret keys

5. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the development server:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Database Setup

Make sure PostgreSQL is installed and running. Create a database:
```sql
CREATE DATABASE family_budget_tracker;
```

## API Documentation

API endpoints will be documented using Swagger UI (available after implementation).

# Database Migrations

This directory contains the database migration files for the Family Budget Tracker application.

## Setup

Flask-Migrate has been initialized and configured. The initial migration (001_initial_migration.py) creates all the database tables.

## Prerequisites

Before running migrations, ensure you have:

1. PostgreSQL installed and running
2. Created a database named `family_budget_tracker`
3. Installed psycopg2-binary: `pip install psycopg2-binary`
4. Set up your `.env` file with the correct DATABASE_URL

## Running Migrations

To apply the migrations to your database:

```bash
# Set the Flask app environment variable
export FLASK_APP=run.py  # On Windows: set FLASK_APP=run.py

# Apply migrations
flask db upgrade
```

## Creating New Migrations

When you make changes to the models, create a new migration:

```bash
# Generate a new migration automatically
flask db migrate -m "Description of changes"

# Review the generated migration file in migrations/versions/

# Apply the migration
flask db upgrade
```

## Downgrading Migrations

To rollback the last migration:

```bash
flask db downgrade
```

## Migration History

To see the migration history:

```bash
flask db history
```

## Current Database Schema

The initial migration creates the following tables:

- `shared_accounts` - Shared household accounts
- `users` - User accounts
- `invitations` - Spouse invitation tracking
- `categories` - Expense categories
- `expenses` - Expense records
- `budget_limits` - Budget limits per category
- `credit_cards` - Credit card information
- `credit_card_transactions` - Credit card transactions
- `installments` - Installment payment plans
- `savings_goals` - Savings goals
- `savings_contributions` - Savings contributions
- `monthly_income` - Monthly income records

All tables use UUID (String(36)) as primary keys and include appropriate foreign key relationships.

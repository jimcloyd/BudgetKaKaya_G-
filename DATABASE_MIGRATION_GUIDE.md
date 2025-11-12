# Database Migration Guide

Comprehensive guide for managing database migrations in the Family Budget Tracker application using Flask-Migrate (Alembic).

## Table of Contents

1. [Overview](#overview)
2. [Migration Basics](#migration-basics)
3. [Common Migration Tasks](#common-migration-tasks)
4. [Production Migration Strategy](#production-migration-strategy)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

---

## Overview

### What are Database Migrations?

Database migrations are version-controlled changes to your database schema. They allow you to:
- Track database schema changes over time
- Apply changes consistently across environments
- Rollback changes if needed
- Collaborate with team members on schema changes

### Migration Tools

- **Flask-Migrate**: Flask extension for Alembic
- **Alembic**: Database migration tool for SQLAlchemy
- **SQLAlchemy**: Python ORM (Object-Relational Mapping)

### Migration Files Location

```
backend/
├── migrations/
│   ├── versions/
│   │   ├── 001_initial_migration.py
│   │   ├── 002_add_credit_cards.py
│   │   └── ...
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
```

---

## Migration Basics

### Initialize Migrations (First Time Only)

```bash
cd backend
flask db init
```

This creates the `migrations` directory structure.

**Note:** Only run this once per project. The migrations folder should be committed to Git.

### Create a Migration

After modifying models in `app/models.py`:

```bash
flask db migrate -m "Description of changes"
```

Example:
```bash
flask db migrate -m "Add credit card limit field"
```

This generates a migration file in `migrations/versions/`.

### Review the Migration

**Always review** the generated migration before applying:

```bash
# Find the latest migration file
ls -lt migrations/versions/

# Open and review
cat migrations/versions/xxxxx_description.py
```

Check:
- ✅ Upgrade function creates/modifies tables correctly
- ✅ Downgrade function reverses the changes
- ✅ No unintended changes
- ✅ Data migrations are safe

### Apply Migrations

```bash
flask db upgrade
```

This applies all pending migrations to the database.

### Rollback Migrations

```bash
# Rollback one migration
flask db downgrade

# Rollback to specific version
flask db downgrade <revision_id>

# Rollback all migrations
flask db downgrade base
```

### Check Migration Status

```bash
# Show current version
flask db current

# Show migration history
flask db history

# Show pending migrations
flask db heads
```

---

## Common Migration Tasks

### 1. Adding a New Table

**Step 1: Define Model**

Edit `backend/app/models.py`:

```python
class NewTable(db.Model):
    __tablename__ = 'new_table'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Step 2: Create Migration**

```bash
flask db migrate -m "Add new_table"
```

**Step 3: Review Migration**

```python
# migrations/versions/xxxxx_add_new_table.py
def upgrade():
    op.create_table('new_table',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('new_table')
```

**Step 4: Apply Migration**

```bash
flask db upgrade
```

### 2. Adding a Column

**Step 1: Modify Model**

```python
class Expense(db.Model):
    # ... existing columns ...
    notes = db.Column(db.Text)  # New column
```

**Step 2: Create and Apply Migration**

```bash
flask db migrate -m "Add notes column to expenses"
flask db upgrade
```

**Generated Migration:**

```python
def upgrade():
    op.add_column('expenses', sa.Column('notes', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('expenses', 'notes')
```

### 3. Modifying a Column

**Step 1: Modify Model**

```python
class User(db.Model):
    # Change from String(100) to String(255)
    name = db.Column(db.String(255), nullable=False)
```

**Step 2: Create Migration**

```bash
flask db migrate -m "Increase user name length"
```

**Step 3: Review and Modify if Needed**

```python
def upgrade():
    # Alembic might not detect this automatically
    # You may need to add manually:
    op.alter_column('users', 'name',
                    existing_type=sa.String(100),
                    type_=sa.String(255),
                    existing_nullable=False)

def downgrade():
    op.alter_column('users', 'name',
                    existing_type=sa.String(255),
                    type_=sa.String(100),
                    existing_nullable=False)
```

**Step 4: Apply Migration**

```bash
flask db upgrade
```

### 4. Removing a Column

**Step 1: Remove from Model**

```python
class Expense(db.Model):
    # Remove the 'notes' column
    # notes = db.Column(db.Text)  # Commented out or deleted
    pass
```

**Step 2: Create Migration**

```bash
flask db migrate -m "Remove notes column from expenses"
```

**Step 3: Review Migration**

```python
def upgrade():
    op.drop_column('expenses', 'notes')

def downgrade():
    op.add_column('expenses', sa.Column('notes', sa.Text(), nullable=True))
```

**⚠️ Warning:** Dropping columns deletes data permanently!

**Step 4: Apply Migration**

```bash
flask db upgrade
```

### 5. Adding a Foreign Key

**Step 1: Modify Model**

```python
class Expense(db.Model):
    # ... existing columns ...
    payment_method_id = db.Column(db.String(36), db.ForeignKey('payment_methods.id'))
    payment_method = db.relationship('PaymentMethod', backref='expenses')
```

**Step 2: Create Migration**

```bash
flask db migrate -m "Add payment method to expenses"
```

**Step 3: Review Migration**

```python
def upgrade():
    op.add_column('expenses', sa.Column('payment_method_id', sa.String(36), nullable=True))
    op.create_foreign_key('fk_expenses_payment_method', 
                         'expenses', 'payment_methods',
                         ['payment_method_id'], ['id'])

def downgrade():
    op.drop_constraint('fk_expenses_payment_method', 'expenses', type_='foreignkey')
    op.drop_column('expenses', 'payment_method_id')
```

### 6. Data Migration

When you need to migrate existing data:

**Example: Populate default categories**

```python
# migrations/versions/xxxxx_add_default_categories.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import uuid

def upgrade():
    # Define table structure for data migration
    categories = table('categories',
        column('id', sa.String),
        column('name', sa.String),
        column('shared_account_id', sa.String),
        column('is_custom', sa.Boolean)
    )
    
    # Get all shared accounts
    conn = op.get_bind()
    shared_accounts = conn.execute(sa.text("SELECT id FROM shared_accounts")).fetchall()
    
    # Insert default categories for each shared account
    default_categories = ['Groceries', 'Utilities', 'Transportation', 
                         'Entertainment', 'Healthcare', 'Miscellaneous']
    
    for account in shared_accounts:
        for cat_name in default_categories:
            op.execute(
                categories.insert().values(
                    id=str(uuid.uuid4()),
                    name=cat_name,
                    shared_account_id=account[0],
                    is_custom=False
                )
            )

def downgrade():
    # Remove default categories
    op.execute("DELETE FROM categories WHERE is_custom = false")
```

### 7. Renaming a Table

```python
def upgrade():
    op.rename_table('old_table_name', 'new_table_name')

def downgrade():
    op.rename_table('new_table_name', 'old_table_name')
```

### 8. Adding an Index

```python
def upgrade():
    op.create_index('idx_expenses_date', 'expenses', ['date'])

def downgrade():
    op.drop_index('idx_expenses_date', 'expenses')
```

### 9. Adding a Unique Constraint

```python
def upgrade():
    op.create_unique_constraint('uq_user_email', 'users', ['email'])

def downgrade():
    op.drop_constraint('uq_user_email', 'users', type_='unique')
```

---

## Production Migration Strategy

### Pre-Migration Checklist

- [ ] Test migration on development database
- [ ] Test migration on staging database with production-like data
- [ ] Review migration code for correctness
- [ ] Backup production database
- [ ] Plan rollback strategy
- [ ] Schedule maintenance window (if needed)
- [ ] Notify users of potential downtime

### Backup Database

**Local PostgreSQL:**
```bash
pg_dump -U postgres budget_tracker > backup_$(date +%Y%m%d_%H%M%S).sql
```

**AWS RDS:**
```bash
pg_dump -h rds-endpoint.amazonaws.com \
        -U budget_admin \
        -d budget_tracker \
        -F c \
        -f backup_$(date +%Y%m%d_%H%M%S).dump
```

### Apply Migration to Production

**Option 1: Manual Deployment**

```bash
# SSH into production server
ssh user@production-server

# Navigate to application directory
cd /path/to/family-budget-tracker/backend

# Activate virtual environment
source venv/bin/activate

# Set production DATABASE_URL
export DATABASE_URL="postgresql://user:pass@rds-endpoint:5432/budget_tracker"

# Apply migrations
flask db upgrade

# Restart application
sudo systemctl restart budget-api
```

**Option 2: Elastic Beanstalk**

Create `.ebextensions/01_flask_migrate.config`:

```yaml
container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && flask db upgrade"
    leader_only: true
```

Deploy:
```bash
eb deploy
```

**Option 3: CI/CD Pipeline**

Example GitHub Actions workflow:

```yaml
# .github/workflows/deploy.yml
- name: Run Database Migrations
  run: |
    cd backend
    source venv/bin/activate
    export DATABASE_URL=${{ secrets.DATABASE_URL }}
    flask db upgrade
```

### Post-Migration Verification

```bash
# Check migration was applied
flask db current

# Verify tables exist
psql $DATABASE_URL -c "\dt"

# Check application logs
tail -f /var/log/budget-api.log

# Test API endpoints
curl https://api.yourdomain.com/api/auth/me
```

### Rollback Procedure

If migration fails:

```bash
# Rollback migration
flask db downgrade

# Or restore from backup
pg_restore -h rds-endpoint \
           -U budget_admin \
           -d budget_tracker \
           -c \
           backup_20241111_120000.dump

# Restart application
sudo systemctl restart budget-api
```

---

## Troubleshooting

### Issue: "Target database is not up to date"

**Cause:** Database is ahead of migration files

**Solution:**
```bash
# Check current version
flask db current

# Stamp database with current head
flask db stamp head
```

### Issue: "Can't locate revision identified by 'xxxxx'"

**Cause:** Migration file missing or database tracking corrupted

**Solution:**
```bash
# Check migration files exist
ls migrations/versions/

# If files exist, stamp to correct version
flask db stamp <revision_id>

# If files missing, restore from Git
git checkout migrations/versions/
```

### Issue: "relation already exists"

**Cause:** Table already exists in database

**Solution:**
```bash
# Option 1: Stamp database to skip this migration
flask db stamp head

# Option 2: Drop and recreate (DEVELOPMENT ONLY)
psql $DATABASE_URL -c "DROP TABLE table_name CASCADE;"
flask db upgrade
```

### Issue: "column does not exist"

**Cause:** Migration order issue or missing migration

**Solution:**
```bash
# Check migration history
flask db history

# Ensure all migrations are applied
flask db upgrade

# If migration is missing, create it
flask db migrate -m "Add missing column"
```

### Issue: "cannot drop table because other objects depend on it"

**Cause:** Foreign key constraints

**Solution:**
```python
# In migration, drop constraints first
def upgrade():
    op.drop_constraint('fk_constraint_name', 'table_name', type_='foreignkey')
    op.drop_table('table_name')

def downgrade():
    # Recreate table and constraints
    pass
```

### Issue: "Migration takes too long"

**Cause:** Large table or complex operation

**Solution:**
```python
# Add timeout and batch operations
def upgrade():
    # For large tables, use batch operations
    with op.batch_alter_table('large_table') as batch_op:
        batch_op.add_column(sa.Column('new_column', sa.String(100)))
    
    # Or add index concurrently (PostgreSQL)
    op.create_index('idx_name', 'table', ['column'], postgresql_concurrently=True)
```

---

## Best Practices

### 1. Always Review Generated Migrations

```bash
# After creating migration
flask db migrate -m "Description"

# Review the file
cat migrations/versions/xxxxx_description.py
```

### 2. Use Descriptive Migration Messages

```bash
# Good
flask db migrate -m "Add payment_method_id to expenses table"

# Bad
flask db migrate -m "Update"
```

### 3. Test Migrations Before Production

```bash
# Test on development
flask db upgrade
flask db downgrade
flask db upgrade

# Test on staging with production-like data
```

### 4. Keep Migrations Small and Focused

```bash
# Good: One logical change per migration
flask db migrate -m "Add email verification field"
flask db migrate -m "Add email verification index"

# Bad: Multiple unrelated changes
flask db migrate -m "Add various fields and indexes"
```

### 5. Never Modify Applied Migrations

Once a migration is applied to production:
- ❌ Don't modify the migration file
- ✅ Create a new migration to fix issues

### 6. Backup Before Migrations

```bash
# Always backup before production migrations
pg_dump -U postgres budget_tracker > backup_before_migration.sql
```

### 7. Use Transactions

Migrations run in transactions by default. For operations that can't run in transactions:

```python
def upgrade():
    # Disable transaction for this operation
    op.execute('CREATE INDEX CONCURRENTLY idx_name ON table (column)')

# In migration file header
# revision = 'xxxxx'
# down_revision = 'yyyyy'
# branch_labels = None
# depends_on = None
# transaction_per_migration = False  # Add this
```

### 8. Document Complex Migrations

```python
def upgrade():
    """
    This migration adds a payment_method_id column to expenses
    and populates it with default values for existing records.
    
    Steps:
    1. Add column (nullable)
    2. Populate with default value
    3. Make column non-nullable
    """
    # Add column
    op.add_column('expenses', sa.Column('payment_method_id', sa.String(36), nullable=True))
    
    # Populate existing records
    op.execute("UPDATE expenses SET payment_method_id = 'default-id' WHERE payment_method_id IS NULL")
    
    # Make non-nullable
    op.alter_column('expenses', 'payment_method_id', nullable=False)
```

### 9. Handle Data Carefully

```python
# Good: Safe data migration
def upgrade():
    # Add column as nullable first
    op.add_column('users', sa.Column('full_name', sa.String(255), nullable=True))
    
    # Populate from existing data
    op.execute("UPDATE users SET full_name = name WHERE full_name IS NULL")
    
    # Make non-nullable after population
    op.alter_column('users', 'full_name', nullable=False)

# Bad: Immediate non-nullable column
def upgrade():
    op.add_column('users', sa.Column('full_name', sa.String(255), nullable=False))
    # This will fail if table has existing rows!
```

### 10. Version Control Migrations

```bash
# Always commit migration files
git add migrations/versions/xxxxx_description.py
git commit -m "Add migration: description"
git push
```

---

## Quick Reference

### Common Commands

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback one migration
flask db downgrade

# Show current version
flask db current

# Show history
flask db history

# Stamp database
flask db stamp head
```

### Migration File Structure

```python
"""Description

Revision ID: xxxxx
Revises: yyyyy
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'xxxxx'
down_revision = 'yyyyy'
branch_labels = None
depends_on = None

def upgrade():
    # Changes to apply
    pass

def downgrade():
    # Changes to rollback
    pass
```

### Useful SQL Queries

```sql
-- Check migration version
SELECT * FROM alembic_version;

-- List all tables
\dt

-- Describe table structure
\d table_name

-- Check table size
SELECT pg_size_pretty(pg_total_relation_size('table_name'));

-- Check indexes
\di
```

---

## Additional Resources

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

For environment setup, see [SETUP_GUIDE.md](SETUP_GUIDE.md).  
For deployment, see [DEPLOYMENT.md](DEPLOYMENT.md).

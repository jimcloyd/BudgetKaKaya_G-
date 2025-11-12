# Family Budget Tracker - Deployment Guide

This comprehensive guide covers environment setup, database migrations, and deployment strategies for the Family Budget Tracker application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Setup and Migrations](#database-setup-and-migrations)
4. [Local Development](#local-development)
5. [AWS Deployment Options](#aws-deployment-options)
6. [Security and Monitoring](#security-and-monitoring)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- AWS Account (for production deployment)
- PostgreSQL 14+ database
- Python 3.9+
- Node.js 18+
- Git
- Domain name (optional but recommended for production)

## Environment Setup

### Backend Environment Setup

#### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd family-budget-tracker
```

#### 2. Set Up Python Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- Flask==3.0.0 - Web framework
- Flask-SQLAlchemy==3.1.1 - ORM for database operations
- Flask-Migrate==4.0.5 - Database migration management
- Flask-JWT-Extended==4.5.3 - JWT authentication
- Flask-CORS==4.0.0 - Cross-origin resource sharing
- psycopg2-binary==2.9.9 - PostgreSQL adapter
- python-dotenv==1.0.0 - Environment variable management
- bcrypt==4.1.1 - Password hashing
- gunicorn==21.2.0 - Production WSGI server
- python-dateutil==2.8.2 - Date utilities

#### 4. Configure Backend Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/budget_tracker

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development  # Use 'production' for production
SECRET_KEY=your-secret-key-here-change-in-production

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 hours in seconds

# CORS Configuration
CORS_ORIGINS=http://localhost:3000  # Frontend URL

# Server Configuration
PORT=5000
HOST=0.0.0.0
```

**Important Security Notes:**
- Generate strong random keys for `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Use Python to generate secure keys:
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```
- Never commit `.env` files to version control
- Use different keys for development and production

### Frontend Environment Setup

#### 1. Navigate to Frontend Directory

```bash
cd frontend
```

#### 2. Install Frontend Dependencies

```bash
npm install
```

**Key dependencies:**
- react@18.2.0 - UI library
- react-router-dom@6.20.0 - Routing
- axios@1.6.2 - HTTP client
- chart.js@4.4.0 - Data visualization
- react-chartjs-2@5.2.0 - React wrapper for Chart.js
- tailwindcss@3.3.6 - CSS framework

#### 3. Configure Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Development
VITE_API_BASE_URL=http://localhost:5000/api

# Production (update with your actual API URL)
# VITE_API_BASE_URL=https://api.yourdomain.com/api
```

**Note:** Vite requires environment variables to be prefixed with `VITE_` to be exposed to the client.

## Database Setup and Migrations

### Initial Database Setup

#### 1. Install PostgreSQL

**Windows:**
- Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- Run installer and follow setup wizard
- Remember the password you set for the `postgres` user

**Mac (using Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### 2. Create Database

**Using psql:**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE budget_tracker;

# Create user (optional, for better security)
CREATE USER budget_user WITH PASSWORD 'secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE budget_tracker TO budget_user;

# Exit psql
\q
```

**Using pgAdmin:**
1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Enter database name: `budget_tracker`
4. Click "Save"

#### 3. Update DATABASE_URL

Update your `backend/.env` file with the correct database URL:

```bash
# If using default postgres user
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/budget_tracker

# If using custom user
DATABASE_URL=postgresql://budget_user:secure_password@localhost:5432/budget_tracker
```

### Database Migration Process

The application uses Flask-Migrate (Alembic) for database schema management.

#### Initialize Migrations (First Time Only)

If the `migrations` folder doesn't exist:

```bash
cd backend
flask db init
```

This creates a `migrations` directory with the migration framework.

#### Create Initial Migration

Generate migration files from your models:

```bash
flask db migrate -m "Initial migration"
```

This command:
- Analyzes your SQLAlchemy models in `app/models.py`
- Compares them with the current database schema
- Generates migration scripts in `migrations/versions/`

#### Apply Migrations

Apply the migration to create database tables:

```bash
flask db upgrade
```

This command:
- Executes all pending migrations
- Creates all tables defined in your models
- Updates the database schema

#### Verify Database Tables

Check that tables were created:

```bash
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
- alembic_version (migration tracking)

### Common Migration Commands

```bash
# Create a new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# Show current migration version
flask db current

# Show migration history
flask db history

# Rollback to specific version
flask db downgrade <revision_id>
```

### Migration Best Practices

1. **Always review generated migrations** before applying them
   - Check `migrations/versions/` for the generated Python file
   - Verify the upgrade and downgrade functions are correct

2. **Test migrations on development first**
   - Never run untested migrations on production

3. **Backup database before migrations**
   ```bash
   pg_dump -U postgres budget_tracker > backup_$(date +%Y%m%d).sql
   ```

4. **Handle data migrations carefully**
   - For complex data transformations, write custom migration scripts
   - Test with production-like data volumes

5. **Version control migrations**
   - Commit migration files to Git
   - Never modify existing migrations that have been applied

### Seeding Default Data

After running migrations, seed default categories:

```python
# Create a seed script: backend/seed_data.py
from app import create_app, db
from app.models import Category, SharedAccount

app = create_app()

with app.app_context():
    # Create a default shared account for testing
    shared_account = SharedAccount()
    db.session.add(shared_account)
    db.session.commit()
    
    # Default categories
    default_categories = [
        'Groceries',
        'Utilities',
        'Transportation',
        'Entertainment',
        'Healthcare',
        'Miscellaneous'
    ]
    
    for cat_name in default_categories:
        category = Category(
            name=cat_name,
            shared_account_id=shared_account.id,
            is_custom=False
        )
        db.session.add(category)
    
    db.session.commit()
    print("Default data seeded successfully!")
```

Run the seed script:
```bash
python seed_data.py
```

## Local Development

### Starting the Backend Server

```bash
cd backend
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run development server
python run.py
```

The API will be available at `http://localhost:5000`

**Development features:**
- Auto-reload on code changes
- Debug mode enabled
- Detailed error messages
- CORS enabled for localhost:3000

### Starting the Frontend Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

**Development features:**
- Hot module replacement (HMR)
- Fast refresh
- API proxy to backend (configured in vite.config.ts)
- TypeScript type checking

### Development Workflow

1. **Start backend first** (port 5000)
2. **Start frontend** (port 3000)
3. **Access application** at http://localhost:3000
4. **API requests** are proxied from frontend to backend

### Testing the Setup

1. **Test backend health:**
   ```bash
   curl http://localhost:5000/api/auth/me
   # Should return 401 (unauthorized) - this is correct
   ```

2. **Test frontend:**
   - Open http://localhost:3000
   - You should see the login/register page

3. **Test registration:**
   - Register a new user
   - Check database: `psql -U postgres -d budget_tracker -c "SELECT * FROM users;"`

## Architecture Overview

The application consists of:
- **Backend**: Flask REST API (Python)
- **Frontend**: React + TypeScript + Vite
- **Database**: PostgreSQL

## AWS Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended for beginners)

#### Backend Deployment

1. **Prepare the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create Elastic Beanstalk application**
   ```bash
   eb init -p python-3.9 family-budget-tracker
   eb create production-env
   ```

3. **Set environment variables**
   ```bash
   eb setenv DATABASE_URL="postgresql://user:pass@host:5432/dbname" \
            SECRET_KEY="your-secret-key" \
            JWT_SECRET_KEY="your-jwt-secret" \
            FLASK_ENV="production" \
            CORS_ORIGINS="https://yourdomain.com"
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

#### Frontend Deployment (S3 + CloudFront)

1. **Build the frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Create S3 bucket**
   ```bash
   aws s3 mb s3://your-budget-app-frontend
   aws s3 website s3://your-budget-app-frontend --index-document index.html
   ```

3. **Upload build files**
   ```bash
   aws s3 sync dist/ s3://your-budget-app-frontend --delete
   ```

4. **Create CloudFront distribution** (for HTTPS and CDN)
   - Origin: S3 bucket
   - Enable HTTPS
   - Set custom error response: 404 -> /index.html (for React Router)

### Option 2: AWS EC2 (More control)

#### Backend on EC2

1. **Launch EC2 instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.micro (or larger based on needs)
   - Security group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **SSH into instance and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv nginx -y
   
   # Clone repository
   git clone your-repo-url
   cd family-budget-tracker/backend
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

3. **Create systemd service**
   ```bash
   sudo nano /etc/systemd/system/budget-api.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Family Budget Tracker API
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/family-budget-tracker/backend
   Environment="PATH=/home/ubuntu/family-budget-tracker/backend/venv/bin"
   EnvironmentFile=/home/ubuntu/family-budget-tracker/backend/.env
   ExecStart=/home/ubuntu/family-budget-tracker/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app

   [Install]
   WantedBy=multi-user.target
   ```

4. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/budget-api
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Enable and start services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/budget-api /etc/nginx/sites-enabled/
   sudo systemctl enable budget-api
   sudo systemctl start budget-api
   sudo systemctl restart nginx
   ```

### Option 3: AWS ECS with Fargate (Containerized)

1. **Create Dockerfile for backend**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
   ```

2. **Build and push to ECR**
   ```bash
   aws ecr create-repository --repository-name budget-tracker-api
   docker build -t budget-tracker-api .
   docker tag budget-tracker-api:latest <account-id>.dkr.ecr.<region>.amazonaws.com/budget-tracker-api:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/budget-tracker-api:latest
   ```

3. **Create ECS cluster and service** (via AWS Console or CLI)

## Database Setup (AWS RDS)

### Creating RDS PostgreSQL Instance

#### Via AWS Console

1. **Navigate to RDS Dashboard**
   - Go to AWS Console → RDS → Create database

2. **Choose Database Creation Method**
   - Select "Standard create"

3. **Engine Options**
   - Engine type: PostgreSQL
   - Version: PostgreSQL 14.x or higher
   - Templates: Free tier (for testing) or Production (for production)

4. **Settings**
   - DB instance identifier: `budget-tracker-db`
   - Master username: `budget_admin`
   - Master password: (generate strong password)
   - Confirm password

5. **Instance Configuration**
   - DB instance class: db.t3.micro (free tier) or db.t3.small (production)
   - Storage type: General Purpose SSD (gp3)
   - Allocated storage: 20 GB
   - Enable storage autoscaling (max 100 GB)

6. **Connectivity**
   - VPC: Default VPC or custom VPC
   - Public access: No (for security)
   - VPC security group: Create new or select existing
   - Availability zone: No preference

7. **Database Authentication**
   - Password authentication

8. **Additional Configuration**
   - Initial database name: `budget_tracker`
   - Enable automated backups
   - Backup retention period: 7 days
   - Enable encryption
   - Enable Enhanced Monitoring (optional)

9. **Create Database**

#### Via AWS CLI

```bash
aws rds create-db-instance \
    --db-instance-identifier budget-tracker-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 14.9 \
    --master-username budget_admin \
    --master-user-password YourStrongPassword123! \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-name budget_tracker \
    --backup-retention-period 7 \
    --no-publicly-accessible \
    --storage-encrypted
```

### Configure RDS Security Group

1. **Create or modify security group**
   ```bash
   # Get your backend security group ID
   BACKEND_SG_ID=sg-xxxxxxxxx
   
   # Get your RDS security group ID
   RDS_SG_ID=sg-yyyyyyyyy
   
   # Allow PostgreSQL access from backend
   aws ec2 authorize-security-group-ingress \
       --group-id $RDS_SG_ID \
       --protocol tcp \
       --port 5432 \
       --source-group $BACKEND_SG_ID
   ```

2. **For development/testing only** (not recommended for production):
   ```bash
   # Allow access from your IP
   aws ec2 authorize-security-group-ingress \
       --group-id $RDS_SG_ID \
       --protocol tcp \
       --port 5432 \
       --cidr YOUR_IP_ADDRESS/32
   ```

### Get RDS Connection Details

```bash
# Get RDS endpoint
aws rds describe-db-instances \
    --db-instance-identifier budget-tracker-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text
```

Example endpoint: `budget-tracker-db.xxxxxxxxx.us-east-1.rds.amazonaws.com`

### Run Migrations on RDS

#### From Local Machine (for initial setup)

1. **Update DATABASE_URL**
   ```bash
   export DATABASE_URL="postgresql://budget_admin:YourPassword@budget-tracker-db.xxxxxxxxx.us-east-1.rds.amazonaws.com:5432/budget_tracker"
   ```

2. **Test connection**
   ```bash
   psql $DATABASE_URL -c "SELECT version();"
   ```

3. **Run migrations**
   ```bash
   cd backend
   flask db upgrade
   ```

4. **Verify tables**
   ```bash
   psql $DATABASE_URL -c "\dt"
   ```

#### From EC2 Instance (recommended for production)

1. **SSH into EC2 instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

2. **Navigate to application directory**
   ```bash
   cd /home/ubuntu/family-budget-tracker/backend
   source venv/bin/activate
   ```

3. **Set DATABASE_URL**
   ```bash
   export DATABASE_URL="postgresql://budget_admin:YourPassword@rds-endpoint:5432/budget_tracker"
   ```

4. **Run migrations**
   ```bash
   flask db upgrade
   ```

#### From Elastic Beanstalk

1. **Set environment variable**
   ```bash
   eb setenv DATABASE_URL="postgresql://budget_admin:YourPassword@rds-endpoint:5432/budget_tracker"
   ```

2. **Create .ebextensions/01_flask_migrate.config**
   ```yaml
   container_commands:
     01_migrate:
       command: "source /var/app/venv/*/bin/activate && flask db upgrade"
       leader_only: true
   ```

3. **Deploy**
   ```bash
   eb deploy
   ```

### Database Backup and Restore

#### Manual Backup

```bash
# Backup from RDS
pg_dump -h budget-tracker-db.xxxxxxxxx.us-east-1.rds.amazonaws.com \
        -U budget_admin \
        -d budget_tracker \
        -F c \
        -f backup_$(date +%Y%m%d_%H%M%S).dump
```

#### Restore from Backup

```bash
# Restore to RDS
pg_restore -h budget-tracker-db.xxxxxxxxx.us-east-1.rds.amazonaws.com \
           -U budget_admin \
           -d budget_tracker \
           -c \
           backup_20241111_120000.dump
```

#### Automated Backups

RDS automated backups are enabled by default:
- Retention period: 7 days (configurable)
- Backup window: Automatic or specify preferred time
- Point-in-time recovery available

### Database Migration Strategy for Production

1. **Before deploying new code:**
   ```bash
   # Backup database
   pg_dump -h rds-endpoint -U budget_admin -d budget_tracker -F c -f pre_migration_backup.dump
   ```

2. **Test migration on staging:**
   ```bash
   # On staging environment
   flask db upgrade
   # Test application thoroughly
   ```

3. **Deploy to production:**
   ```bash
   # On production
   flask db upgrade
   # Monitor application logs
   ```

4. **Rollback if needed:**
   ```bash
   # Rollback migration
   flask db downgrade
   # Or restore from backup
   pg_restore -h rds-endpoint -U budget_admin -d budget_tracker -c pre_migration_backup.dump
   ```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-strong-random-key>
FLASK_ENV=production
CORS_ORIGINS=https://yourdomain.com
```

### Frontend (.env)
```
VITE_API_BASE_URL=https://api.yourdomain.com/api
```

## Security Checklist

- [ ] Use strong, unique SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS (use AWS Certificate Manager)
- [ ] Configure CORS properly (only allow your frontend domain)
- [ ] Use RDS with encryption at rest
- [ ] Enable RDS automated backups
- [ ] Use security groups to restrict database access
- [ ] Keep dependencies updated
- [ ] Use environment variables for sensitive data
- [ ] Enable CloudWatch logging
- [ ] Set up AWS WAF for DDoS protection (optional)

## SSL/TLS Certificate

### Using AWS Certificate Manager (ACM)

1. Request certificate for your domain
2. Validate domain ownership (DNS or email)
3. Attach certificate to:
   - CloudFront distribution (frontend)
   - Application Load Balancer (backend)

## Security and Monitoring

### Security Best Practices

#### Application Security

1. **Environment Variables**
   - Never commit `.env` files
   - Use strong, unique keys for production
   - Rotate secrets regularly
   - Use AWS Secrets Manager or Parameter Store for production secrets

2. **Database Security**
   - Use strong passwords (minimum 16 characters)
   - Enable encryption at rest
   - Enable encryption in transit (SSL/TLS)
   - Restrict network access via security groups
   - Regular security patches and updates

3. **API Security**
   - JWT tokens expire after 24 hours
   - Implement rate limiting (use Flask-Limiter)
   - Validate all input data
   - Use HTTPS only in production
   - Implement CORS properly (whitelist specific origins)

4. **Password Security**
   - Passwords hashed with bcrypt
   - Minimum 8 characters required
   - Consider adding password complexity requirements

#### AWS Security Configuration

1. **IAM Roles and Policies**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "rds:DescribeDBInstances",
           "rds:Connect"
         ],
         "Resource": "arn:aws:rds:region:account-id:db:budget-tracker-db"
       }
     ]
   }
   ```

2. **Security Groups**
   - Backend: Allow 80, 443 from internet; 5000 from ALB
   - RDS: Allow 5432 only from backend security group
   - Deny all other inbound traffic

3. **SSL/TLS Certificates**
   - Use AWS Certificate Manager (ACM)
   - Enable HTTPS on CloudFront and ALB
   - Redirect HTTP to HTTPS

### Monitoring and Logging

#### CloudWatch Setup

**1. Backend Application Logs**

For EC2:
```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

# Start agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json
```

For Elastic Beanstalk:
- Logs automatically sent to CloudWatch
- Access via EB Console → Logs → Request Logs

**2. Application Logging Configuration**

Add to `backend/app/__init__.py`:
```python
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    
    # Configure logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/budget_tracker.log',
                                          maxBytes=10240000,
                                          backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Budget Tracker startup')
    
    return app
```

**3. Frontend Logs (CloudFront)**

Enable CloudFront logging:
```bash
aws cloudfront update-distribution \
    --id DISTRIBUTION_ID \
    --logging-config \
        Enabled=true,\
        IncludeCookies=false,\
        Bucket=my-logs-bucket.s3.amazonaws.com,\
        Prefix=cloudfront-logs/
```

**4. Database Monitoring**

Enable RDS Enhanced Monitoring:
```bash
aws rds modify-db-instance \
    --db-instance-identifier budget-tracker-db \
    --monitoring-interval 60 \
    --monitoring-role-arn arn:aws:iam::account-id:role/rds-monitoring-role
```

#### CloudWatch Alarms

**1. High CPU Usage (Backend)**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name budget-tracker-high-cpu \
    --alarm-description "Alert when CPU exceeds 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --alarm-actions arn:aws:sns:region:account-id:alerts
```

**2. Database Connection Count**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name budget-tracker-db-connections \
    --alarm-description "Alert when connections exceed 80" \
    --metric-name DatabaseConnections \
    --namespace AWS/RDS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --dimensions Name=DBInstanceIdentifier,Value=budget-tracker-db
```

**3. Low Storage Space**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name budget-tracker-low-storage \
    --alarm-description "Alert when storage below 2GB" \
    --metric-name FreeStorageSpace \
    --namespace AWS/RDS \
    --statistic Average \
    --period 300 \
    --threshold 2000000000 \
    --comparison-operator LessThanThreshold \
    --evaluation-periods 1 \
    --dimensions Name=DBInstanceIdentifier,Value=budget-tracker-db
```

**4. API Error Rate**
```bash
aws cloudwatch put-metric-alarm \
    --alarm-name budget-tracker-error-rate \
    --alarm-description "Alert when 5xx errors exceed 10" \
    --metric-name 5XXError \
    --namespace AWS/ApiGateway \
    --statistic Sum \
    --period 300 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1
```

#### Performance Monitoring

**1. Application Performance Monitoring (APM)**

Consider integrating:
- **New Relic**: Full-stack monitoring
- **Datadog**: Infrastructure and application monitoring
- **Sentry**: Error tracking and performance monitoring

Example Sentry integration:
```python
# backend/requirements.txt
sentry-sdk[flask]==1.38.0

# backend/app/__init__.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    environment="production"
)
```

**2. Custom Metrics**

Log custom business metrics:
```python
# Example: Track expense creation
app.logger.info(f'Expense created: user_id={user_id}, amount={amount}, category={category}')

# Example: Track authentication
app.logger.info(f'User login: user_id={user_id}, ip={request.remote_addr}')
```

#### Log Analysis

**1. CloudWatch Insights Queries**

Query failed login attempts:
```
fields @timestamp, @message
| filter @message like /login failed/
| sort @timestamp desc
| limit 100
```

Query slow API responses:
```
fields @timestamp, @message
| filter @message like /response_time/
| parse @message /response_time: (?<duration>\d+)ms/
| filter duration > 1000
| sort duration desc
```

**2. Set Up Dashboards**

Create CloudWatch Dashboard with:
- API request count
- Error rate (4xx, 5xx)
- Response time (p50, p95, p99)
- Database connections
- CPU and memory usage
- Active users

## Backup Strategy

1. **Database backups**
   - RDS automated backups (daily)
   - Manual snapshots before major changes

2. **Application backups**
   - Store code in Git repository
   - Tag releases

## Cost Optimization

- Use t3.micro instances (free tier eligible)
- Enable RDS auto-scaling for storage
- Use S3 lifecycle policies for old logs
- Set up billing alerts
- Consider Reserved Instances for long-term use

## Estimated Monthly Costs (AWS)

- EC2 t3.micro: $8-10/month
- RDS db.t3.micro: $15-20/month
- S3 + CloudFront: $1-5/month
- **Total: ~$25-35/month**

(Free tier eligible for first 12 months)

## Troubleshooting

### Backend Issues

#### Backend Server Won't Start

**Symptoms:**
- Server crashes on startup
- Import errors
- Database connection errors

**Solutions:**

1. **Check Python version**
   ```bash
   python --version  # Should be 3.9+
   ```

2. **Verify virtual environment is activated**
   ```bash
   which python  # Should point to venv
   ```

3. **Check dependencies**
   ```bash
   pip install -r requirements.txt
   pip list  # Verify all packages installed
   ```

4. **Check environment variables**
   ```bash
   cat .env  # Verify all required variables are set
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DATABASE_URL'))"
   ```

5. **Test database connection**
   ```bash
   psql $DATABASE_URL -c "SELECT 1;"
   ```

6. **Check logs**
   ```bash
   # Local development
   python run.py  # Check console output
   
   # Production (systemd)
   sudo journalctl -u budget-api -f
   
   # Production (Elastic Beanstalk)
   eb logs
   ```

#### Database Migration Errors

**Error: "Target database is not up to date"**
```bash
# Check current version
flask db current

# Check pending migrations
flask db history

# Apply migrations
flask db upgrade
```

**Error: "Can't locate revision identified by 'xxxxx'"**
```bash
# Reset migration tracking (CAUTION: only for development)
flask db stamp head

# For production, restore from backup and reapply migrations
```

**Error: "relation already exists"**
```bash
# Check if tables exist
psql $DATABASE_URL -c "\dt"

# If tables exist but migrations not tracked
flask db stamp head

# If tables are wrong, drop and recreate (DEVELOPMENT ONLY)
psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
flask db upgrade
```

#### JWT Authentication Errors

**Error: "Token has expired"**
- Tokens expire after 24 hours
- User needs to log in again
- Consider implementing refresh tokens

**Error: "Invalid token"**
- JWT_SECRET_KEY mismatch between environments
- Token was generated with different secret
- Verify JWT_SECRET_KEY in .env

#### CORS Errors

**Error: "Access-Control-Allow-Origin"**

1. **Check CORS configuration**
   ```python
   # backend/app/__init__.py
   from flask_cors import CORS
   
   CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))
   ```

2. **Verify CORS_ORIGINS environment variable**
   ```bash
   # Development
   CORS_ORIGINS=http://localhost:3000
   
   # Production
   CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

### Frontend Issues

#### Frontend Won't Build

**Error: "Module not found"**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "TypeScript errors"**
```bash
# Check TypeScript configuration
npx tsc --noEmit

# Fix type errors or temporarily skip
npm run build -- --skipLibCheck
```

#### API Requests Failing

**Error: "Network Error" or "ERR_CONNECTION_REFUSED"**

1. **Check backend is running**
   ```bash
   curl http://localhost:5000/api/auth/me
   ```

2. **Verify API URL**
   ```bash
   # Check .env file
   cat frontend/.env
   
   # Should be:
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

3. **Check browser console**
   - Open DevTools → Network tab
   - Look for failed requests
   - Check request URL and response

**Error: "401 Unauthorized"**
- Token expired or invalid
- User needs to log in again
- Check localStorage for token

**Error: "403 Forbidden"**
- User doesn't have access to shared account
- Check user's shared_account_id in database

#### Frontend Not Loading in Production

**S3 + CloudFront Issues:**

1. **Check S3 bucket policy**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::your-bucket/*"
       }
     ]
   }
   ```

2. **Check CloudFront distribution**
   ```bash
   aws cloudfront get-distribution --id DISTRIBUTION_ID
   ```

3. **Invalidate CloudFront cache**
   ```bash
   aws cloudfront create-invalidation \
       --distribution-id DISTRIBUTION_ID \
       --paths "/*"
   ```

4. **Check error pages configuration**
   - 404 should redirect to /index.html (for React Router)
   - 403 should redirect to /index.html

### Database Issues

#### Can't Connect to Database

**Local PostgreSQL:**
```bash
# Check if PostgreSQL is running
# Windows
sc query postgresql-x64-14

# Mac
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql

# Start if not running
# Windows
sc start postgresql-x64-14

# Mac
brew services start postgresql@14

# Linux
sudo systemctl start postgresql
```

**RDS Connection:**
```bash
# Test connection
psql -h budget-tracker-db.xxxxxxxxx.us-east-1.rds.amazonaws.com \
     -U budget_admin \
     -d budget_tracker \
     -c "SELECT 1;"

# Check security group
aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx

# Verify RDS is available
aws rds describe-db-instances \
    --db-instance-identifier budget-tracker-db \
    --query 'DBInstances[0].DBInstanceStatus'
```

#### Database Performance Issues

**Slow Queries:**
```sql
-- Enable query logging (PostgreSQL)
ALTER DATABASE budget_tracker SET log_statement = 'all';
ALTER DATABASE budget_tracker SET log_duration = on;

-- Find slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

**Too Many Connections:**
```sql
-- Check current connections
SELECT count(*) FROM pg_stat_activity;

-- Kill idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND state_change < current_timestamp - INTERVAL '10 minutes';
```

**Add connection pooling:**
```python
# backend/config.py
class Config:
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
```

### Deployment Issues

#### Elastic Beanstalk Deployment Fails

```bash
# Check environment health
eb health

# View recent logs
eb logs

# SSH into instance
eb ssh

# Check application logs
sudo tail -f /var/log/eb-engine.log
sudo tail -f /var/log/web.stdout.log
```

#### EC2 Instance Issues

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Check service status
sudo systemctl status budget-api

# Check logs
sudo journalctl -u budget-api -n 100 --no-pager

# Restart service
sudo systemctl restart budget-api

# Check Nginx
sudo systemctl status nginx
sudo nginx -t  # Test configuration
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Virtual environment not activated | Activate venv: `source venv/bin/activate` |
| `psycopg2.OperationalError: could not connect` | Database not running or wrong credentials | Check DATABASE_URL and PostgreSQL status |
| `sqlalchemy.exc.ProgrammingError: relation does not exist` | Migrations not applied | Run `flask db upgrade` |
| `JWT decode error` | Wrong JWT_SECRET_KEY | Verify JWT_SECRET_KEY matches between environments |
| `CORS policy: No 'Access-Control-Allow-Origin'` | CORS not configured | Add frontend URL to CORS_ORIGINS |
| `502 Bad Gateway` | Backend not responding | Check backend service status and logs |
| `504 Gateway Timeout` | Request taking too long | Check database queries and add indexes |

### Getting Help

1. **Check application logs** first
2. **Search error messages** in documentation
3. **Review AWS CloudWatch** for infrastructure issues
4. **Check database logs** for query issues
5. **Test API endpoints** with curl or Postman
6. **Verify environment variables** are set correctly

## Maintenance

### Updating the application

1. **Backend updates**
   ```bash
   git pull
   pip install -r requirements.txt
   flask db upgrade  # if database changes
   sudo systemctl restart budget-api
   ```

2. **Frontend updates**
   ```bash
   git pull
   npm install
   npm run build
   aws s3 sync dist/ s3://your-bucket --delete
   aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
   ```

## Quick Reference

### Essential Commands

#### Local Development
```bash
# Backend
cd backend
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
python run.py

# Frontend
cd frontend
npm run dev

# Database Migrations
flask db migrate -m "Description"
flask db upgrade
flask db current
```

#### Production Deployment

**Elastic Beanstalk:**
```bash
# Deploy backend
cd backend
eb deploy

# Check status
eb health
eb logs
```

**EC2:**
```bash
# SSH and restart
ssh -i key.pem ubuntu@ec2-ip
sudo systemctl restart budget-api
sudo systemctl status budget-api
```

**Frontend (S3):**
```bash
cd frontend
npm run build
aws s3 sync dist/ s3://bucket-name --delete
aws cloudfront create-invalidation --distribution-id ID --paths "/*"
```

**Database:**
```bash
# Backup
pg_dump -h rds-endpoint -U user -d budget_tracker -F c -f backup.dump

# Restore
pg_restore -h rds-endpoint -U user -d budget_tracker -c backup.dump

# Migrations
export DATABASE_URL="postgresql://user:pass@rds-endpoint:5432/budget_tracker"
flask db upgrade
```

### Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Database backup created
- [ ] Environment variables configured
- [ ] Migrations tested on staging
- [ ] Security groups configured
- [ ] SSL certificates installed
- [ ] Monitoring and alerts set up
- [ ] Rollback plan documented

### Post-Deployment Verification

```bash
# Test API health
curl https://api.yourdomain.com/api/auth/me

# Check database connection
psql $DATABASE_URL -c "SELECT version();"

# Verify migrations
flask db current

# Check logs
eb logs  # Elastic Beanstalk
sudo journalctl -u budget-api -n 50  # EC2
```

### Emergency Rollback

**Application:**
```bash
# Elastic Beanstalk
eb deploy --version previous-version

# EC2
git checkout previous-tag
sudo systemctl restart budget-api
```

**Database:**
```bash
# Rollback migration
flask db downgrade

# Or restore from backup
pg_restore -h rds-endpoint -U user -d budget_tracker -c backup.dump
```

## Support

For issues or questions:
- Check application logs
- Review AWS CloudWatch metrics
- Consult AWS documentation
- See [Troubleshooting](#troubleshooting) section above

## Complete Deployment Workflow

### Step-by-Step Deployment Process

1. **Preparation** (See [SETUP_GUIDE.md](SETUP_GUIDE.md))
   - Set up local development environment
   - Test application locally
   - Create production environment variables

2. **Database Setup** (See [DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md))
   - Create production database (RDS)
   - Configure security groups
   - Run migrations
   - Verify tables created

3. **Backend Deployment** (Choose one option above)
   - Deploy to Elastic Beanstalk, EC2, or ECS
   - Configure environment variables
   - Set up monitoring and logging
   - Test API endpoints

4. **Frontend Deployment**
   - Build production bundle
   - Deploy to S3
   - Configure CloudFront (optional)
   - Set up custom domain (optional)

5. **Post-Deployment** (See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md))
   - Verify all features working
   - Set up monitoring and alerts
   - Configure backups
   - Document deployment

### Deployment Time Estimates

- **Elastic Beanstalk**: 30-45 minutes (recommended for beginners)
- **EC2**: 1-2 hours (more control, requires more setup)
- **ECS/Fargate**: 1-2 hours (containerized, scalable)

### Recommended Deployment Path

For first-time deployment:
1. Start with **Elastic Beanstalk** for backend (easiest)
2. Use **S3 + CloudFront** for frontend (simple and fast)
3. Use **RDS** for database (managed service)
4. Follow the **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** step by step

### Cost Considerations

**Minimal Setup** (~$25-35/month):
- EC2 t3.micro (backend)
- RDS db.t3.micro (database)
- S3 + CloudFront (frontend)

**Production Setup** (~$100-150/month):
- EC2 t3.small or larger
- RDS db.t3.small with Multi-AZ
- CloudFront with custom domain
- Enhanced monitoring and backups

**Free Tier Eligible** (First 12 months):
- EC2 t2.micro/t3.micro (750 hours/month)
- RDS db.t2.micro/db.t3.micro (750 hours/month)
- S3 (5GB storage, 20,000 GET requests)
- CloudFront (50GB data transfer)

## Related Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Local development setup
- **[DATABASE_MIGRATION_GUIDE.md](DATABASE_MIGRATION_GUIDE.md)** - Detailed migration guide
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API endpoint reference
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment checklist
- **[README.md](README.md)** - Project overview and quick start

## Summary

This deployment guide provides:
- ✅ Complete environment setup instructions
- ✅ Multiple deployment options (EB, EC2, ECS)
- ✅ Database migration procedures
- ✅ Security and monitoring setup
- ✅ Troubleshooting common issues
- ✅ Quick reference commands
- ✅ Cost estimates and optimization tips

Choose the deployment option that best fits your needs and follow the checklist to ensure a smooth deployment process.

---

**Note**: This guide provides multiple deployment options. Choose the one that best fits your technical expertise and requirements.

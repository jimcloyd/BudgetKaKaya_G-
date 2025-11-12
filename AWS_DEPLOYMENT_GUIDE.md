# AWS Deployment Guide - Family Budget Tracker

This guide walks you through deploying the Family Budget Tracker application to AWS.

## Architecture Overview

- **Backend**: AWS Elastic Beanstalk (Python 3.9)
- **Database**: AWS RDS PostgreSQL
- **Frontend**: AWS S3 + CloudFront
- **Secrets**: AWS Secrets Manager
- **Domain**: Route 53 (optional)

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. EB CLI installed (`pip install awsebcli`)
4. Node.js and npm installed
5. Python 3.9+ installed

## Step 1: Set Up AWS RDS PostgreSQL Database

### Using AWS Console:

1. Go to AWS RDS Console
2. Click "Create database"
3. Choose:
   - Engine: PostgreSQL 14+
   - Template: Free tier (for testing) or Production
   - DB instance identifier: `family-budget-db`
   - Master username: `budgetadmin`
   - Master password: (generate a strong password)
   - DB instance class: `db.t3.micro` (free tier) or larger
   - Storage: 20 GB (adjust as needed)
   - VPC: Default VPC
   - Public access: No (for production)
   - Database name: `family_budget_tracker`
4. Click "Create database"
5. Wait for the database to be available
6. Note the endpoint URL (e.g., `family-budget-db.xxxxx.us-east-1.rds.amazonaws.com`)

### Using AWS CLI:

```bash
aws rds create-db-instance \
    --db-instance-identifier family-budget-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username budgetadmin \
    --master-user-password YOUR_STRONG_PASSWORD \
    --allocated-storage 20 \
    --db-name family_budget_tracker \
    --backup-retention-period 7 \
    --no-publicly-accessible
```

## Step 2: Store Secrets in AWS Secrets Manager

```bash
# Create secret for database credentials
aws secretsmanager create-secret \
    --name family-budget-tracker/db \
    --description "Database credentials for Family Budget Tracker" \
    --secret-string '{
        "username":"budgetadmin",
        "password":"YOUR_DB_PASSWORD",
        "host":"YOUR_RDS_ENDPOINT",
        "port":"5432",
        "dbname":"family_budget_tracker"
    }'

# Create secret for JWT and Flask keys
aws secretsmanager create-secret \
    --name family-budget-tracker/app \
    --description "Application secrets for Family Budget Tracker" \
    --secret-string '{
        "jwt_secret_key":"'$(openssl rand -base64 32)'",
        "secret_key":"'$(openssl rand -base64 32)'"
    }'
```

## Step 3: Deploy Backend to Elastic Beanstalk

### 3.1 Initialize Elastic Beanstalk

```bash
cd backend

# Initialize EB application
eb init -p python-3.9 family-budget-tracker --region us-east-1

# Create environment
eb create family-budget-prod \
    --instance-type t3.small \
    --envvars \
        FLASK_ENV=production,\
        DATABASE_URL=postgresql://budgetadmin:YOUR_PASSWORD@YOUR_RDS_ENDPOINT:5432/family_budget_tracker,\
        JWT_SECRET_KEY=YOUR_JWT_SECRET,\
        SECRET_KEY=YOUR_FLASK_SECRET
```

### 3.2 Configure Security Group

After creating the environment, you need to allow the EB instances to connect to RDS:

1. Go to RDS Console → Your database → Security groups
2. Edit inbound rules
3. Add rule: PostgreSQL (5432) from the Elastic Beanstalk security group

### 3.3 Deploy Application

```bash
# Deploy the application
eb deploy

# Check status
eb status

# View logs if needed
eb logs
```

### 3.4 Run Database Migrations

```bash
# SSH into the EB instance
eb ssh

# Activate virtual environment and run migrations
source /var/app/venv/*/bin/activate
cd /var/app/current
flask db upgrade

# Exit SSH
exit
```

## Step 4: Deploy Frontend to S3 + CloudFront

### 4.1 Build Frontend

```bash
cd frontend

# Update API endpoint in your frontend code
# Create .env.production file
echo "VITE_API_URL=http://YOUR_EB_URL.elasticbeanstalk.com/api" > .env.production

# Build for production
npm run build
```

### 4.2 Create S3 Bucket

```bash
# Create bucket (use a unique name)
aws s3 mb s3://family-budget-tracker-frontend

# Enable static website hosting
aws s3 website s3://family-budget-tracker-frontend \
    --index-document index.html \
    --error-document index.html

# Upload build files
aws s3 sync dist/ s3://family-budget-tracker-frontend --delete

# Set bucket policy for public read
aws s3api put-bucket-policy \
    --bucket family-budget-tracker-frontend \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::family-budget-tracker-frontend/*"
        }]
    }'
```

### 4.3 Create CloudFront Distribution

```bash
aws cloudfront create-distribution \
    --origin-domain-name family-budget-tracker-frontend.s3.amazonaws.com \
    --default-root-object index.html
```

Or use AWS Console:
1. Go to CloudFront Console
2. Create Distribution
3. Origin domain: Your S3 bucket
4. Origin access: Public
5. Default root object: `index.html`
6. Custom error responses: 404 → /index.html (for React Router)
7. Create distribution
8. Note the CloudFront domain name

## Step 5: Configure CORS on Backend

Update your backend to allow requests from the CloudFront domain:

```python
# In backend/app/__init__.py
CORS(app, origins=[
    "http://localhost:3000",
    "https://YOUR_CLOUDFRONT_DOMAIN.cloudfront.net"
])
```

Redeploy backend:
```bash
cd backend
eb deploy
```

## Step 6: Update Frontend API URL

Update the frontend to use the production API:

```bash
cd frontend

# Update .env.production
echo "VITE_API_URL=http://YOUR_EB_URL.elasticbeanstalk.com/api" > .env.production

# Rebuild and redeploy
npm run build
aws s3 sync dist/ s3://family-budget-tracker-frontend --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
    --distribution-id YOUR_DISTRIBUTION_ID \
    --paths "/*"
```

## Step 7: (Optional) Set Up Custom Domain

### 7.1 Register Domain in Route 53

1. Go to Route 53 Console
2. Register a domain (e.g., `familybudget.com`)

### 7.2 Create SSL Certificate

```bash
# Request certificate in ACM (must be in us-east-1 for CloudFront)
aws acm request-certificate \
    --domain-name familybudget.com \
    --domain-name www.familybudget.com \
    --validation-method DNS \
    --region us-east-1
```

### 7.3 Update CloudFront with Custom Domain

1. Go to CloudFront Console
2. Edit your distribution
3. Add alternate domain names (CNAMEs)
4. Select your SSL certificate
5. Save changes

### 7.4 Create Route 53 Records

1. Go to Route 53 Console
2. Create A record (Alias) pointing to CloudFront distribution
3. Create CNAME for www subdomain

## Environment Variables Summary

### Backend (Elastic Beanstalk)

```bash
FLASK_ENV=production
DATABASE_URL=postgresql://username:password@host:5432/dbname
JWT_SECRET_KEY=your-jwt-secret
SECRET_KEY=your-flask-secret
```

### Frontend (.env.production)

```bash
VITE_API_URL=https://api.yourdomain.com/api
```

## Monitoring and Maintenance

### View Backend Logs

```bash
eb logs
```

### Monitor RDS

```bash
aws rds describe-db-instances --db-instance-identifier family-budget-db
```

### Update Backend

```bash
cd backend
# Make changes
eb deploy
```

### Update Frontend

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://family-budget-tracker-frontend --delete
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

## Cost Estimation (Monthly)

- **RDS db.t3.micro**: ~$15-20
- **Elastic Beanstalk t3.small**: ~$15-20
- **S3 Storage**: ~$1-5
- **CloudFront**: ~$1-10 (depends on traffic)
- **Route 53**: ~$0.50 per hosted zone
- **Total**: ~$35-60/month

## Security Best Practices

1. ✅ Use HTTPS for all communications
2. ✅ Store secrets in AWS Secrets Manager
3. ✅ Enable RDS encryption at rest
4. ✅ Use VPC for RDS (not publicly accessible)
5. ✅ Enable CloudFront with HTTPS only
6. ✅ Set up IAM roles with least privilege
7. ✅ Enable RDS automated backups
8. ✅ Use strong passwords
9. ✅ Enable CloudWatch monitoring
10. ✅ Set up AWS WAF for CloudFront (optional)

## Troubleshooting

### Backend won't start
- Check EB logs: `eb logs`
- Verify environment variables are set correctly
- Check RDS security group allows EB instances

### Database connection fails
- Verify RDS endpoint is correct
- Check security group rules
- Verify credentials in Secrets Manager

### Frontend can't reach API
- Check CORS configuration
- Verify API URL in frontend .env.production
- Check CloudFront cache (invalidate if needed)

### 404 errors on frontend routes
- Ensure CloudFront custom error response is set (404 → /index.html)

## Rollback

### Backend
```bash
eb deploy --version VERSION_LABEL
```

### Frontend
```bash
# Restore previous S3 version
aws s3 sync s3://family-budget-tracker-frontend-backup/ s3://family-budget-tracker-frontend/
```

## Cleanup (To Delete Everything)

```bash
# Delete EB environment
eb terminate family-budget-prod

# Delete RDS instance
aws rds delete-db-instance --db-instance-identifier family-budget-db --skip-final-snapshot

# Delete S3 bucket
aws s3 rb s3://family-budget-tracker-frontend --force

# Delete CloudFront distribution (must disable first)
aws cloudfront delete-distribution --id YOUR_DISTRIBUTION_ID

# Delete secrets
aws secretsmanager delete-secret --secret-id family-budget-tracker/db
aws secretsmanager delete-secret --secret-id family-budget-tracker/app
```

# AWS Deployment Quick Start

This is a simplified guide to get your Family Budget Tracker deployed to AWS quickly.

## Prerequisites

Install these tools:

```bash
# AWS CLI
# Download from: https://aws.amazon.com/cli/

# EB CLI
pip install awsebcli

# Configure AWS credentials
aws configure
```

## Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
# On Linux/Mac
chmod +x aws-setup.sh
./aws-setup.sh

# On Windows (PowerShell)
# Use the manual steps below
```

The script will:
1. Create RDS PostgreSQL database
2. Store secrets in AWS Secrets Manager
3. Initialize and deploy Elastic Beanstalk
4. Create S3 bucket for frontend

## Option 2: Manual Setup

### 1. Create RDS Database (5 minutes)

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
    --region us-east-1

# Wait for database to be ready (5-10 minutes)
aws rds wait db-instance-available --db-instance-identifier family-budget-db

# Get the endpoint
aws rds describe-db-instances \
    --db-instance-identifier family-budget-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text
```

### 2. Deploy Backend (10 minutes)

```bash
cd backend

# Initialize EB
eb init -p python-3.9 family-budget-tracker --region us-east-1

# Create environment with environment variables
eb create family-budget-prod \
    --instance-type t3.small \
    --envvars \
        FLASK_ENV=production,\
        DATABASE_URL=postgresql://budgetadmin:YOUR_PASSWORD@YOUR_RDS_ENDPOINT:5432/family_budget_tracker,\
        JWT_SECRET_KEY=$(openssl rand -base64 32),\
        SECRET_KEY=$(openssl rand -base64 32)

# Deploy
eb deploy
```

### 3. Configure RDS Security Group

**Important:** Allow EB to connect to RDS:

1. Go to AWS RDS Console → Your database → Security groups
2. Edit inbound rules
3. Add: PostgreSQL (5432) from Elastic Beanstalk security group

### 4. Run Database Migrations

```bash
eb ssh
source /var/app/venv/*/bin/activate
cd /var/app/current
flask db upgrade
exit
```

### 5. Deploy Frontend (5 minutes)

```bash
cd frontend

# Create production config
echo "VITE_API_URL=http://YOUR_EB_URL.elasticbeanstalk.com/api" > .env.production

# Build
npm run build

# Create S3 bucket (use a unique name)
aws s3 mb s3://your-unique-bucket-name

# Enable website hosting
aws s3 website s3://your-unique-bucket-name \
    --index-document index.html \
    --error-document index.html

# Upload files
aws s3 sync dist/ s3://your-unique-bucket-name --delete

# Make public
aws s3api put-bucket-policy \
    --bucket your-unique-bucket-name \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-unique-bucket-name/*"
        }]
    }'
```

### 6. Access Your Application

Your app is now live at:
- Frontend: `http://your-unique-bucket-name.s3-website-us-east-1.amazonaws.com`
- Backend: `http://YOUR_EB_URL.elasticbeanstalk.com`

## Quick Deploy Commands

After initial setup, use these to deploy updates:

```bash
# Deploy backend
cd backend
eb deploy

# Deploy frontend
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket-name --delete
```

Or use the provided scripts:

```bash
# Linux/Mac
./deploy-backend.sh
./deploy-frontend.sh your-bucket-name

# Windows
.\deploy-backend.ps1
.\deploy-frontend.ps1 your-bucket-name
```

## Cost Estimate

- RDS db.t3.micro: ~$15/month
- EB t3.small: ~$15/month
- S3 + Data Transfer: ~$2/month
- **Total: ~$32/month**

## Add HTTPS (Optional but Recommended)

### Create CloudFront Distribution

1. Go to CloudFront Console
2. Create distribution
3. Origin: Your S3 bucket
4. Default root object: `index.html`
5. Custom error response: 404 → /index.html (200)
6. Wait for deployment (~15 minutes)

### Request SSL Certificate

```bash
aws acm request-certificate \
    --domain-name yourdomain.com \
    --validation-method DNS \
    --region us-east-1
```

### Update Backend CORS

Add CloudFront domain to allowed origins in `backend/app/__init__.py`:

```python
CORS(app, origins=[
    "http://localhost:3000",
    "https://YOUR_CLOUDFRONT_DOMAIN.cloudfront.net"
])
```

## Troubleshooting

### Backend won't start
```bash
eb logs
```

### Can't connect to database
- Check RDS security group allows EB instances
- Verify DATABASE_URL is correct

### Frontend shows API errors
- Check CORS configuration
- Verify API URL in .env.production
- Check EB environment is running: `eb status`

## Cleanup (Delete Everything)

```bash
# Delete EB environment
cd backend
eb terminate family-budget-prod

# Delete RDS
aws rds delete-db-instance \
    --db-instance-identifier family-budget-db \
    --skip-final-snapshot

# Delete S3 bucket
aws s3 rb s3://your-bucket-name --force
```

## Need Help?

- AWS Documentation: https://docs.aws.amazon.com/
- EB CLI Docs: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
- Check `AWS_DEPLOYMENT_GUIDE.md` for detailed instructions

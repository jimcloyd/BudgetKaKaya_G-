#!/bin/bash

# AWS Initial Setup Script
# This script helps you set up the AWS infrastructure

set -e

echo "=========================================="
echo "AWS Family Budget Tracker Setup"
echo "=========================================="
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed"
    echo "Please install it from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "Error: EB CLI is not installed"
    echo "Please install it with: pip install awsebcli"
    exit 1
fi

echo "AWS CLI and EB CLI are installed ✓"
echo ""

# Get AWS region
read -p "Enter AWS region (default: us-east-1): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

echo ""
echo "=========================================="
echo "Step 1: Create RDS PostgreSQL Database"
echo "=========================================="
echo ""

read -p "Enter DB instance identifier (default: family-budget-db): " DB_IDENTIFIER
DB_IDENTIFIER=${DB_IDENTIFIER:-family-budget-db}

read -p "Enter DB master username (default: budgetadmin): " DB_USERNAME
DB_USERNAME=${DB_USERNAME:-budgetadmin}

read -sp "Enter DB master password: " DB_PASSWORD
echo ""

read -p "Enter DB name (default: family_budget_tracker): " DB_NAME
DB_NAME=${DB_NAME:-family_budget_tracker}

echo ""
echo "Creating RDS database..."

aws rds create-db-instance \
    --db-instance-identifier $DB_IDENTIFIER \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username $DB_USERNAME \
    --master-user-password $DB_PASSWORD \
    --allocated-storage 20 \
    --db-name $DB_NAME \
    --backup-retention-period 7 \
    --no-publicly-accessible \
    --region $AWS_REGION

echo "RDS database creation initiated. This may take 5-10 minutes..."
echo "Waiting for database to be available..."

aws rds wait db-instance-available \
    --db-instance-identifier $DB_IDENTIFIER \
    --region $AWS_REGION

# Get RDS endpoint
DB_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier $DB_IDENTIFIER \
    --region $AWS_REGION \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text)

echo "Database is ready!"
echo "Endpoint: $DB_ENDPOINT"

echo ""
echo "=========================================="
echo "Step 2: Create Secrets in AWS Secrets Manager"
echo "=========================================="
echo ""

# Generate random secrets
JWT_SECRET=$(openssl rand -base64 32)
FLASK_SECRET=$(openssl rand -base64 32)

echo "Creating database secret..."
aws secretsmanager create-secret \
    --name family-budget-tracker/db \
    --description "Database credentials for Family Budget Tracker" \
    --secret-string "{\"username\":\"$DB_USERNAME\",\"password\":\"$DB_PASSWORD\",\"host\":\"$DB_ENDPOINT\",\"port\":\"5432\",\"dbname\":\"$DB_NAME\"}" \
    --region $AWS_REGION

echo "Creating application secrets..."
aws secretsmanager create-secret \
    --name family-budget-tracker/app \
    --description "Application secrets for Family Budget Tracker" \
    --secret-string "{\"jwt_secret_key\":\"$JWT_SECRET\",\"secret_key\":\"$FLASK_SECRET\"}" \
    --region $AWS_REGION

echo "Secrets created successfully!"

echo ""
echo "=========================================="
echo "Step 3: Initialize Elastic Beanstalk"
echo "=========================================="
echo ""

cd backend

echo "Initializing Elastic Beanstalk..."
eb init -p python-3.9 family-budget-tracker --region $AWS_REGION

echo ""
read -p "Enter environment name (default: family-budget-prod): " EB_ENV
EB_ENV=${EB_ENV:-family-budget-prod}

DATABASE_URL="postgresql://$DB_USERNAME:$DB_PASSWORD@$DB_ENDPOINT:5432/$DB_NAME"

echo "Creating Elastic Beanstalk environment..."
eb create $EB_ENV \
    --instance-type t3.small \
    --envvars \
        FLASK_ENV=production,\
        DATABASE_URL=$DATABASE_URL,\
        JWT_SECRET_KEY=$JWT_SECRET,\
        SECRET_KEY=$FLASK_SECRET

echo ""
echo "Getting EB environment URL..."
EB_URL=$(eb status | grep "CNAME" | awk '{print $2}')

echo ""
echo "=========================================="
echo "Step 4: Configure RDS Security Group"
echo "=========================================="
echo ""

echo "You need to manually configure the RDS security group to allow connections from EB:"
echo "1. Go to AWS RDS Console"
echo "2. Select your database: $DB_IDENTIFIER"
echo "3. Click on the VPC security group"
echo "4. Edit inbound rules"
echo "5. Add PostgreSQL (5432) from the Elastic Beanstalk security group"

read -p "Press Enter after configuring the security group..."

echo ""
echo "=========================================="
echo "Step 5: Create S3 Bucket for Frontend"
echo "=========================================="
echo ""

read -p "Enter S3 bucket name (must be globally unique): " S3_BUCKET

echo "Creating S3 bucket..."
aws s3 mb s3://$S3_BUCKET --region $AWS_REGION

echo "Enabling static website hosting..."
aws s3 website s3://$S3_BUCKET \
    --index-document index.html \
    --error-document index.html

echo "Setting bucket policy..."
aws s3api put-bucket-policy \
    --bucket $S3_BUCKET \
    --policy "{
        \"Version\": \"2012-10-17\",
        \"Statement\": [{
            \"Sid\": \"PublicReadGetObject\",
            \"Effect\": \"Allow\",
            \"Principal\": \"*\",
            \"Action\": \"s3:GetObject\",
            \"Resource\": \"arn:aws:s3:::$S3_BUCKET/*\"
        }]
    }"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Configuration Summary:"
echo "----------------------"
echo "AWS Region: $AWS_REGION"
echo "RDS Endpoint: $DB_ENDPOINT"
echo "RDS Database: $DB_NAME"
echo "EB Environment: $EB_ENV"
echo "EB URL: http://$EB_URL"
echo "S3 Bucket: $S3_BUCKET"
echo ""
echo "Next Steps:"
echo "1. Update frontend/.env.production with API URL: http://$EB_URL/api"
echo "2. Deploy frontend: ./deploy-frontend.sh $S3_BUCKET"
echo "3. (Optional) Set up CloudFront distribution for HTTPS"
echo "4. (Optional) Configure custom domain with Route 53"
echo ""
echo "Deployment Commands:"
echo "  Backend:  ./deploy-backend.sh"
echo "  Frontend: ./deploy-frontend.sh $S3_BUCKET"
echo ""

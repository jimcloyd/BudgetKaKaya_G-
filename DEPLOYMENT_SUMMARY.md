# AWS Deployment Summary

## ✅ Completed Steps

### 1. Database (RDS PostgreSQL)
- **Status**: ✅ Created and Available
- **Endpoint**: `budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com`
- **Database Name**: `budget_tracker`
- **Username**: `budget_admin`
- **Password**: [Your chosen password]
- **Version**: PostgreSQL 14.19

### 2. Backend (Elastic Beanstalk)
- **Status**: 🔄 Deploying (fixing package issue)
- **Environment**: `production-env`
- **URL**: `production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com`
- **API URL**: `http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api`
- **Platform**: Python 3.9 on Amazon Linux 2023

### 3. Issue Fixed
- **Problem**: Missing `postgresql-devel` package
- **Solution**: Added `.ebextensions/01_packages.config` to install `postgresql15-devel`
- **Status**: Redeploying now

---

## 🔄 Next Steps (After Deployment Completes)

### Step 1: Configure Environment Variables

```powershell
cd backend
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

# Replace YOUR_DB_PASSWORD with your actual password
eb setenv `
    FLASK_ENV=production `
    DATABASE_URL="postgresql://budget_admin:YOUR_DB_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker" `
    SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    CORS_ORIGINS="http://localhost:3000"
```

### Step 2: Configure Security Groups

Allow Elastic Beanstalk to connect to RDS:

```powershell
# Get EB instance ID
$ebInstanceId = aws elasticbeanstalk describe-environment-resources --environment-name production-env --query 'EnvironmentResources.Instances[0].Id' --output text

# Get EB security group
$ebSg = aws ec2 describe-instances --instance-ids $ebInstanceId --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' --output text

# Get RDS security group
$rdsSg = aws rds describe-db-instances --db-instance-identifier budget-tracker-db --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' --output text

# Allow connection
aws ec2 authorize-security-group-ingress `
    --group-id $rdsSg `
    --protocol tcp `
    --port 5432 `
    --source-group $ebSg
```

### Step 3: Run Database Migrations

```powershell
# SSH into EB instance
eb ssh production-env

# Once inside, run:
cd /var/app/current
source /var/app/venv/*/bin/activate
export DATABASE_URL="postgresql://budget_admin:YOUR_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
flask db upgrade
exit
```

### Step 4: Test Backend

```powershell
# Test API
curl http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api/auth/me
```

You should get a 401 error (this is correct - it means the API is working!)

### Step 5: Deploy Frontend to S3

```powershell
cd ../frontend

# Create unique bucket name
$BUCKET = "budget-tracker-$(Get-Random)"

# Create bucket
aws s3 mb s3://$BUCKET

# Configure for static website
aws s3 website s3://$BUCKET --index-document index.html --error-document index.html

# Update .env with backend URL
"VITE_API_BASE_URL=http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api" | Out-File .env.production

# Build frontend
npm run build

# Upload to S3
aws s3 sync dist/ s3://$BUCKET --delete

# Make bucket public
$POLICY = @"
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::$BUCKET/*"
  }]
}
"@
$POLICY | Out-File policy.json
aws s3api put-bucket-policy --bucket $BUCKET --policy file://policy.json

Write-Host "Frontend URL: http://$BUCKET.s3-website-us-east-1.amazonaws.com"
```

### Step 6: Update CORS

```powershell
cd ../backend
eb setenv CORS_ORIGINS="http://$BUCKET.s3-website-us-east-1.amazonaws.com"
```

---

## 📋 Your URLs

- **Backend API**: `http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api`
- **Frontend**: Will be `http://your-bucket.s3-website-us-east-1.amazonaws.com`
- **Database**: `budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432`

---

## 🔧 Useful Commands

### Backend Management
```powershell
# View logs
eb logs

# Check health
eb health

# Deploy updates
eb deploy

# SSH into instance
eb ssh

# Check environment status
eb status
```

### Database Management
```powershell
# Check database status
aws rds describe-db-instances --db-instance-identifier budget-tracker-db --query 'DBInstances[0].DBInstanceStatus'

# Connect to database
psql -h budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com -U budget_admin -d budget_tracker
```

---

## 💰 Cost Estimate

With AWS Free Tier (first 12 months):
- **EC2 t3.micro**: FREE (750 hours/month)
- **RDS db.t3.micro**: FREE (750 hours/month)
- **S3**: FREE (5GB storage)
- **Total**: $0-5/month

After free tier:
- **EC2 t3.micro**: ~$8-10/month
- **RDS db.t3.micro**: ~$15-20/month
- **S3 + data transfer**: ~$1-5/month
- **Total**: ~$25-35/month

---

## 🆘 Troubleshooting

### Backend not working
```powershell
eb logs
eb health
```

### Database connection error
- Check security groups are configured
- Verify DATABASE_URL is correct
- Check RDS is in "available" state

### Frontend not loading
```powershell
aws s3 ls s3://your-bucket
```

---

## 🗑️ Clean Up (Delete Everything)

If you want to delete everything:

```powershell
# Delete EB environment
eb terminate production-env

# Delete RDS
aws rds delete-db-instance `
    --db-instance-identifier budget-tracker-db `
    --skip-final-snapshot

# Delete S3 bucket
aws s3 rb s3://your-bucket --force
```

---

**Last Updated**: November 11, 2025
**Account ID**: 566024249772
**Region**: us-east-1

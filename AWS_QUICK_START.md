# AWS Quick Start - Family Budget Tracker

## 🚀 Fast Track Deployment (30 minutes)

### Prerequisites
```powershell
# Install AWS CLI
# Download: https://awscli.amazonaws.com/AWSCLIV2.msi

# Configure AWS
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1), Format (json)

# Install EB CLI
pip install awsebcli

# Verify
aws --version
eb --version
```

### 1. Create Database (5 min)
```powershell
aws rds create-db-instance `
    --db-instance-identifier budget-tracker-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --master-username budget_admin `
    --master-user-password "ChangeMe123!" `
    --allocated-storage 20 `
    --db-name budget_tracker `
    --no-publicly-accessible

# Wait for "available" status (5-10 min)
aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].DBInstanceStatus'

# Get endpoint
aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text
```

### 2. Deploy Backend (10 min)
```powershell
cd backend

# Initialize
eb init -p python-3.9 family-budget-tracker --region us-east-1

# Create environment
eb create production-env

# Set environment variables (replace with your values)
eb setenv `
    FLASK_ENV=production `
    DATABASE_URL="postgresql://budget_admin:ChangeMe123!@YOUR-DB-ENDPOINT:5432/budget_tracker" `
    SECRET_KEY="your-secret-key-here" `
    JWT_SECRET_KEY="your-jwt-secret-here" `
    CORS_ORIGINS="http://localhost:3000"
```

### 3. Configure Security (2 min)
```powershell
# Allow EB to access RDS
# Get security group IDs
$EB_SG = aws elasticbeanstalk describe-environment-resources `
    --environment-name production-env `
    --query 'EnvironmentResources.Instances[0].Id' `
    --output text

$RDS_SG = aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' `
    --output text

# Open port 5432
aws ec2 authorize-security-group-ingress `
    --group-id $RDS_SG `
    --protocol tcp `
    --port 5432 `
    --source-group $EB_SG
```

### 4. Run Migrations (3 min)
```powershell
# SSH into EB
eb ssh

# Run migrations
cd /var/app/current
source /var/app/venv/*/bin/activate
export DATABASE_URL="postgresql://budget_admin:ChangeMe123!@YOUR-ENDPOINT:5432/budget_tracker"
flask db upgrade
exit
```

### 5. Deploy Frontend (5 min)
```powershell
cd ../frontend

# Get backend URL
$BACKEND_URL = eb status | Select-String "CNAME" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }

# Create production env file
echo "VITE_API_BASE_URL=http://$BACKEND_URL/api" > .env.production

# Build
npm run build

# Create S3 bucket
$BUCKET = "budget-tracker-$(Get-Random)"
aws s3 mb s3://$BUCKET
aws s3 website s3://$BUCKET --index-document index.html

# Upload
aws s3 sync dist/ s3://$BUCKET --delete

# Make public
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
$POLICY | Out-File -FilePath policy.json
aws s3api put-bucket-policy --bucket $BUCKET --policy file://policy.json
```

### 6. Update CORS (1 min)
```powershell
cd ../backend
$FRONTEND_URL = "http://$BUCKET.s3-website-us-east-1.amazonaws.com"
eb setenv CORS_ORIGINS=$FRONTEND_URL
```

### 7. Test! 🎉
```powershell
# Open frontend
Start-Process $FRONTEND_URL
```

## 📋 Checklist

- [ ] AWS account created
- [ ] AWS CLI installed and configured
- [ ] EB CLI installed
- [ ] RDS database created
- [ ] Backend deployed to EB
- [ ] Security groups configured
- [ ] Database migrations run
- [ ] Frontend deployed to S3
- [ ] CORS updated
- [ ] Application tested

## 🔗 Your URLs

After deployment, save these:

- **Frontend**: `http://your-bucket.s3-website-us-east-1.amazonaws.com`
- **Backend**: `http://your-env.elasticbeanstalk.com/api`
- **Database**: `your-db.rds.amazonaws.com:5432`

## 💰 Cost

**Free Tier (12 months)**: $0-5/month
**After Free Tier**: $25-35/month

## 🆘 Quick Fixes

**Backend not working?**
```powershell
eb logs
eb health
```

**Frontend not loading?**
```powershell
aws s3 ls s3://your-bucket
```

**Database connection error?**
```powershell
# Check RDS status
aws rds describe-db-instances --db-instance-identifier budget-tracker-db

# Check security groups
aws ec2 describe-security-groups --group-ids $RDS_SG
```

## 📚 Full Documentation

- [AWS_GETTING_STARTED.md](AWS_GETTING_STARTED.md) - Detailed guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment options
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist

## 🔄 Update Application

**Backend:**
```powershell
cd backend
eb deploy
```

**Frontend:**
```powershell
cd frontend
npm run build
aws s3 sync dist/ s3://your-bucket --delete
```

## 🗑️ Clean Up (Delete Everything)

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

**Need help?** Check [AWS_GETTING_STARTED.md](AWS_GETTING_STARTED.md) for detailed instructions!

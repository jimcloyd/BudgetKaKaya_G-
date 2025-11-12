# AWS Deployment - Step by Step Guide

Follow these steps to deploy your Family Budget Tracker to AWS.

## Prerequisites ✅
- [x] AWS Account created (566024249772)
- [x] AWS CLI installed and configured
- [ ] Database password chosen (you'll need this)

---

## Step 1: Create RDS Database (5-10 minutes)

Choose a strong database password (min 8 characters, include letters and numbers).

Run this command (replace `YOUR_PASSWORD` with your chosen password):

```powershell
aws rds create-db-instance `
    --db-instance-identifier budget-tracker-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 14.9 `
    --master-username budget_admin `
    --master-user-password "YOUR_PASSWORD" `
    --allocated-storage 20 `
    --storage-type gp3 `
    --db-name budget_tracker `
    --backup-retention-period 7 `
    --no-publicly-accessible `
    --storage-encrypted
```

**Wait for database to be ready:**
```powershell
# Check status (repeat until you see "available")
aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].DBInstanceStatus' `
    --output text
```

**Get database endpoint:**
```powershell
aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text
```

**Save this endpoint!** You'll need it later.

---

## Step 2: Install Elastic Beanstalk CLI

```powershell
pip install awsebcli
```

Verify installation:
```powershell
eb --version
```

---

## Step 3: Initialize Elastic Beanstalk

```powershell
cd backend
eb init -p python-3.9 family-budget-tracker --region us-east-1
```

When prompted:
- Application name: Press Enter (use default)
- Set up SSH: Type `y` and press Enter
- Select or create keypair: Choose option or create new

---

## Step 4: Create EB Environment (5-10 minutes)

```powershell
eb create production-env
```

This will take 5-10 minutes. Wait for it to complete.

**Get your backend URL:**
```powershell
eb status
```

Look for the **CNAME** line - this is your backend URL.

---

## Step 5: Configure Environment Variables

Replace the placeholders with your actual values:
- `YOUR_DB_ENDPOINT` - from Step 1
- `YOUR_DB_PASSWORD` - your chosen password

```powershell
eb setenv `
    FLASK_ENV=production `
    DATABASE_URL="postgresql://budget_admin:YOUR_DB_PASSWORD@YOUR_DB_ENDPOINT:5432/budget_tracker" `
    SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    CORS_ORIGINS="http://localhost:3000"
```

---

## Step 6: Configure Security Groups

Allow Elastic Beanstalk to connect to RDS:

```powershell
# Get EB security group
$EB_SG = aws elasticbeanstalk describe-environment-resources `
    --environment-name production-env `
    --query 'EnvironmentResources.Instances[0].Id' `
    --output text

# Get RDS security group
$RDS_SG = aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' `
    --output text

# Allow connection
aws ec2 authorize-security-group-ingress `
    --group-id $RDS_SG `
    --protocol tcp `
    --port 5432 `
    --source-group $EB_SG
```

---

## Step 7: Run Database Migrations

SSH into your EB instance:

```powershell
eb ssh
```

Once inside, run these commands:

```bash
cd /var/app/current
source /var/app/venv/*/bin/activate
export DATABASE_URL="postgresql://budget_admin:YOUR_PASSWORD@YOUR_ENDPOINT:5432/budget_tracker"
flask db upgrade
exit
```

---

## Step 8: Test Backend

Get your backend URL:
```powershell
eb status
```

Test the API:
```powershell
curl http://YOUR_EB_URL/api/auth/me
```

You should get a 401 error (this is correct - it means the API is working!)

---

## Step 9: Deploy Frontend to S3

```powershell
cd ../frontend

# Create unique bucket name
$BUCKET = "budget-tracker-$(Get-Random)"

# Create bucket
aws s3 mb s3://$BUCKET

# Configure for static website
aws s3 website s3://$BUCKET --index-document index.html --error-document index.html

# Update .env with backend URL
"VITE_API_BASE_URL=http://YOUR_EB_URL/api" | Out-File .env.production

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
```

Your frontend URL will be:
```
http://$BUCKET.s3-website-us-east-1.amazonaws.com
```

---

## Step 10: Update CORS

Update backend to allow frontend domain:

```powershell
cd ../backend
eb setenv CORS_ORIGINS="http://YOUR_BUCKET.s3-website-us-east-1.amazonaws.com"
```

---

## 🎉 Deployment Complete!

Your application is now live on AWS!

### Your URLs:
- **Frontend**: `http://your-bucket.s3-website-us-east-1.amazonaws.com`
- **Backend API**: `http://your-eb-url.elasticbeanstalk.com/api`

### Test Your Application:
1. Open the frontend URL in your browser
2. Register a new user
3. Test creating expenses, budgets, etc.

---

## Troubleshooting

### Database not connecting
- Check security groups are configured correctly
- Verify DATABASE_URL is correct
- Check RDS is in "available" state

### Backend not working
```powershell
eb logs
eb health
```

### Frontend not loading
```powershell
aws s3 ls s3://your-bucket
```

---

## Cost Estimate

With AWS Free Tier (first 12 months):
- EC2 t3.micro: **FREE**
- RDS db.t3.micro: **FREE**
- S3: **FREE**
- **Total: $0-5/month**

After free tier: **$25-35/month**

---

## Clean Up (Delete Everything)

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

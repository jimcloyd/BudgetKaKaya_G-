# Getting Started with AWS Deployment

Congratulations on creating your AWS account! This guide will walk you through deploying the Family Budget Tracker to AWS.

## Prerequisites Checklist

Before we begin, make sure you have:
- ✅ AWS Account created
- ⬜ AWS CLI installed on your computer
- ⬜ AWS credentials configured
- ⬜ Application tested locally (optional but recommended)

## Step 1: Install AWS CLI

### Windows

Download and install from: https://awscli.amazonaws.com/AWSCLIV2.msi

Or using PowerShell:
```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

Verify installation:
```powershell
aws --version
```

You should see something like: `aws-cli/2.x.x Python/3.x.x Windows/10`

## Step 2: Configure AWS Credentials

### Get Your AWS Access Keys

1. Log in to AWS Console: https://console.aws.amazon.com
2. Click your username (top right) → **Security credentials**
3. Scroll to **Access keys** section
4. Click **Create access key**
5. Choose **Command Line Interface (CLI)**
6. Check the confirmation box
7. Click **Create access key**
8. **IMPORTANT**: Download the CSV file or copy both:
   - Access key ID
   - Secret access key
   
   ⚠️ You won't be able to see the secret key again!

### Configure AWS CLI

Run this command and enter your credentials:
```powershell
aws configure
```

You'll be prompted for:
```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

**Recommended region**: `us-east-1` (US East - N. Virginia)

Verify configuration:
```powershell
aws sts get-caller-identity
```

You should see your account information.

## Step 3: Choose Your Deployment Strategy

You have three options:

### Option A: Elastic Beanstalk (Recommended for Beginners) ⭐

**Pros:**
- Easiest to set up
- Automatic scaling
- Managed platform updates
- Built-in monitoring

**Cons:**
- Less control over infrastructure
- Slightly higher cost

**Time to deploy**: ~30-45 minutes

**Cost**: ~$25-35/month (Free tier eligible for 12 months)

**Next steps**: See [Option A Instructions](#option-a-elastic-beanstalk-deployment) below

### Option B: EC2 (More Control)

**Pros:**
- Full control over server
- More customization options
- Can optimize costs

**Cons:**
- More setup required
- Manual scaling
- You manage updates

**Time to deploy**: ~1-2 hours

**Cost**: ~$25-35/month (Free tier eligible for 12 months)

**Next steps**: See [DEPLOYMENT.md](DEPLOYMENT.md#option-2-aws-ec2-more-control)

### Option C: ECS with Fargate (Containerized)

**Pros:**
- Containerized (Docker)
- Serverless compute
- Easy scaling

**Cons:**
- Requires Docker knowledge
- More complex setup

**Time to deploy**: ~1-2 hours

**Cost**: ~$30-40/month

**Next steps**: See [DEPLOYMENT.md](DEPLOYMENT.md#option-3-aws-ecs-with-fargate-containerized)

---

## Option A: Elastic Beanstalk Deployment

This is the recommended approach for first-time AWS deployment.

### Step 1: Install Elastic Beanstalk CLI

```powershell
pip install awsebcli
```

Verify installation:
```powershell
eb --version
```

### Step 2: Create RDS Database

We'll create the database first so the backend can connect to it.

```powershell
# Create RDS PostgreSQL instance
aws rds create-db-instance `
    --db-instance-identifier budget-tracker-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 14.9 `
    --master-username budget_admin `
    --master-user-password "YourStrongPassword123!" `
    --allocated-storage 20 `
    --storage-type gp3 `
    --db-name budget_tracker `
    --backup-retention-period 7 `
    --no-publicly-accessible `
    --storage-encrypted
```

**⚠️ Important**: Replace `YourStrongPassword123!` with a strong password and save it securely!

This will take 5-10 minutes to create. Check status:
```powershell
aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].DBInstanceStatus'
```

Wait until status is `"available"`.

Get the database endpoint:
```powershell
aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text
```

Save this endpoint - you'll need it later!

### Step 3: Initialize Elastic Beanstalk Application

```powershell
cd backend

# Initialize EB application
eb init -p python-3.9 family-budget-tracker --region us-east-1
```

When prompted:
- Application name: `family-budget-tracker` (or press Enter)
- Do you want to set up SSH: `Y` (yes)
- Select a keypair or create new one

### Step 4: Create Elastic Beanstalk Environment

```powershell
# Create environment
eb create production-env
```

This will take 5-10 minutes. EB will:
- Create EC2 instance
- Set up load balancer
- Configure security groups
- Deploy your application

### Step 5: Configure Environment Variables

Replace the values with your actual database endpoint and password:

```powershell
eb setenv `
    FLASK_ENV=production `
    DATABASE_URL="postgresql://budget_admin:YourStrongPassword123!@your-db-endpoint:5432/budget_tracker" `
    SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    CORS_ORIGINS="http://your-frontend-url.s3-website-us-east-1.amazonaws.com"
```

**Note**: We'll update CORS_ORIGINS after deploying the frontend.

### Step 6: Configure Database Security Group

Allow EB to connect to RDS:

```powershell
# Get EB security group ID
$EB_SG = aws elasticbeanstalk describe-environment-resources `
    --environment-name production-env `
    --query 'EnvironmentResources.Instances[0].Id' `
    --output text

# Get RDS security group ID
$RDS_SG = aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' `
    --output text

# Allow EB to connect to RDS
aws ec2 authorize-security-group-ingress `
    --group-id $RDS_SG `
    --protocol tcp `
    --port 5432 `
    --source-group $EB_SG
```

### Step 7: Run Database Migrations

```powershell
# SSH into EB instance
eb ssh

# Once inside the instance:
cd /var/app/current
source /var/app/venv/*/bin/activate
export DATABASE_URL="postgresql://budget_admin:YourPassword@your-endpoint:5432/budget_tracker"
flask db upgrade

# Exit SSH
exit
```

### Step 8: Get Backend URL

```powershell
eb status
```

Look for the **CNAME** - this is your backend API URL.
Example: `production-env.us-east-1.elasticbeanstalk.com`

Your API will be at: `http://production-env.us-east-1.elasticbeanstalk.com/api`

### Step 9: Deploy Frontend to S3

```powershell
cd ../frontend

# Update .env with backend URL
# Edit frontend/.env.production and add:
# VITE_API_BASE_URL=http://your-eb-url.elasticbeanstalk.com/api

# Build frontend
npm run build

# Create S3 bucket (replace with unique name)
$BUCKET_NAME = "budget-tracker-frontend-$(Get-Random)"
aws s3 mb s3://$BUCKET_NAME

# Configure for static website hosting
aws s3 website s3://$BUCKET_NAME `
    --index-document index.html `
    --error-document index.html

# Upload files
aws s3 sync dist/ s3://$BUCKET_NAME --delete

# Make bucket public
aws s3api put-bucket-policy `
    --bucket $BUCKET_NAME `
    --policy "{
        \"Version\": \"2012-10-17\",
        \"Statement\": [{
            \"Sid\": \"PublicReadGetObject\",
            \"Effect\": \"Allow\",
            \"Principal\": \"*\",
            \"Action\": \"s3:GetObject\",
            \"Resource\": \"arn:aws:s3:::$BUCKET_NAME/*\"
        }]
    }"
```

Your frontend URL will be:
`http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com`

### Step 10: Update CORS Settings

Update backend CORS to allow frontend domain:

```powershell
cd ../backend
eb setenv CORS_ORIGINS="http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com"
```

### Step 11: Test Your Application! 🎉

1. Open your frontend URL in a browser
2. Register a new user
3. Test creating expenses, budgets, etc.

## Deployment Complete! ✅

Your application is now live on AWS!

### Your URLs:
- **Frontend**: `http://your-bucket.s3-website-us-east-1.amazonaws.com`
- **Backend API**: `http://your-eb-env.elasticbeanstalk.com/api`
- **Database**: RDS PostgreSQL (private)

### Next Steps:

1. **Add HTTPS** (Recommended)
   - Set up CloudFront for frontend
   - Request SSL certificate in AWS Certificate Manager
   - See [DEPLOYMENT.md](DEPLOYMENT.md#ssltls-certificate)

2. **Set up monitoring**
   - CloudWatch alarms
   - See [DEPLOYMENT.md](DEPLOYMENT.md#monitoring-and-logging)

3. **Configure backups**
   - RDS automated backups (already enabled)
   - See [DEPLOYMENT.md](DEPLOYMENT.md#backup-strategy)

4. **Custom domain** (Optional)
   - Register domain in Route 53
   - See [DEPLOYMENT.md](DEPLOYMENT.md#custom-domain)

## Cost Breakdown

With AWS Free Tier (first 12 months):
- EC2 t2.micro/t3.micro: **FREE** (750 hours/month)
- RDS db.t3.micro: **FREE** (750 hours/month)
- S3: **FREE** (5GB storage)
- Data transfer: **FREE** (15GB/month)

After free tier or if you exceed limits:
- EC2 t3.micro: ~$8-10/month
- RDS db.t3.micro: ~$15-20/month
- S3 + data transfer: ~$1-5/month
- **Total**: ~$25-35/month

## Troubleshooting

### EB deployment fails
```powershell
eb logs
```

### Can't connect to database
- Check security group allows EB → RDS connection
- Verify DATABASE_URL is correct
- Check RDS is in "available" state

### Frontend can't reach backend
- Check CORS_ORIGINS includes frontend URL
- Verify backend is running: `eb health`
- Check backend URL is correct in frontend .env

### Need to rollback
```powershell
eb deploy --version previous-version
```

## Getting Help

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides
- Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for step-by-step checklist
- Review AWS CloudWatch logs for errors
- Check [Troubleshooting section](DEPLOYMENT.md#troubleshooting)

## Useful Commands

```powershell
# Check EB status
eb status

# View logs
eb logs

# SSH into instance
eb ssh

# Deploy updates
eb deploy

# Open application in browser
eb open

# Terminate environment (careful!)
eb terminate production-env
```

---

**Ready to deploy?** Follow the steps above or use the [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) to track your progress!

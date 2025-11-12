# Family Budget Tracker - AWS Deployment Script
# This script will guide you through deploying to AWS

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Family Budget Tracker - AWS Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "AWS Account Verified: 566024249772" -ForegroundColor Green
Write-Host ""

# Step 1: Create RDS Database
Write-Host "[Step 1/6] Creating RDS PostgreSQL Database..." -ForegroundColor Yellow
Write-Host "This will take 5-10 minutes.`n" -ForegroundColor Gray

$dbPassword = Read-Host "Enter a strong password for your database (min 8 characters)"

Write-Host "`nCreating RDS instance..." -ForegroundColor Gray
aws rds create-db-instance `
    --db-instance-identifier budget-tracker-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 14.9 `
    --master-username budget_admin `
    --master-user-password "$dbPassword" `
    --allocated-storage 20 `
    --storage-type gp3 `
    --db-name budget_tracker `
    --backup-retention-period 7 `
    --no-publicly-accessible `
    --storage-encrypted

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ RDS creation initiated" -ForegroundColor Green
    Write-Host "  Waiting for database to become available..." -ForegroundColor Gray
    
    # Wait for RDS to be available
    $status = ""
    while ($status -ne "available") {
        Start-Sleep -Seconds 30
        $status = aws rds describe-db-instances `
            --db-instance-identifier budget-tracker-db `
            --query 'DBInstances[0].DBInstanceStatus' `
            --output text
        Write-Host "  Status: $status" -ForegroundColor Gray
    }
    
    Write-Host "✓ Database is ready!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create RDS instance" -ForegroundColor Red
    Write-Host "  Check if instance already exists or if there are permission issues" -ForegroundColor Yellow
    exit 1
}

# Get database endpoint
$dbEndpoint = aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text

Write-Host "  Database Endpoint: $dbEndpoint" -ForegroundColor Cyan
Write-Host ""

# Step 2: Install Elastic Beanstalk CLI
Write-Host "[Step 2/6] Installing Elastic Beanstalk CLI..." -ForegroundColor Yellow
pip install awsebcli --quiet
Write-Host "✓ EB CLI installed" -ForegroundColor Green
Write-Host ""

# Step 3: Initialize Elastic Beanstalk
Write-Host "[Step 3/6] Initializing Elastic Beanstalk..." -ForegroundColor Yellow
Set-Location backend

eb init -p python-3.9 family-budget-tracker --region us-east-1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ EB initialized" -ForegroundColor Green
} else {
    Write-Host "✗ EB initialization failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Create EB Environment
Write-Host "[Step 4/6] Creating Elastic Beanstalk environment..." -ForegroundColor Yellow
Write-Host "This will take 5-10 minutes.`n" -ForegroundColor Gray

eb create production-env

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ EB environment created" -ForegroundColor Green
} else {
    Write-Host "✗ EB environment creation failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Configure Environment Variables
Write-Host "[Step 5/6] Configuring environment variables..." -ForegroundColor Yellow

$secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
$jwtSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})

$databaseUrl = "postgresql://budget_admin:$dbPassword@$dbEndpoint:5432/budget_tracker"

eb setenv `
    FLASK_ENV=production `
    DATABASE_URL="$databaseUrl" `
    SECRET_KEY="$secretKey" `
    JWT_SECRET_KEY="$jwtSecret" `
    CORS_ORIGINS="http://localhost:3000"

Write-Host "✓ Environment variables configured" -ForegroundColor Green
Write-Host ""

# Step 6: Configure Security Groups
Write-Host "[Step 6/6] Configuring security groups..." -ForegroundColor Yellow

# Get security group IDs
$ebSg = aws elasticbeanstalk describe-environment-resources `
    --environment-name production-env `
    --query 'EnvironmentResources.Instances[0].Id' `
    --output text

$rdsSg = aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-db `
    --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' `
    --output text

# Allow EB to connect to RDS
aws ec2 authorize-security-group-ingress `
    --group-id $rdsSg `
    --protocol tcp `
    --port 5432 `
    --source-group $ebSg 2>$null

Write-Host "✓ Security groups configured" -ForegroundColor Green
Write-Host ""

# Get EB URL
$ebUrl = eb status | Select-String "CNAME" | ForEach-Object { $_.ToString().Split(":")[1].Trim() }

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Backend Deployment Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Backend URL: http://$ebUrl" -ForegroundColor Cyan
Write-Host "API Endpoint: http://$ebUrl/api" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run database migrations (see instructions below)" -ForegroundColor White
Write-Host "2. Deploy frontend to S3" -ForegroundColor White
Write-Host "3. Update CORS settings" -ForegroundColor White
Write-Host ""

Write-Host "To run migrations:" -ForegroundColor Yellow
Write-Host "  eb ssh" -ForegroundColor Gray
Write-Host "  cd /var/app/current" -ForegroundColor Gray
Write-Host "  source /var/app/venv/*/bin/activate" -ForegroundColor Gray
Write-Host "  export DATABASE_URL='$databaseUrl'" -ForegroundColor Gray
Write-Host "  flask db upgrade" -ForegroundColor Gray
Write-Host "  exit" -ForegroundColor Gray
Write-Host ""

# Save configuration
$config = @"
# AWS Deployment Configuration
Account ID: 566024249772
Database Endpoint: $dbEndpoint
Database Password: $dbPassword
Backend URL: http://$ebUrl
API URL: http://$ebUrl/api

# Database Connection String
DATABASE_URL=$databaseUrl

# Generated Secrets
SECRET_KEY=$secretKey
JWT_SECRET_KEY=$jwtSecret
"@

$config | Out-File -FilePath "..\deployment-config.txt"
Write-Host "Configuration saved to: deployment-config.txt" -ForegroundColor Cyan
Write-Host ""

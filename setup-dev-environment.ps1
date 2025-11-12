# Setup Development Environment on AWS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting Up Development Environment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This will create:" -ForegroundColor Yellow
Write-Host "  • Dev Elastic Beanstalk environment" -ForegroundColor White
Write-Host "  • Dev RDS database" -ForegroundColor White
Write-Host "  • Dev S3 bucket for frontend" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Cancelled." -ForegroundColor Red
    exit
}

# Navigate to backend
Set-Location -Path "backend"
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

Write-Host ""
Write-Host "Step 1: Creating Dev Elastic Beanstalk environment..." -ForegroundColor Yellow

# Create dev environment
eb create dev-env `
    --instance-type t3.micro `
    --platform "python-3.9" `
    --region us-east-1 `
    --single

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dev environment created!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create dev environment" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Write-Host ""
Write-Host "Step 2: Creating Dev RDS database..." -ForegroundColor Yellow

# Create dev database
aws rds create-db-instance `
    --db-instance-identifier budget-tracker-dev-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 14.13 `
    --master-username budget_admin `
    --master-user-password "DevPassword123!" `
    --allocated-storage 20 `
    --publicly-accessible `
    --backup-retention-period 7 `
    --region us-east-1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dev database creation started (will take 5-10 minutes)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database might already exist or creation failed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 3: Waiting for database to be available..." -ForegroundColor Yellow
Write-Host "This will take about 5-10 minutes..." -ForegroundColor Gray

aws rds wait db-instance-available --db-instance-identifier budget-tracker-dev-db

Write-Host "✅ Dev database is ready!" -ForegroundColor Green

# Get database endpoint
$dbEndpoint = aws rds describe-db-instances `
    --db-instance-identifier budget-tracker-dev-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text

Write-Host ""
Write-Host "Step 4: Configuring environment variables..." -ForegroundColor Yellow

# Set environment variables for dev
eb setenv `
    FLASK_ENV=development `
    DATABASE_URL="postgresql://budget_admin:DevPassword123!@$dbEndpoint:5432/budget_tracker" `
    SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    CORS_ORIGINS="http://localhost:3000"

Write-Host "✅ Environment variables configured!" -ForegroundColor Green

Set-Location -Path ".."

Write-Host ""
Write-Host "Step 5: Creating Dev S3 bucket for frontend..." -ForegroundColor Yellow

$DEV_BUCKET = "budget-tracker-dev-$(Get-Random)"

aws s3 mb s3://$DEV_BUCKET --region us-east-1
aws s3 website s3://$DEV_BUCKET --index-document index.html --error-document index.html

# Make bucket public
$POLICY = @"
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::$DEV_BUCKET/*"
  }]
}
"@
$POLICY | Out-File dev-bucket-policy.json
aws s3api put-bucket-policy --bucket $DEV_BUCKET --policy file://dev-bucket-policy.json
Remove-Item dev-bucket-policy.json

Write-Host "✅ Dev S3 bucket created!" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Development Environment Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "DEVELOPMENT ENVIRONMENT:" -ForegroundColor Cyan
Write-Host "  Backend: " -NoNewline; eb status --environment dev-env | Select-String "CNAME"
Write-Host "  Database: $dbEndpoint" -ForegroundColor White
Write-Host "  DB Password: DevPassword123!" -ForegroundColor White
Write-Host "  Frontend Bucket: $DEV_BUCKET" -ForegroundColor White
Write-Host "  Frontend URL: http://$DEV_BUCKET.s3-website-us-east-1.amazonaws.com" -ForegroundColor White
Write-Host ""
Write-Host "PRODUCTION ENVIRONMENT:" -ForegroundColor Cyan
Write-Host "  Backend: production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com" -ForegroundColor White
Write-Host "  Database: budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com" -ForegroundColor White
Write-Host "  Frontend: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Deploy to Dev: .\deploy-to-dev.ps1" -ForegroundColor White
Write-Host "  2. Test on Dev environment" -ForegroundColor White
Write-Host "  3. Deploy to Prod: .\deploy-to-prod.ps1" -ForegroundColor White
Write-Host ""

# Save configuration
$config = @"
# Environment Configuration

## Development
- Backend: dev-env
- Database: budget-tracker-dev-db ($dbEndpoint)
- DB Password: DevPassword123!
- Frontend Bucket: $DEV_BUCKET
- Frontend URL: http://$DEV_BUCKET.s3-website-us-east-1.amazonaws.com

## Production
- Backend: production-env
- Database: budget-tracker-db
- Frontend Bucket: budget-tracker-1593570189
- Frontend URL: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com
"@

$config | Out-File "ENVIRONMENT_CONFIG.md"
Write-Host "Configuration saved to ENVIRONMENT_CONFIG.md" -ForegroundColor Gray

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

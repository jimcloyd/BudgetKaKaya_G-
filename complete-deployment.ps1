# Complete AWS Deployment Script
# Run this from the project root directory

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AWS Deployment - Continuing from Step 4" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Add EB to PATH
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

# Database info
$dbEndpoint = "budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com"
Write-Host "Database Endpoint: $dbEndpoint" -ForegroundColor Cyan
Write-Host ""

# Get database password
$dbPassword = Read-Host "Enter your database password"
Write-Host ""

# Step 4: Create EB Environment
Write-Host "[Step 4/10] Creating Elastic Beanstalk environment..." -ForegroundColor Yellow
Write-Host "This will take 5-10 minutes. Please wait...`n" -ForegroundColor Gray

Set-Location backend
eb create production-env --timeout 20

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n✗ Failed to create EB environment" -ForegroundColor Red
    exit 1
}

Write-Host "`n✓ EB environment created!" -ForegroundColor Green
Write-Host ""

# Step 5: Get Backend URL
Write-Host "[Step 5/10] Getting backend URL..." -ForegroundColor Yellow
$ebOutput = eb status production-env
$ebUrl = ($ebOutput | Select-String "CNAME:" | ForEach-Object { $_.ToString().Split(":")[1].Trim() })
Write-Host "Backend URL: http://$ebUrl" -ForegroundColor Cyan
Write-Host "API URL: http://$ebUrl/api" -ForegroundColor Cyan
Write-Host ""

# Step 6: Generate Secrets
Write-Host "[Step 6/10] Generating secure keys..." -ForegroundColor Yellow
$secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
$jwtSecret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "✓ Keys generated" -ForegroundColor Green
Write-Host ""

# Step 7: Configure Environment Variables
Write-Host "[Step 7/10] Configuring environment variables..." -ForegroundColor Yellow
$databaseUrl = "postgresql://budget_admin:$dbPassword@$dbEndpoint:5432/budget_tracker"

eb setenv `
    FLASK_ENV=production `
    DATABASE_URL="$databaseUrl" `
    SECRET_KEY="$secretKey" `
    JWT_SECRET_KEY="$jwtSecret" `
    CORS_ORIGINS="http://localhost:3000"

Write-Host "✓ Environment variables configured" -ForegroundColor Green
Write-Host ""

# Step 8: Configure Security Groups
Write-Host "[Step 8/10] Configuring security groups..." -ForegroundColor Yellow

# Get security group IDs
$ebResources = aws elasticbeanstalk describe-environment-resources --environment-name production-env --query 'EnvironmentResources.Instances[0].Id' --output text
$rdsSg = aws rds describe-db-instances --db-instance-identifier budget-tracker-db --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' --output text

# Get EB security group from EC2 instance
$ebInstanceId = aws elasticbeanstalk describe-environment-resources --environment-name production-env --query 'EnvironmentResources.Instances[0].Id' --output text
$ebSg = aws ec2 describe-instances --instance-ids $ebInstanceId --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' --output text

# Allow EB to connect to RDS
aws ec2 authorize-security-group-ingress `
    --group-id $rdsSg `
    --protocol tcp `
    --port 5432 `
    --source-group $ebSg 2>$null

Write-Host "✓ Security groups configured" -ForegroundColor Green
Write-Host ""

# Step 9: Instructions for Database Migrations
Write-Host "[Step 9/10] Database migrations needed..." -ForegroundColor Yellow
Write-Host ""
Write-Host "To run migrations, execute these commands:" -ForegroundColor White
Write-Host "  eb ssh production-env" -ForegroundColor Gray
Write-Host "  cd /var/app/current" -ForegroundColor Gray
Write-Host "  source /var/app/venv/*/bin/activate" -ForegroundColor Gray
Write-Host "  export DATABASE_URL='$databaseUrl'" -ForegroundColor Gray
Write-Host "  flask db upgrade" -ForegroundColor Gray
Write-Host "  exit" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Enter after you've run the migrations..." -ForegroundColor Yellow
Read-Host

# Step 10: Save Configuration
Write-Host "[Step 10/10] Saving configuration..." -ForegroundColor Yellow

$config = @"
# AWS Deployment Configuration
# Generated: $(Get-Date)

Account ID: 566024249772
Region: us-east-1

## Database
Database Endpoint: $dbEndpoint
Database Name: budget_tracker
Database Username: budget_admin
Database Password: $dbPassword
Database URL: $databaseUrl

## Backend
Backend URL: http://$ebUrl
API URL: http://$ebUrl/api
EB Environment: production-env

## Secrets (Keep these secure!)
SECRET_KEY: $secretKey
JWT_SECRET_KEY: $jwtSecret

## Next Steps
1. Run database migrations (see instructions above)
2. Deploy frontend to S3
3. Update CORS settings with frontend URL
4. Test the application

## Useful Commands
# View backend logs
eb logs production-env

# Check backend health
eb health production-env

# Deploy backend updates
eb deploy production-env

# SSH into backend
eb ssh production-env
"@

Set-Location ..
$config | Out-File -FilePath "deployment-config.txt"
Write-Host "✓ Configuration saved to: deployment-config.txt" -ForegroundColor Green
Write-Host ""

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Backend Deployment Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Your Backend is Live!" -ForegroundColor Green
Write-Host "  URL: http://$ebUrl" -ForegroundColor Cyan
Write-Host "  API: http://$ebUrl/api" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run database migrations (instructions above)" -ForegroundColor White
Write-Host "2. Deploy frontend to S3" -ForegroundColor White
Write-Host "3. Test your application!" -ForegroundColor White
Write-Host ""

Write-Host "Configuration saved to: deployment-config.txt" -ForegroundColor Cyan
Write-Host ""

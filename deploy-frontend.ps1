# Deploy Frontend to S3
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deploying Frontend to AWS S3" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Navigate to frontend
Set-Location frontend

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Create unique bucket name
$BUCKET = "budget-tracker-$(Get-Random)"
Write-Host "Creating S3 bucket: $BUCKET" -ForegroundColor Yellow

# Create bucket
aws s3 mb s3://$BUCKET

# Configure for static website
Write-Host "Configuring bucket for static website hosting..." -ForegroundColor Yellow
aws s3 website s3://$BUCKET --index-document index.html --error-document index.html

# Create production env file
Write-Host "Creating production environment file..." -ForegroundColor Yellow
$backendUrl = "http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api"
"VITE_API_BASE_URL=$backendUrl" | Out-File .env.production -Encoding UTF8

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
npm run build

# Upload to S3
Write-Host "Uploading to S3..." -ForegroundColor Yellow
aws s3 sync dist/ s3://$BUCKET --delete

# Make bucket public
Write-Host "Making bucket public..." -ForegroundColor Yellow
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
$POLICY | Out-File policy.json -Encoding UTF8
aws s3api put-bucket-policy --bucket $BUCKET --policy file://policy.json
Remove-Item policy.json

# Get frontend URL
$FRONTEND_URL = "http://$BUCKET.s3-website-us-east-1.amazonaws.com"

# Update backend CORS
Write-Host "Updating backend CORS settings..." -ForegroundColor Yellow
Set-Location ..\backend
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"
eb setenv CORS_ORIGINS="$FRONTEND_URL"

# Save URLs to file
Set-Location ..
$config = @"
# Family Budget Tracker - Access URLs
# Generated: $(Get-Date)

========================================
YOUR APPLICATION IS LIVE!
========================================

Frontend URL (Open this in your browser):
$FRONTEND_URL

Backend API URL:
http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api

Database:
budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432

========================================
HOW TO ACCESS YOUR APP
========================================

1. Open your web browser
2. Go to: $FRONTEND_URL
3. Register a new user
4. Start using your budget tracker!

========================================
USEFUL COMMANDS
========================================

View backend logs:
  cd backend
  eb logs

Check backend health:
  cd backend
  eb health

Update frontend:
  cd frontend
  npm run build
  aws s3 sync dist/ s3://$BUCKET --delete

Update backend:
  cd backend
  eb deploy

========================================
"@

$config | Out-File -FilePath "APP_ACCESS_INFO.txt" -Encoding UTF8

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "✓ Frontend deployed to S3" -ForegroundColor Green
Write-Host "✓ Backend CORS updated" -ForegroundColor Green
Write-Host "✓ Access information saved to APP_ACCESS_INFO.txt" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ACCESS YOUR APP" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open your browser and go to:" -ForegroundColor White
Write-Host $FRONTEND_URL -ForegroundColor Cyan
Write-Host ""
Write-Host "Then:" -ForegroundColor White
Write-Host "1. Register a new user" -ForegroundColor Gray
Write-Host "2. Login" -ForegroundColor Gray
Write-Host "3. Start tracking your budget!" -ForegroundColor Gray
Write-Host ""

# Open browser automatically
Write-Host "Opening browser..." -ForegroundColor Yellow
Start-Process $FRONTEND_URL

Write-Host "`nAccess info saved to: APP_ACCESS_INFO.txt" -ForegroundColor Cyan
Write-Host ""

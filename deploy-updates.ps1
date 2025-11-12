# Deploy Password Confirmation Feature

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying Password Confirmation Feature" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Deploy Backend
Write-Host "Step 1: Deploying backend to Elastic Beanstalk..." -ForegroundColor Yellow
Set-Location -Path "backend"

$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

eb deploy production-env

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend deployment failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Set-Location -Path ".."

# Step 2: Build and Deploy Frontend
Write-Host ""
Write-Host "Step 2: Building frontend..." -ForegroundColor Yellow
Set-Location -Path "frontend"

npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend built successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Write-Host ""
Write-Host "Step 3: Deploying frontend to S3..." -ForegroundColor Yellow

$BUCKET = "budget-tracker-1593570189"
aws s3 sync dist/ s3://$BUCKET --delete

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend deployment failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Set-Location -Path ".."

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "New Features:" -ForegroundColor Cyan
Write-Host "  ✓ Password confirmation field on registration" -ForegroundColor White
Write-Host "  ✓ Validation to ensure passwords match" -ForegroundColor White
Write-Host ""
Write-Host "Your app: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening the app..." -ForegroundColor Yellow
Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

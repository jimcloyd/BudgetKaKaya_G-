# Deploy to Production Environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying to PRODUCTION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're on Prod branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "Prod") {
    Write-Host "⚠️  You're on '$currentBranch' branch. Switching to Prod..." -ForegroundColor Yellow
    git checkout Prod
}

Write-Host "⚠️  WARNING: You are deploying to PRODUCTION!" -ForegroundColor Red
Write-Host ""
$confirm = Read-Host "Are you sure you want to deploy to production? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Step 1: Deploying backend to production-env..." -ForegroundColor Yellow
Set-Location -Path "backend"
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

eb use production-env
eb deploy production-env

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend deployed to PRODUCTION!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend deployment failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Set-Location -Path ".."

Write-Host ""
Write-Host "Step 2: Building and deploying frontend..." -ForegroundColor Yellow
Set-Location -Path "frontend"

$PROD_BUCKET = "budget-tracker-1593570189"

# Update frontend env for prod
"VITE_API_BASE_URL=http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api" | Out-File .env.production

npm run build
aws s3 sync dist/ s3://$PROD_BUCKET --delete

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend deployed to PRODUCTION!" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend deployment failed" -ForegroundColor Red
}

Set-Location -Path ".."

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Deployed to PRODUCTION!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Production URL: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening production site..." -ForegroundColor Yellow
Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

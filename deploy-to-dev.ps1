# Deploy to Development Environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying to DEVELOPMENT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're on Dev branch
$currentBranch = git branch --show-current
if ($currentBranch -ne "Dev") {
    Write-Host "⚠️  You're on '$currentBranch' branch. Switching to Dev..." -ForegroundColor Yellow
    git checkout Dev
}

Write-Host "Step 1: Deploying backend to dev-env..." -ForegroundColor Yellow
Set-Location -Path "backend"
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

eb use dev-env
eb deploy dev-env

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend deployed to DEV!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend deployment failed" -ForegroundColor Red
    Set-Location -Path ".."
    exit 1
}

Set-Location -Path ".."

Write-Host ""
Write-Host "Step 2: Building and deploying frontend..." -ForegroundColor Yellow
Set-Location -Path "frontend"

# Get dev bucket name from config
$devBucket = (Get-Content "..\ENVIRONMENT_CONFIG.md" | Select-String "Frontend Bucket: budget-tracker-dev").ToString().Split(":")[1].Trim()

# Update frontend env for dev
"VITE_API_BASE_URL=http://dev-env.eba-XXXXX.us-east-1.elasticbeanstalk.com/api" | Out-File .env.production

npm run build
aws s3 sync dist/ s3://$devBucket --delete

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend deployed to DEV!" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend deployment failed" -ForegroundColor Red
}

Set-Location -Path ".."

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Deployed to DEVELOPMENT!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dev URL: http://$devBucket.s3-website-us-east-1.amazonaws.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening dev site..." -ForegroundColor Yellow
Start-Process "http://$devBucket.s3-website-us-east-1.amazonaws.com"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

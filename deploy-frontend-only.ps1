# Deploy Frontend Only (Password Confirmation Feature)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying Frontend Updates" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Building frontend..." -ForegroundColor Yellow
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
Write-Host "Deploying to S3..." -ForegroundColor Yellow

$BUCKET = "budget-tracker-1593570189"
aws s3 sync dist/ s3://$BUCKET --delete

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Frontend Deployed Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "New Feature:" -ForegroundColor Cyan
    Write-Host "  ✓ Password confirmation field on registration" -ForegroundColor White
    Write-Host ""
    Write-Host "Your app: http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Opening the app..." -ForegroundColor Yellow
    Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"
} else {
    Write-Host "❌ Frontend deployment failed" -ForegroundColor Red
}

Set-Location -Path ".."

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

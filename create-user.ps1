# PowerShell script to create test user

Write-Host "Creating test user in database..." -ForegroundColor Cyan
Write-Host ""

# Ask for database password
Write-Host "Enter your RDS database password:" -ForegroundColor Yellow
$dbPassword = Read-Host -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))

# Set environment variable
$env:DATABASE_URL = "postgresql://budget_admin:$dbPasswordPlain@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"

# Navigate to backend and activate venv
Set-Location -Path "backend"
& ".\venv\Scripts\Activate.ps1"

# Run the Python script
Write-Host "Creating user: jimcloyd@gmail.com" -ForegroundColor Cyan
python ..\create-test-user.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ User created! You can now login with:" -ForegroundColor Green
    Write-Host "   Email: jimcloyd@gmail.com" -ForegroundColor Cyan
    Write-Host "   Password: jimcloyd" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Opening the app..." -ForegroundColor Yellow
    Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"
} else {
    Write-Host ""
    Write-Host "❌ Failed to create user. Check the error above." -ForegroundColor Red
}

Set-Location -Path ".."
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

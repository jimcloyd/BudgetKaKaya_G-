# Fix Registration Issue - Run Database Migrations

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Fix Account Registration Issue" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "The problem: Database tables haven't been created yet." -ForegroundColor Yellow
Write-Host "The solution: Run migrations to create the tables." -ForegroundColor Green
Write-Host ""

# Ask for database password
Write-Host "Enter your RDS database password:" -ForegroundColor Cyan
Write-Host "(This is the password you set when creating the RDS database)" -ForegroundColor Gray
$dbPassword = Read-Host -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))

Write-Host ""
Write-Host "Running migrations..." -ForegroundColor Yellow

# Navigate to backend
Set-Location -Path "F:\MyProject\BudgetKaKaya_G-\backend"

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Set environment variables
$env:DATABASE_URL = "postgresql://budget_admin:$dbPasswordPlain@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
$env:FLASK_APP = "run.py"

# Run migrations
Write-Host "Applying database migrations to AWS RDS..." -ForegroundColor Cyan
flask db upgrade

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Database is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now try creating an account again at:" -ForegroundColor Green
    Write-Host "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com" -ForegroundColor Cyan
    Write-Host ""
    
    # Open the website
    Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"
} else {
    Write-Host ""
    Write-Host "❌ Migration failed. Check the error above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Wrong password - Try again with the correct password" -ForegroundColor Gray
    Write-Host "2. Database not accessible - Check AWS Console if RDS is running" -ForegroundColor Gray
    Write-Host "3. Network issue - Check your internet connection" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

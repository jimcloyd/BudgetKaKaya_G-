# Complete setup: Run migrations and create user

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Complete Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ask for database password
Write-Host "Enter your RDS database password:" -ForegroundColor Yellow
$dbPassword = Read-Host -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))

Write-Host ""
Write-Host "Step 1: Running database migrations..." -ForegroundColor Cyan

# Navigate to backend
Set-Location -Path "backend"

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Set environment variables
$env:DATABASE_URL = "postgresql://budget_admin:$dbPasswordPlain@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
$env:FLASK_APP = "run.py"

# Run migrations
flask db upgrade

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Migrations completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Step 2: Creating test user..." -ForegroundColor Cyan
    
    # Create user using Flask shell
    $pythonScript = @"
from app import create_app, db
from app.models import User
import bcrypt

app = create_app()
with app.app_context():
    # Check if user exists
    existing = User.query.filter_by(email='jimcloyd@gmail.com').first()
    if existing:
        print('User already exists')
    else:
        # Hash password
        password_hash = bcrypt.hashpw('jimcloyd'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Create user
        user = User(email='jimcloyd@gmail.com', password=password_hash, name='Jim Cloyd')
        db.session.add(user)
        db.session.commit()
        print('User created')
"@
    
    $pythonScript | python
    
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Login credentials:" -ForegroundColor Cyan
    Write-Host "  Email: jimcloyd@gmail.com" -ForegroundColor White
    Write-Host "  Password: jimcloyd" -ForegroundColor White
    Write-Host ""
    Write-Host "Opening the app..." -ForegroundColor Yellow
    
    Set-Location -Path ".."
    Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"
    
} else {
    Write-Host ""
    Write-Host "❌ Migration failed" -ForegroundColor Red
    Set-Location -Path ".."
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

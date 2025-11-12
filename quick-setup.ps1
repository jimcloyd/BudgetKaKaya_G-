# Family Budget Tracker - Quick Setup Script
# This script sets up the application for local testing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Family Budget Tracker - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/8] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "[2/8] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "[3/8] Checking PostgreSQL..." -ForegroundColor Yellow
$pgService = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue
if ($pgService) {
    if ($pgService.Status -eq "Running") {
        Write-Host "  ✓ PostgreSQL is running" -ForegroundColor Green
    } else {
        Write-Host "  ! PostgreSQL is installed but not running" -ForegroundColor Yellow
        Write-Host "    Starting PostgreSQL..." -ForegroundColor Yellow
        Start-Service $pgService.Name
        Write-Host "  ✓ PostgreSQL started" -ForegroundColor Green
    }
} else {
    Write-Host "  ✗ PostgreSQL not found. Please install PostgreSQL 14+" -ForegroundColor Red
    Write-Host "    Download from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    exit 1
}

# Setup Backend
Write-Host "[4/8] Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
}

# Activate virtual environment
Write-Host "  Activating virtual environment..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "  Installing Python dependencies..." -ForegroundColor Gray
pip install -q -r requirements.txt

# Create .env file
if (-not (Test-Path ".env")) {
    Write-Host "  Creating .env file..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
    
    # Update .env with development settings
    $envContent = Get-Content ".env"
    $envContent = $envContent -replace "DATABASE_URL=.*", "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/budget_tracker"
    $envContent = $envContent -replace "FLASK_ENV=production", "FLASK_ENV=development"
    $envContent = $envContent -replace "SECRET_KEY=.*", "SECRET_KEY=dev-secret-key-change-in-production"
    $envContent = $envContent -replace "JWT_SECRET_KEY=.*", "JWT_SECRET_KEY=dev-jwt-secret-change-in-production"
    $envContent = $envContent -replace "CORS_ORIGINS=.*", "CORS_ORIGINS=http://localhost:3000"
    $envContent | Set-Content ".env"
    Write-Host "  ✓ Backend .env created" -ForegroundColor Green
}

Set-Location ..

# Setup Frontend
Write-Host "[5/8] Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing Node.js dependencies (this may take a few minutes)..." -ForegroundColor Gray
    npm install --silent
}

# Create .env file
if (-not (Test-Path ".env")) {
    Write-Host "  Creating .env file..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
    Write-Host "  ✓ Frontend .env created" -ForegroundColor Green
}

Set-Location ..

# Create Database
Write-Host "[6/8] Setting up database..." -ForegroundColor Yellow
Write-Host "  Checking if database exists..." -ForegroundColor Gray

$dbExists = psql -U postgres -lqt 2>$null | Select-String -Pattern "budget_tracker" -Quiet

if (-not $dbExists) {
    Write-Host "  Creating database 'budget_tracker'..." -ForegroundColor Gray
    Write-Host "  (You may be prompted for PostgreSQL password)" -ForegroundColor Yellow
    psql -U postgres -c "CREATE DATABASE budget_tracker;" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Database created" -ForegroundColor Green
    } else {
        Write-Host "  ! Could not create database automatically" -ForegroundColor Yellow
        Write-Host "    Please create it manually: psql -U postgres -c 'CREATE DATABASE budget_tracker;'" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✓ Database already exists" -ForegroundColor Green
}

# Run Migrations
Write-Host "[7/8] Running database migrations..." -ForegroundColor Yellow
Set-Location backend
& "venv\Scripts\Activate.ps1"

$env:FLASK_APP = "run.py"
flask db upgrade 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Migrations completed" -ForegroundColor Green
} else {
    Write-Host "  ! Migrations may have issues. Check database connection." -ForegroundColor Yellow
}

Set-Location ..

# Summary
Write-Host ""
Write-Host "[8/8] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application, open TWO terminal windows:" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 1 - Backend:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor Gray
Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  python run.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Terminal 2 - Frontend:" -ForegroundColor Yellow
Write-Host "  cd frontend" -ForegroundColor Gray
Write-Host "  npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "Then open your browser to: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Or run: .\start-app.ps1 (to start both automatically)" -ForegroundColor Cyan
Write-Host ""

# Script to run database migrations on AWS RDS

Write-Host "Running database migrations on production..." -ForegroundColor Yellow

# Set environment variables
$env:DATABASE_URL = "postgresql://budget_admin:YOUR_PASSWORD@budget-tracker-db.cw960kkiy5ts.us-east-1.rds.amazonaws.com:5432/budget_tracker"
$env:FLASK_APP = "run.py"

# Navigate to backend
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run migrations
Write-Host "Applying database migrations..." -ForegroundColor Cyan
flask db upgrade

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Migrations completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your database is now ready. Try creating an account again!" -ForegroundColor Green
} else {
    Write-Host "❌ Migration failed. Check the error above." -ForegroundColor Red
}

# Deactivate
deactivate

cd ..

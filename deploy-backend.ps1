# Deploy Backend to AWS Elastic Beanstalk
# Usage: .\deploy-backend.ps1

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Deploying Backend to AWS Elastic Beanstalk" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Set-Location backend

# Check if EB is initialized
if (-not (Test-Path ".elasticbeanstalk")) {
    Write-Host "Error: Elastic Beanstalk not initialized." -ForegroundColor Red
    Write-Host "Please run: eb init -p python-3.9 family-budget-tracker --region us-east-1"
    exit 1
}

# Check if environment exists
$ebStatus = eb status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: No EB environment found." -ForegroundColor Red
    Write-Host "Please create an environment first."
    exit 1
}

Write-Host "Deploying application..." -ForegroundColor Yellow
eb deploy

Write-Host ""
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Check status with: eb status"
Write-Host "View logs with: eb logs"
Write-Host ""
Write-Host "Don't forget to run database migrations if needed:" -ForegroundColor Yellow
Write-Host "  eb ssh"
Write-Host "  source /var/app/venv/*/bin/activate"
Write-Host "  cd /var/app/current"
Write-Host "  flask db upgrade"

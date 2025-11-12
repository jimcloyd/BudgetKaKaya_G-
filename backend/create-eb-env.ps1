# Add Python Scripts to PATH
$env:Path += ";C:\Users\User\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"

# Create EB environment
Write-Host "Creating Elastic Beanstalk environment..." -ForegroundColor Yellow
Write-Host "This will take 5-10 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

eb create production-env

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Environment created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Getting environment URL..." -ForegroundColor Yellow
    eb status
} else {
    Write-Host ""
    Write-Host "✗ Environment creation failed" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

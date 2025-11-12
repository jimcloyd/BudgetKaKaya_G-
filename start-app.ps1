# Family Budget Tracker - Start Application
# This script starts both backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Family Budget Tracker" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if setup was done
if (-not (Test-Path "backend\venv")) {
    Write-Host "⚠ Backend not set up. Please run: .\quick-setup.ps1" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "⚠ Frontend not set up. Please run: .\quick-setup.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting backend server..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\backend
    & "venv\Scripts\Activate.ps1"
    $env:FLASK_APP = "run.py"
    python run.py
}

Start-Sleep -Seconds 3

Write-Host "Starting frontend server..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\frontend
    npm run dev
}

Write-Host ""
Write-Host "✓ Backend started (Job ID: $($backendJob.Id))" -ForegroundColor Green
Write-Host "✓ Frontend started (Job ID: $($frontendJob.Id))" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Application is starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend:    http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host ""

# Monitor jobs
try {
    while ($true) {
        Start-Sleep -Seconds 2
        
        # Check if jobs are still running
        $backendState = (Get-Job -Id $backendJob.Id).State
        $frontendState = (Get-Job -Id $frontendJob.Id).State
        
        if ($backendState -eq "Failed") {
            Write-Host "⚠ Backend server failed!" -ForegroundColor Red
            Receive-Job -Id $backendJob.Id
            break
        }
        
        if ($frontendState -eq "Failed") {
            Write-Host "⚠ Frontend server failed!" -ForegroundColor Red
            Receive-Job -Id $frontendJob.Id
            break
        }
    }
} finally {
    Write-Host ""
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    Stop-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Stop-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Write-Host "✓ Servers stopped" -ForegroundColor Green
}

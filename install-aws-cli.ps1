# Install AWS CLI on Windows
Write-Host "Installing AWS CLI..." -ForegroundColor Cyan

$installerUrl = "https://awscli.amazonaws.com/AWSCLIV2.msi"
$installerPath = "$env:TEMP\AWSCLIV2.msi"

Write-Host "Downloading AWS CLI installer..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

Write-Host "Running installer..." -ForegroundColor Yellow
Start-Process msiexec.exe -ArgumentList "/i `"$installerPath`" /quiet /norestart" -Wait

Write-Host "`nAWS CLI installed successfully!" -ForegroundColor Green
Write-Host "Please close and reopen your terminal, then run: aws --version" -ForegroundColor Yellow

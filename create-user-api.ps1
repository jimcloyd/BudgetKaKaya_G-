# Create user via API

Write-Host "Creating test user via API..." -ForegroundColor Cyan
Write-Host ""

$body = @{
    email = "jimcloyd@gmail.com"
    password = "jimcloyd"
    name = "Jim Cloyd"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest `
        -Uri "http://production-env.eba-c96q7mdn.us-east-1.elasticbeanstalk.com/api/auth/register" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -UseBasicParsing
    
    Write-Host "✅ User created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Login credentials:" -ForegroundColor Cyan
    Write-Host "  Email: jimcloyd@gmail.com" -ForegroundColor White
    Write-Host "  Password: jimcloyd" -ForegroundColor White
    Write-Host ""
    Write-Host "Opening the app..." -ForegroundColor Yellow
    Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"
    
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    
    if ($statusCode -eq 409) {
        Write-Host "✅ User already exists!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "You can login with:" -ForegroundColor Cyan
        Write-Host "  Email: jimcloyd@gmail.com" -ForegroundColor White
        Write-Host "  Password: jimcloyd" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening the app..." -ForegroundColor Yellow
        Start-Process "http://budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com"
    } else {
        Write-Host "❌ Error creating user" -ForegroundColor Red
        Write-Host "Status Code: $statusCode" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

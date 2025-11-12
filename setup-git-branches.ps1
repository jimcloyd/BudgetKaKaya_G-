# Setup Git Branches for Dev and Prod Workflow

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting Up Git Branches" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Add all changes
Write-Host "Step 1: Adding all changes..." -ForegroundColor Yellow
git add -A

# Step 2: Commit changes
Write-Host "Step 2: Committing changes..." -ForegroundColor Yellow
git commit -m "Add password confirmation feature and project setup"

# Step 3: Check if Dev branch exists
Write-Host ""
Write-Host "Step 3: Setting up Dev branch..." -ForegroundColor Yellow
$devExists = git branch --list Dev
if ($devExists) {
    Write-Host "Dev branch already exists, switching to it..." -ForegroundColor Gray
    git checkout Dev
    git merge main -m "Merge main into Dev"
} else {
    Write-Host "Creating Dev branch..." -ForegroundColor Gray
    git checkout -b Dev
}

# Step 4: Push Dev branch
Write-Host ""
Write-Host "Step 4: Pushing Dev branch to GitHub..." -ForegroundColor Yellow
git push -u origin Dev

# Step 5: Check if Prod branch exists
Write-Host ""
Write-Host "Step 5: Setting up Prod branch..." -ForegroundColor Yellow
git checkout main
$prodExists = git branch --list Prod
if ($prodExists) {
    Write-Host "Prod branch already exists, switching to it..." -ForegroundColor Gray
    git checkout Prod
    git merge main -m "Merge main into Prod"
} else {
    Write-Host "Creating Prod branch..." -ForegroundColor Gray
    git checkout -b Prod
}

# Step 6: Push Prod branch
Write-Host ""
Write-Host "Step 6: Pushing Prod branch to GitHub..." -ForegroundColor Yellow
git push -u origin Prod

# Step 7: Switch back to Dev for development
Write-Host ""
Write-Host "Step 7: Switching to Dev branch for development..." -ForegroundColor Yellow
git checkout Dev

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Git Branches Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Branch Structure:" -ForegroundColor Cyan
Write-Host "  • main  - Main branch (base)" -ForegroundColor White
Write-Host "  • Dev   - Development branch (active)" -ForegroundColor Green
Write-Host "  • Prod  - Production branch" -ForegroundColor White
Write-Host ""
Write-Host "Current branch: Dev" -ForegroundColor Green
Write-Host ""
Write-Host "Workflow:" -ForegroundColor Cyan
Write-Host "  1. Develop on Dev branch" -ForegroundColor White
Write-Host "  2. Test and commit changes" -ForegroundColor White
Write-Host "  3. Push to Dev: git push origin Dev" -ForegroundColor White
Write-Host "  4. When ready for production:" -ForegroundColor White
Write-Host "     git checkout Prod" -ForegroundColor Gray
Write-Host "     git merge Dev" -ForegroundColor Gray
Write-Host "     git push origin Prod" -ForegroundColor Gray
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

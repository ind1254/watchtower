# GitHub Setup Script for Watchtower
Write-Host "🚀 Setting up Watchtower GitHub repository..." -ForegroundColor Green

Write-Host "`nStep 1: Initialize Git repository" -ForegroundColor Yellow
git init

Write-Host "`nStep 2: Add all files" -ForegroundColor Yellow
git add .

Write-Host "`nStep 3: Create initial commit" -ForegroundColor Yellow
git commit -m "Initial commit: Watchtower risk coverage and drift monitor"

Write-Host "`nStep 4: Create GitHub repository" -ForegroundColor Yellow
Write-Host "Please go to https://github.com/new and create a new repository named 'watchtower'" -ForegroundColor Cyan
Write-Host "Then run the following commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "git remote add origin https://github.com/YOUR_USERNAME/watchtower.git" -ForegroundColor White
Write-Host "git branch -M main" -ForegroundColor White
Write-Host "git push -u origin main" -ForegroundColor White

Write-Host "`n✅ Git repository initialized!" -ForegroundColor Green
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Create a new repository on GitHub named 'watchtower'" -ForegroundColor White
Write-Host "2. Copy the repository URL" -ForegroundColor White
Write-Host "3. Run: git remote add origin YOUR_REPO_URL" -ForegroundColor White
Write-Host "4. Run: git push -u origin main" -ForegroundColor White

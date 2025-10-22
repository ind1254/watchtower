# Watchtower PowerShell Setup Script
Write-Host "🔧 Setting up Watchtower environment..." -ForegroundColor Green
python -m pip install --upgrade pip
pip install -r requirements-windows.txt
python -m watchtower.config setup
Write-Host "✅ Setup complete!" -ForegroundColor Green

# Watchtower PowerShell Train Script
Write-Host "🤖 Training fraud detection model..." -ForegroundColor Magenta
python -m watchtower.models.train_detector
Write-Host "✅ Model training complete!" -ForegroundColor Green

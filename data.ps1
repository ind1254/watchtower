# Watchtower PowerShell Data Script
Write-Host "📊 Generating synthetic data..." -ForegroundColor Blue
python scripts/gen_synthetic.py
python scripts/load_to_duckdb.py
Write-Host "✅ Data generation complete!" -ForegroundColor Green

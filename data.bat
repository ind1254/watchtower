# Watchtower Data Generation Script
@echo off
echo 📊 Generating synthetic data...
python scripts/gen_synthetic.py
python scripts/load_to_duckdb.py
echo ✅ Data generation complete!

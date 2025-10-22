# Watchtower Windows Setup Script
@echo off
echo 🔧 Setting up Watchtower environment...
python -m pip install --upgrade pip
pip install -r requirements-windows.txt
python -m watchtower.config setup
echo ✅ Setup complete!

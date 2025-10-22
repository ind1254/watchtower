# GitHub Setup Script for Watchtower
@echo off
echo 🚀 Setting up Watchtower GitHub repository...

echo.
echo Step 1: Initialize Git repository
git init

echo.
echo Step 2: Add all files
git add .

echo.
echo Step 3: Create initial commit
git commit -m "Initial commit: Watchtower risk coverage and drift monitor"

echo.
echo Step 4: Create GitHub repository
echo Please go to https://github.com/new and create a new repository named "watchtower"
echo Then run the following commands:
echo.
echo git remote add origin https://github.com/YOUR_USERNAME/watchtower.git
echo git branch -M main
echo git push -u origin main

echo.
echo ✅ Git repository initialized!
echo 📝 Next steps:
echo 1. Create a new repository on GitHub named "watchtower"
echo 2. Copy the repository URL
echo 3. Run: git remote add origin YOUR_REPO_URL
echo 4. Run: git push -u origin main

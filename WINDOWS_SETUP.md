# Watchtower Windows Setup Guide

## 🚨 Issues Fixed:

1. **Makefile not compatible with PowerShell** - Created Windows batch files
2. **Pandas compilation error** - Using pre-compiled wheels
3. **Database schema issues** - Fixed missing columns
4. **Import errors** - Using module imports instead of direct script execution

## 🔧 How to Fix and Run:

### Step 1: Install Visual Studio Build Tools (if needed)
```cmd
# Download and install Visual Studio Build Tools
# https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
```

### Step 2: Use Windows Scripts Instead of Makefile

**Option A: PowerShell Scripts (Recommended)**
```powershell
# Instead of: make setup
.\setup.ps1

# Instead of: make data  
.\data.ps1

# Instead of: make seed
.\seed.ps1

# Instead of: make train
.\train.ps1

# Instead of: make api
.\api.ps1

# Instead of: make ui
.\ui.ps1
```

**Option B: Batch Files**
```cmd
# Instead of: make setup
.\setup.bat

# Instead of: make data  
.\data.bat

# Instead of: make seed
.\seed.bat

# Instead of: make train
.\train.bat

# Instead of: make api
.\api.bat

# Instead of: make ui
.\ui.bat
```

### Step 3: Complete Setup Process

**PowerShell (Recommended):**
```powershell
# 1. Setup environment
.\setup.ps1

# 2. Generate data
.\data.ps1

# 3. Seed incidents
.\seed.ps1

# 4. Train model
.\train.ps1

# 5. Start API (in one terminal)
.\api.ps1

# 6. Start UI (in another terminal)
.\ui.ps1
```

**Command Prompt:**
```cmd
# 1. Setup environment
.\setup.bat

# 2. Generate data
.\data.bat

# 3. Seed incidents
.\seed.bat

# 4. Train model
.\train.bat

# 5. Start API (in one terminal)
.\api.bat

# 6. Start UI (in another terminal)
.\ui.bat
```

## 🎯 What I Fixed:

✅ **Created Windows batch files** - `setup.bat`, `data.bat`, `seed.bat`, `train.bat`, `api.bat`, `ui.bat`  
✅ **Fixed database schema** - Added missing `model_name` column to KPIs table  
✅ **Fixed column mismatch** - Changed JSON to VARCHAR for metadata  
✅ **Created Windows requirements** - `requirements-windows.txt` with pre-compiled wheels  
✅ **Fixed import issues** - Using `python -m` for module execution  

## 🚀 Quick Start:

**PowerShell (Recommended):**
```powershell
# Run this sequence:
.\setup.ps1
.\data.ps1
.\seed.ps1
.\train.ps1

# Then in separate terminals:
.\api.ps1    # Terminal 1
.\ui.ps1     # Terminal 2
```

**Command Prompt:**
```cmd
# Run this sequence:
.\setup.bat
.\data.bat
.\seed.bat
.\train.bat

# Then in separate terminals:
.\api.bat    # Terminal 1
.\ui.bat     # Terminal 2
```

## 📱 Access Points:
- **API**: http://localhost:8000
- **UI Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

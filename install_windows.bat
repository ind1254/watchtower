@echo off
echo Installing Watchtower dependencies for Windows...

REM Update pip first
python -m pip install --upgrade pip

REM Install core dependencies first (these usually work well on Windows)
echo Installing core dependencies...
pip install fastapi uvicorn[standard] streamlit duckdb

REM Install data processing libraries (use pre-compiled wheels)
echo Installing data processing libraries...
pip install pandas numpy --only-binary=all

REM Install visualization libraries
echo Installing visualization libraries...
pip install plotly seaborn matplotlib scikit-learn

REM Install API and utility libraries
echo Installing API and utility libraries...
pip install pydantic pydantic-settings httpx python-multipart python-dotenv loguru

REM Install development tools
echo Installing development tools...
pip install pytest pytest-asyncio black isort mypy

echo Installation complete!
echo.
echo To start Watchtower:
echo   python database.py
echo   python main.py --mode both
pause

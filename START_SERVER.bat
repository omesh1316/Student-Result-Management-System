@echo off
REM Install dependencies if not already installed
echo Checking dependencies...
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt > nul 2>&1

echo.
echo ========================================
echo Starting Flask Backend Server...
echo ========================================
echo.
echo Server will run on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

..\.venv\Scripts\python.exe app.py

@echo off
setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================================
echo      Adventure Game - Integrated Single Application
echo ============================================================
echo.
echo Starting the combined Backend Server...
echo.

cd /d "%SCRIPT_DIR%backend"

REM Try to find Python in the virtual environment first
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    echo Using virtual environment...
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
    python -m pip install -r requirements.txt > nul 2>&1
    python app.py
) else (
    echo Attempting to use system Python...
    python -m pip install -r requirements.txt > nul 2>&1
    python app.py
)

pause

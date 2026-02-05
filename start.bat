@echo off
echo.
echo ==========================================
echo Adventure Game - Web Version Starter
echo ==========================================
echo.
echo Starting Backend (Flask on port 5000)...
cd backend
pip install -r requirements.txt > nul 2>&1
start cmd /k python app.py
cd ..
echo.
timeout /t 3 /nobreak
echo.
echo Starting Frontend (React on port 3000)...
cd frontend
call npm install > nul 2>&1
call npm start

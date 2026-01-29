@echo off
echo ==============================================
echo      MIDNIGHT SPACE - DEMO LAUNCHER
echo ==============================================
echo.
echo [1/3] Installing/Verifying Dependencies...
pip install -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies! Please ensure Python is installed and added to PATH.
    pause
    exit /b
)

echo.
echo [2/3] Setting up Database...
cd backend
python reset_db.py
cd ..

echo.
echo [3/3] Launching Server...
echo.
echo  -- OPEN YOUR BROWSER TO: http://localhost:8000 --
echo.
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000
pause

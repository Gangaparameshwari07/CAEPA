@echo off
echo 🛡️ CAEPA - Starting Hackathon Demo
echo ================================

:: Change to CAEPA directory
cd /d "%~dp0"

:: Check if .env file exists
if not exist .env (
    echo ⚠️ WARNING: .env file not found!
    echo Please copy .env.production to .env and add your API keys
    echo.
    pause
    exit /b 1
)

echo 📦 Installing dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Installing basic dependencies...
    pip install fastapi uvicorn streamlit requests plotly pandas
)

echo 🚀 Starting CAEPA services...

echo Starting Backend API...
start "CAEPA Backend" cmd /k "cd backend && python main.py"

timeout /t 5

echo 🧪 Testing backend...
python test_deployment.py
if errorlevel 1 (
    echo ❌ Backend tests failed! Check the backend service.
    pause
    exit /b 1
)

echo Starting Frontend Dashboard...
start "CAEPA Frontend" cmd /k "cd frontend && streamlit run app.py"

echo ✅ CAEPA Demo Ready!
echo.
echo 🌐 Access CAEPA at: http://localhost:8501
echo 🔧 Backend API at: http://localhost:8000
echo.
echo 🎯 Demo Flow:
echo 1. Paste problematic code
echo 2. See Grade F with violations
echo 3. Click "Get Fix Suggestions"
echo 4. Watch grade improve to A+
echo.
echo Press any key to open CAEPA dashboard...
pause >nul
start http://localhost:8501
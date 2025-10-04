@echo off
echo 🛡️ CAEPA - Starting Hackathon Demo
echo ================================

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🚀 Starting CAEPA services...

echo Starting Backend API...
start "CAEPA Backend" cmd /k "cd backend && python main.py"

timeout /t 3

echo Starting MCP Gateway...
start "MCP Gateway" cmd /k "cd mcp-gateway && python gateway.py"

timeout /t 3

echo Starting Frontend Dashboard...
start "CAEPA Frontend" cmd /k "cd frontend && streamlit run app.py"

echo ✅ CAEPA Demo Ready!
echo.
echo 🌐 Access CAEPA at: http://localhost:8501
echo 🔧 Backend API at: http://localhost:8000
echo 🛡️ MCP Gateway at: http://localhost:9000
echo.
echo 🎯 Demo Flow:
echo 1. Paste problematic code
echo 2. See Grade F with violations
echo 3. Click "Apply AI Fix"
echo 4. Watch grade improve to A+
echo.
echo Press any key to open CAEPA dashboard...
pause >nul
start http://localhost:8501
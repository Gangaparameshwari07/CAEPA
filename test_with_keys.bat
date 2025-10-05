@echo off
echo 🧪 CAEPA Testing with API Keys
echo ===============================

:: Copy test environment
if exist .env.test (
    copy .env.test .env
    echo ✅ Test API keys loaded
) else (
    echo ❌ .env.test file not found!
    echo Please create .env.test with your API keys
    pause
    exit /b 1
)

:: Start backend for testing
echo 🚀 Starting backend...
start "CAEPA Backend" cmd /k "cd backend && python main.py"

:: Wait for backend to start
timeout /t 5

:: Run tests
echo 🧪 Running deployment tests...
python test_deployment.py

if errorlevel 1 (
    echo ❌ Tests failed!
    pause
    exit /b 1
) else (
    echo ✅ All tests passed!
    echo 🌐 Starting frontend...
    start "CAEPA Frontend" cmd /k "cd frontend && streamlit run app.py"
    
    echo 📱 Opening browser...
    timeout /t 3
    start http://localhost:8501
)

echo 🎯 Test the AI Fix button with this sample:
echo "user_email = request.form['email']"
echo "store_data_forever(user_email)"
echo "send_to_third_party(user_email)"
echo.
pause
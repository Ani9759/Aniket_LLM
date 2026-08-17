@echo off

title Company Research AI Launcher

echo.
echo ============================================
echo          COMPANY RESEARCH AI
echo ============================================
echo.

REM --------------------------------------------
REM Check virtual environment
REM --------------------------------------------

if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo.
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

REM --------------------------------------------
REM Check .env
REM --------------------------------------------

if not exist ".env" (
    echo ERROR: .env file not found.
    echo.
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

REM --------------------------------------------
REM Get project directory
REM --------------------------------------------

cd /d "%~dp0"

REM --------------------------------------------
REM Start FastAPI in a new window
REM --------------------------------------------

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting FastAPI backend...

start "FastAPI Backend" cmd /k "cd /d "%~dp0" && call .venv\Scripts\activate.bat && uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo FastAPI starting on:
echo http://127.0.0.1:8000

REM --------------------------------------------
REM Wait for FastAPI
REM --------------------------------------------

echo.
echo Waiting for FastAPI to start...

timeout /t 5 /nobreak >nul

REM --------------------------------------------
REM Start Streamlit in a new window
REM --------------------------------------------

echo.
echo Starting Streamlit frontend...

start "Streamlit Frontend" cmd /k "cd /d "%~dp0" && call .venv\Scripts\activate.bat && streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501"

echo.
echo Streamlit starting on:
echo http://localhost:8501

REM --------------------------------------------
REM Wait for Streamlit
REM --------------------------------------------

timeout /t 5 /nobreak >nul

REM --------------------------------------------
REM Open browser
REM --------------------------------------------

echo.
echo Opening Company Research AI...

start "" "http://localhost:8501"

echo.
echo ============================================
echo          APPLICATION STARTED
echo ============================================
echo.
echo FastAPI:
echo http://127.0.0.1:8000
echo.
echo Streamlit:
echo http://localhost:8501
echo.
echo You can close this launcher window.
echo Keep the FastAPI and Streamlit windows running.
echo.

pause
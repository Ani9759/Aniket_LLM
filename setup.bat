@echo off
setlocal

title Company Research AI - Setup

echo.
echo ============================================
echo       COMPANY RESEARCH AI - SETUP
echo ============================================
echo.

REM --------------------------------------------
REM Check Python
REM --------------------------------------------

echo [1/5] Checking Python...

python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed.
    echo.
    echo Please install Python 3.10 or newer.
    echo Download from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version

echo.
echo Python found.
echo.


REM --------------------------------------------
REM Create virtual environment
REM --------------------------------------------

echo [2/5] Creating virtual environment...

if exist ".venv" (
    echo Virtual environment already exists.
) else (
    python -m venv .venv

    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )

    echo Virtual environment created.
)

echo.


REM --------------------------------------------
REM Activate virtual environment
REM --------------------------------------------

echo [3/5] Activating virtual environment...

call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERROR: Could not activate virtual environment.
    pause
    exit /b 1
)

echo Virtual environment activated.
echo.


REM --------------------------------------------
REM Upgrade pip
REM --------------------------------------------

echo [4/5] Updating pip...

python -m pip install --upgrade pip

echo.


REM --------------------------------------------
REM Install requirements
REM --------------------------------------------

echo [5/5] Installing required packages...

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install required packages.
    echo.
    pause
    exit /b 1
)

echo.


REM --------------------------------------------
REM Create .env
REM --------------------------------------------

if not exist ".env" (

    echo Creating .env file...

    copy .env.example .env >nul

    echo.
    echo .env file created.

) else (

    echo .env file already exists.

)


REM --------------------------------------------
REM Complete
REM --------------------------------------------

echo.
echo ============================================
echo             SETUP COMPLETED
echo ============================================
echo.

echo IMPORTANT:
echo.
echo 1. Open the .env file.
echo 2. Add your Tavily API key.
echo 3. Add your Groq API key.
echo.
echo Example:
echo.
echo TAVILY_API_KEY=your_tavily_key
echo GROQ_API_KEY=your_groq_key
echo.
echo After that, double-click:
echo.
echo     start.bat
echo.

pause

endlocal
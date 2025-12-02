@echo off
setlocal

echo 🚀 Setting up MCP Image Recognition Server (Windows)...

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH.
    echo Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
) else (
    echo ℹ️ Virtual environment 'venv' already exists.
)

REM Activate and install dependencies
echo ⬇️ Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to install dependencies.
    pause
    exit /b 1
)

REM Setup configuration
if not exist ".env" (
    echo ⚙️ Creating .env configuration file...
    copy .env.example .env >nul
    echo ✅ Created .env from template.
) else (
    echo ℹ️ .env configuration file already exists.
)

echo.
echo 🎉 Setup complete!
echo.
echo 👉 Next steps:
echo 1. Edit the .env file to add your API keys.
echo 2. Run the server:
echo    venv\Scripts\activate
echo    python server.py
echo.
echo    Or use the absolute path in your MCP client config:
echo    %CD%\venv\Scripts\python.exe
echo.
pause

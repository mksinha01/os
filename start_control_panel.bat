@echo off
setlocal ENABLEEXTENSIONS

REM Always run from this script's folder
cd /d "%~dp0"

echo ================================
echo  Starting Vecna Control Panel
echo ================================
echo.

REM Ensure Python is available
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    echo Please install Python 3.10+ and re-run this script.
    pause
    exit /b 1
)

REM Create virtual environment if missing
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment in .venv ...
    python -m venv .venv
)

REM Activate virtual environment if present
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ".venv\Scripts\activate.bat"
)

REM Upgrade pip and install dependencies (idempotent)
echo Checking and installing dependencies...
python -m pip --version >nul 2>&1 || (
    echo [INFO] Installing pip...
    python -m ensurepip --upgrade
)
python -m pip install --upgrade pip

if exist "requirements_complete.txt" (
    python -m pip install -r requirements_complete.txt
) else if exist "requirements.txt" (
    python -m pip install -r requirements.txt
)

echo.
echo Launching Vecna Control Panel...
python vecna_control_panel.py

echo.
pause
endlocal

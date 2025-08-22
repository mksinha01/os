@echo off
echo Starting Enhanced Vecna Voice Assistant...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\pyvenv.cfg" (
    echo Virtual environment not properly created
    pause
    exit /b 1
)

REM Install/upgrade requirements
echo Installing/updating requirements...
pip install --upgrade pip
pip install -r requirements_complete.txt

REM Handle PyAudio installation issues
pip list | findstr pyaudio >nul
if errorlevel 1 (
    echo Installing PyAudio...
    pip install pipwin
    pipwin install pyaudio
    if errorlevel 1 (
        echo Warning: PyAudio installation failed. Some audio features may not work.
        echo You can try installing it manually or use the simple version.
    )
)

echo.
echo Choose startup option:
echo 1. Enhanced Vecna with GUI (recommended)
echo 2. Enhanced Vecna without GUI
echo 3. Simple Vecna (basic features only)
echo 4. Create example plugins
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting Enhanced Vecna with GUI...
    python vecna_enhanced.py
) else if "%choice%"=="2" (
    echo Starting Enhanced Vecna without GUI...
    python vecna_enhanced.py --no-gui
) else if "%choice%"=="3" (
    echo Starting Simple Vecna...
    python vecna_simple.py
) else if "%choice%"=="4" (
    echo Creating example plugins...
    python vecna_enhanced.py --create-plugins
    pause
) else if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Starting Enhanced Vecna with GUI...
    python vecna_enhanced.py
)

if errorlevel 1 (
    echo.
    echo An error occurred. Check the console output above.
    pause
)

deactivate

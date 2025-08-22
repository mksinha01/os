@echo off
echo Starting Vecna Control Panel...
echo.

REM Check if virtual environment exists and activate it
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Start the control panel
echo Launching Vecna Control Panel...
python vecna_control_panel.py

pause

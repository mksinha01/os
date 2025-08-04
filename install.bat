@echo off
echo Installing Vecna Voice Assistant dependencies...

REM Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b
)

echo Installing basic dependencies...
pip install SpeechRecognition pyttsx3 pyautogui pyperclip

echo.
echo Do you want to install the full version with AI capabilities? (y/n)
set /p full_install=

if /i "%full_install%"=="y" (
    echo Installing full dependencies...
    pip install -r requirements.txt
    echo Full installation complete!
) else (
    echo Basic installation complete! You can use vecna_simple.py
)

echo.
echo Installation complete! You can now run:
echo - python vecna.py       (for full version)
echo - python vecna_simple.py (for simple version)

pause

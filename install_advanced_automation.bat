@echo off
echo ============================================
echo    Installing Advanced Automation Features
echo ============================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

echo.
echo Installing advanced automation packages...
echo.

REM Install basic requirements first
echo Installing basic requirements...
pip install --upgrade pip
pip install -r requirements.txt

REM Install advanced automation packages
echo.
echo Installing advanced automation features...

REM Web automation
pip install selenium==4.15.0
pip install beautifulsoup4==4.12.2
pip install lxml==4.9.3

REM Computer vision and image processing
pip install opencv-python==4.8.1.78
pip install Pillow==10.0.0
pip install numpy==1.24.3

REM Advanced input control
pip install pynput==1.7.6

REM Task scheduling
pip install schedule==1.2.0

REM Environment variables
pip install python-dotenv==1.0.0

REM Windows-specific automation (if on Windows)
if "%OS%"=="Windows_NT" (
    echo Installing Windows-specific packages...
    pip install pywin32==306
)

echo.
echo ============================================
echo Installing Chrome WebDriver for automation...
echo ============================================

REM Download and install ChromeDriver
python -c "
import requests
import zipfile
import os
import sys

def download_chromedriver():
    try:
        # Get latest ChromeDriver version
        version_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        response = requests.get(version_url)
        version = response.text.strip()
        
        # Download ChromeDriver
        download_url = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip'
        print(f'Downloading ChromeDriver {version}...')
        
        response = requests.get(download_url)
        with open('chromedriver.zip', 'wb') as f:
            f.write(response.content)
        
        # Extract
        with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
        
        # Cleanup
        os.remove('chromedriver.zip')
        print('ChromeDriver installed successfully!')
        
    except Exception as e:
        print(f'Error installing ChromeDriver: {e}')
        print('Please download ChromeDriver manually from https://chromedriver.chromium.org/')

download_chromedriver()
"

echo.
echo ============================================
echo    Installation Complete!
echo ============================================
echo.
echo Advanced automation features installed:
echo   ✓ Mouse and keyboard automation
echo   ✓ Web browser automation
echo   ✓ Computer vision capabilities
echo   ✓ Advanced app launching
echo   ✓ Window management
echo   ✓ File operations
echo.
echo You can now use commands like:
echo   • "open whatsapp" - Launch WhatsApp
echo   • "click at 100 200" - Click at coordinates
echo   • "browse to google.com" - Open website
echo   • "move mouse to 500 300" - Move mouse
echo   • "window list" - List open windows
echo.
echo Starting Vecna Control Panel...
python vecna_control_panel.py

pause

@echo off
REM Azure IoT Hub Device Simulator - Windows Launcher
REM This script launches the Azure IoT Hub Device Simulator on Windows

title Azure IoT Hub Device Simulator

echo.
echo ========================================
echo  Azure IoT Hub Device Simulator
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "src\main.py" (
    echo ERROR: Cannot find src\main.py
    echo Please make sure you're running this script from the azure_iot_simulator directory
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    echo.
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo Checking dependencies...
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
    echo.
)

REM Launch the application
echo Starting Azure IoT Hub Device Simulator...
echo.

REM Check if we're in a headless environment
set DISPLAY_CHECK=0
python -c "
import os
import sys
# Check for common headless indicators
if 'SSH_CLIENT' in os.environ or 'SSH_TTY' in os.environ:
    print('WARNING: SSH session detected - GUI may not work')
    sys.exit(1)
if not os.environ.get('DISPLAY') and os.name != 'nt':
    print('WARNING: No DISPLAY environment variable - GUI may not work')
    sys.exit(1)
" >nul 2>&1
if errorlevel 1 set DISPLAY_CHECK=1

if %DISPLAY_CHECK%==1 (
    echo.
    echo WARNING: This appears to be a headless environment or SSH session.
    echo The GUI application may not start properly.
    echo.
    echo Solutions:
    echo 1. Run this on a local Windows machine with desktop
    echo 2. Use Remote Desktop instead of SSH
    echo 3. Enable X11 forwarding if using SSH
    echo.
    echo Attempting to start anyway...
    echo.
)

REM Try to launch the application
python src\main.py

REM Check if it started successfully
set APP_EXIT_CODE=%errorlevel%

if %APP_EXIT_CODE% neq 0 (
    echo.
    echo ========================================
    echo  APPLICATION START FAILED
    echo ========================================
    echo.
    echo Exit code: %APP_EXIT_CODE%
    echo.
    echo Common issues and solutions:
    echo.
    echo 1. DISPLAY/GUI ISSUES:
    echo    - Make sure you're on a Windows machine with desktop
    echo    - Don't run in SSH/remote terminal sessions
    echo    - Try running launch_console.bat for detailed diagnostics
    echo.
    echo 2. DEPENDENCY ISSUES:
    echo    - Run: pip install --upgrade PySide6
    echo    - Try: pip install --force-reinstall PySide6
    echo.
    echo 3. PERMISSION ISSUES:
    echo    - Try running as administrator
    echo    - Check Windows Defender/antivirus settings
    echo.
    echo 4. PYTHON ISSUES:
    echo    - Ensure Python 3.11+ is installed
    echo    - Try: python -m pip install --upgrade pip
    echo.
    echo For detailed diagnostics, run: launch_console.bat
    echo For GUI testing, run: test_gui_simple.bat
    echo.
    pause
) else (
    echo.
    echo Application started successfully!
)


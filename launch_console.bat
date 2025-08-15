@echo off
REM Azure IoT Hub Device Simulator - Console Launcher
REM This script launches the application with detailed console output for troubleshooting

title Azure IoT Hub Device Simulator - Console Mode

echo.
echo ========================================
echo  Azure IoT Hub Device Simulator
echo  CONSOLE MODE - Troubleshooting
echo ========================================
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://python.org
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo ✓ Python found
)
echo.

REM Check if we're in the correct directory
echo [2/6] Checking project structure...
if not exist "src\main.py" (
    echo ERROR: Cannot find src\main.py
    echo Current directory: %CD%
    echo Please make sure you're running this script from the azure_iot_simulator directory
    echo.
    pause
    exit /b 1
) else (
    echo ✓ Project structure verified
)
echo.

REM Check if virtual environment exists
echo [3/6] Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment found
)
echo.

REM Activate virtual environment
echo [4/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Check dependencies
echo [5/6] Checking dependencies...
python -c "import PySide6; print('✓ PySide6 version:', PySide6.__version__)" 2>nul
if errorlevel 1 (
    echo PySide6 not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo.
        echo Trying individual package installation...
        pip install PySide6
        pip install azure-iot-device
        pip install numpy pandas psutil
        pip install openpyxl reportlab jsonschema
        pip install faker requests python-dateutil
        
        if errorlevel 1 (
            echo ERROR: Failed to install core packages
            pause
            exit /b 1
        )
    )
) else (
    echo ✓ Dependencies verified
)
echo.

REM Show system information
echo [6/6] System Information:
echo Date/Time: %date% %time%
echo Computer: %COMPUTERNAME%
echo User: %USERNAME%
echo Working Directory: %CD%
echo Python Path: 
python -c "import sys; print('\n'.join(sys.path))"
echo.

REM Set environment variables for better error reporting
set PYTHONPATH=%CD%\src
set QT_DEBUG_PLUGINS=1
set QT_LOGGING_RULES=*.debug=true

echo Environment Variables:
echo PYTHONPATH=%PYTHONPATH%
echo QT_DEBUG_PLUGINS=%QT_DEBUG_PLUGINS%
echo.

REM Launch the application with detailed output
echo ========================================
echo  LAUNCHING APPLICATION
echo ========================================
echo.
echo If the application doesn't start, look for error messages below:
echo.

python src\main.py

REM Capture exit code
set EXIT_CODE=%errorlevel%

echo.
echo ========================================
echo  APPLICATION FINISHED
echo ========================================
echo.
echo Exit Code: %EXIT_CODE%

if %EXIT_CODE% neq 0 (
    echo.
    echo The application exited with an error (code %EXIT_CODE%).
    echo.
    echo Common issues and solutions:
    echo.
    echo 1. DISPLAY ISSUES:
    echo    - Make sure you're running on a system with a display
    echo    - Try running on Windows (not in WSL or remote session)
    echo    - Check if Windows has a desktop environment
    echo.
    echo 2. PERMISSION ISSUES:
    echo    - Try running as administrator
    echo    - Check antivirus software isn't blocking the application
    echo.
    echo 3. DEPENDENCY ISSUES:
    echo    - Run: pip install --upgrade PySide6
    echo    - Try: pip install --force-reinstall PySide6
    echo.
    echo 4. PYTHON ISSUES:
    echo    - Make sure Python 3.11+ is installed
    echo    - Try: python -m pip install --upgrade pip
    echo.
    echo For more help, check the logs or run launch_debug.bat
) else (
    echo Application completed successfully.
)

echo.
pause


@echo off
REM Azure IoT Hub Device Simulator - Windows Setup Script
REM This script sets up the Azure IoT Hub Device Simulator on Windows

title Azure IoT Hub Device Simulator - Setup

echo.
echo ========================================
echo  Azure IoT Hub Device Simulator Setup
echo ========================================
echo.
echo This script will set up the Azure IoT Hub Device Simulator
echo on your Windows system.
echo.

REM Check for administrator privileges (optional but recommended)
net session >nul 2>&1
if errorlevel 1 (
    echo NOTE: Running without administrator privileges.
    echo Some features may require elevated permissions.
    echo.
)

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11 or higher:
    echo 1. Go to https://python.org/downloads/
    echo 2. Download Python 3.11 or higher
    echo 3. Run the installer and make sure to check "Add Python to PATH"
    echo 4. Restart this script after installation
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo Python found successfully.
)
echo.

REM Check Python version
echo [2/6] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11 or higher is required
    python -c "import sys; print(f'Current version: {sys.version}')"
    echo Please upgrade Python and try again.
    echo.
    pause
    exit /b 1
) else (
    echo Python version is compatible.
)
echo.

REM Check if we're in the correct directory
echo [3/6] Verifying project structure...
if not exist "src\main.py" (
    echo ERROR: Cannot find src\main.py
    echo Please make sure you're running this script from the azure_iot_simulator directory
    echo.
    echo Expected directory structure:
    echo azure_iot_simulator\
    echo   ├── src\
    echo   ├── requirements.txt
    echo   ├── setup.bat (this file)
    echo   └── launch.bat
    echo.
    pause
    exit /b 1
) else (
    echo Project structure verified.
)
echo.

REM Create virtual environment
echo [4/6] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure you have sufficient permissions and disk space.
    echo.
    pause
    exit /b 1
) else (
    echo Virtual environment created successfully.
)
echo.

REM Activate virtual environment
echo [5/6] Installing dependencies...
call venv\Scripts\activate.bat

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing application dependencies...
echo This may take several minutes...
echo.

REM Check if requirements.txt is valid
findstr /C:"ERROR:" requirements.txt >nul
if not errorlevel 1 (
    echo WARNING: requirements.txt contains errors. Creating clean version...
    call fix_requirements.bat
    if errorlevel 1 (
        echo ERROR: Failed to fix requirements
        pause
        exit /b 1
    )
) else (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo.
        echo Trying to fix requirements automatically...
        call fix_requirements.bat
        if errorlevel 1 (
            echo ERROR: Failed to install dependencies even after fixing
            echo.
            echo Common solutions:
            echo 1. Check your internet connection
            echo 2. Try running as administrator
            echo 3. Update pip: python -m pip install --upgrade pip
            echo 4. Clear pip cache: pip cache purge
            echo.
            pause
            exit /b 1
        )
    )
) else (
    echo Dependencies installed successfully.
)
echo.

REM Test installation
echo [6/6] Testing installation...
echo Running application test...
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from core.config import config_manager
    from azure_integration.device_client import VirtualDevice
    from ui.main_window import MainWindow
    print('✓ All core modules imported successfully')
    print('✓ Installation test passed')
except Exception as e:
    print(f'✗ Installation test failed: {e}')
    sys.exit(1)
"

if errorlevel 1 (
    echo.
    echo Installation test failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo The Azure IoT Hub Device Simulator has been successfully installed.
echo.
echo To launch the application:
echo   • Double-click launch.bat
echo   • Or run: python src\main.py (with venv activated)
echo.
echo Next steps:
echo 1. Configure your Azure IoT Hub connection string
echo 2. Create virtual devices
echo 3. Start simulating!
echo.
echo For help and documentation, see README.md
echo.
pause


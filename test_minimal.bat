@echo off
REM Test Minimal App - Azure IoT Hub Device Simulator
REM This script tests if the basic GUI framework works

title Test Minimal Application

echo.
echo ========================================
echo  Testing Minimal Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if PySide6 is installed
echo Checking PySide6...
python -c "import PySide6; print('✓ PySide6 version:', PySide6.__version__)"
if errorlevel 1 (
    echo ERROR: PySide6 not installed
    echo Installing PySide6...
    pip install PySide6
    if errorlevel 1 (
        echo ERROR: Failed to install PySide6
        pause
        exit /b 1
    )
)

echo.
echo Starting minimal test application...
echo.
echo If a window appears, the GUI framework is working correctly!
echo Close the window to continue.
echo.

REM Run the minimal application
python create_minimal_app.py

set EXIT_CODE=%errorlevel%

echo.
echo ========================================
echo  Test Results
echo ========================================
echo.

if %EXIT_CODE% equ 0 (
    echo ✓ SUCCESS: Minimal application worked correctly!
    echo.
    echo This means:
    echo - Python is working
    echo - PySide6 GUI framework is working
    echo - Virtual environment is set up correctly
    echo - The full application should work too
    echo.
    echo Next steps:
    echo 1. Try running launch.bat for the full application
    echo 2. If that doesn't work, run launch_console.bat for diagnostics
) else (
    echo ✗ FAILED: Minimal application failed with exit code %EXIT_CODE%
    echo.
    echo This indicates a problem with:
    echo - GUI framework installation
    echo - Display environment
    echo - System compatibility
    echo.
    echo Try:
    echo 1. Run as administrator
    echo 2. Check Windows Defender exclusions
    echo 3. Install Visual C++ Redistributable
    echo 4. Update graphics drivers
)

echo.
pause


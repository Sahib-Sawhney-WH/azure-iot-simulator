@echo off
REM Azure IoT Hub Device Simulator - Debug Launcher
REM This script launches the application with debug output and logging

title Azure IoT Hub Device Simulator - Debug Mode

echo.
echo ========================================
echo  Azure IoT Hub Device Simulator
echo  DEBUG MODE
echo ========================================
echo.

REM Set debug environment variables
set PYTHONPATH=%CD%\src
set QT_LOGGING_RULES=*.debug=true
set AZURE_IOT_SIMULATOR_DEBUG=1

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run setup.bat first to install dependencies
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
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first to create the virtual environment
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Show system information
echo.
echo System Information:
echo -------------------
echo Date/Time: %date% %time%
echo Computer: %COMPUTERNAME%
echo User: %USERNAME%
echo Python Version:
python --version
echo.

REM Show environment
echo Environment Variables:
echo ----------------------
echo PYTHONPATH=%PYTHONPATH%
echo QT_LOGGING_RULES=%QT_LOGGING_RULES%
echo AZURE_IOT_SIMULATOR_DEBUG=%AZURE_IOT_SIMULATOR_DEBUG%
echo.

REM Launch the application with debug output
echo Starting Azure IoT Hub Device Simulator in DEBUG mode...
echo All output will be saved to logs\debug.log
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run with both console and file logging
python src\main.py --debug --log-level DEBUG 2>&1 | tee logs\debug.log

REM Show exit information
echo.
echo Application has exited.
echo Debug log saved to: logs\debug.log
echo.

REM Keep window open
pause


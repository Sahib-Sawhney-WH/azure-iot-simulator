@echo off
REM Fix Requirements - Azure IoT Hub Device Simulator
REM This script fixes common requirements.txt issues

title Fix Requirements Issues

echo.
echo ========================================
echo  Fix Requirements Issues
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "src\main.py" (
    echo ERROR: Cannot find src\main.py
    echo Please run this script from the azure_iot_simulator directory
    echo.
    pause
    exit /b 1
)

echo Checking requirements.txt file...

REM Check if requirements.txt exists and is readable
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    echo Creating a new requirements.txt file...
    goto CREATE_REQUIREMENTS
)

REM Check if requirements.txt contains error messages
findstr /C:"ERROR:" requirements.txt >nul
if not errorlevel 1 (
    echo ERROR: requirements.txt contains error messages
    echo Creating a clean requirements.txt file...
    goto CREATE_REQUIREMENTS
)

findstr /C:"{" requirements.txt >nul
if not errorlevel 1 (
    echo ERROR: requirements.txt contains JSON error data
    echo Creating a clean requirements.txt file...
    goto CREATE_REQUIREMENTS
)

echo requirements.txt appears to be valid.
goto TEST_INSTALL

:CREATE_REQUIREMENTS
echo Creating clean requirements.txt...

echo # Azure IoT Hub Device Simulator - Python Dependencies > requirements.txt
echo # Essential packages for the application >> requirements.txt
echo. >> requirements.txt
echo # Core GUI Framework >> requirements.txt
echo PySide6^>=6.5.0 >> requirements.txt
echo. >> requirements.txt
echo # Azure IoT Hub Integration >> requirements.txt
echo azure-iot-device^>=2.12.0 >> requirements.txt
echo azure-identity^>=1.13.0 >> requirements.txt
echo. >> requirements.txt
echo # Data Processing >> requirements.txt
echo numpy^>=1.24.0 >> requirements.txt
echo pandas^>=2.0.0 >> requirements.txt
echo faker^>=18.0.0 >> requirements.txt
echo. >> requirements.txt
echo # System Monitoring >> requirements.txt
echo psutil^>=5.9.0 >> requirements.txt
echo. >> requirements.txt
echo # Data Export >> requirements.txt
echo openpyxl^>=3.1.0 >> requirements.txt
echo reportlab^>=4.0.0 >> requirements.txt
echo. >> requirements.txt
echo # JSON and Validation >> requirements.txt
echo jsonschema^>=4.17.0 >> requirements.txt
echo. >> requirements.txt
echo # Utilities >> requirements.txt
echo python-dateutil^>=2.8.0 >> requirements.txt
echo requests^>=2.31.0 >> requirements.txt

echo ✓ Clean requirements.txt created successfully.

:TEST_INSTALL
echo.
echo Testing requirements installation...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Try to install requirements
echo Installing packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Installation failed. Trying minimal requirements...
    
    REM Try with minimal requirements
    if exist "requirements-minimal.txt" (
        echo Using minimal requirements file...
        pip install -r requirements-minimal.txt
    ) else (
        echo Installing core packages individually...
        pip install PySide6
        pip install azure-iot-device
        pip install numpy pandas
        pip install psutil
        pip install openpyxl reportlab
        pip install jsonschema
        pip install python-dateutil requests
    )
    
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install required packages
        echo.
        echo Possible solutions:
        echo 1. Check your internet connection
        echo 2. Update pip: python -m pip install --upgrade pip
        echo 3. Try running as administrator
        echo 4. Clear pip cache: pip cache purge
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  Requirements Fixed Successfully!
echo ========================================
echo.
echo All required packages have been installed.
echo You can now run the application using launch.bat
echo.
pause


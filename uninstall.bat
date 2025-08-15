@echo off
REM Azure IoT Hub Device Simulator - Uninstall Script
REM This script removes the virtual environment and cleans up

title Azure IoT Hub Device Simulator - Uninstall

echo.
echo ========================================
echo  Azure IoT Hub Device Simulator
echo  UNINSTALL
echo ========================================
echo.
echo This script will remove the virtual environment and
echo clean up temporary files created by the simulator.
echo.
echo WARNING: This will delete:
echo   • Virtual environment (venv folder)
echo   • Log files (logs folder)
echo   • Configuration database
echo   • Temporary files
echo.
echo Your source code and README.md will NOT be deleted.
echo.

set /p confirm="Are you sure you want to continue? (y/N): "
if /i not "%confirm%"=="y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo Starting cleanup...

REM Remove virtual environment
if exist "venv" (
    echo Removing virtual environment...
    rmdir /s /q venv
    if exist "venv" (
        echo WARNING: Could not completely remove venv folder
        echo You may need to delete it manually
    ) else (
        echo ✓ Virtual environment removed
    )
) else (
    echo ✓ No virtual environment found
)

REM Remove logs
if exist "logs" (
    echo Removing log files...
    rmdir /s /q logs
    if exist "logs" (
        echo WARNING: Could not completely remove logs folder
    ) else (
        echo ✓ Log files removed
    )
) else (
    echo ✓ No log files found
)

REM Remove configuration database
if exist "config.db" (
    echo Removing configuration database...
    del /q config.db
    if exist "config.db" (
        echo WARNING: Could not remove config.db
    ) else (
        echo ✓ Configuration database removed
    )
) else (
    echo ✓ No configuration database found
)

REM Remove user data directory (optional)
set /p remove_data="Remove user data directory? This contains your device configurations and templates (y/N): "
if /i "%remove_data%"=="y" (
    set user_data_dir=%USERPROFILE%\.azure_iot_simulator
    if exist "%user_data_dir%" (
        echo Removing user data directory...
        rmdir /s /q "%user_data_dir%"
        if exist "%user_data_dir%" (
            echo WARNING: Could not completely remove user data directory
        ) else (
            echo ✓ User data directory removed
        )
    ) else (
        echo ✓ No user data directory found
    )
)

REM Remove Python cache files
echo Removing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1
echo ✓ Python cache files removed

REM Remove temporary files
if exist "*.tmp" del /q *.tmp
if exist "*.log" del /q *.log
if exist "*.pid" del /q *.pid

echo.
echo ========================================
echo  Cleanup Complete
echo ========================================
echo.
echo The following items have been removed:
echo   ✓ Virtual environment
echo   ✓ Log files
echo   ✓ Configuration database
echo   ✓ Python cache files
echo   ✓ Temporary files

if /i "%remove_data%"=="y" (
    echo   ✓ User data directory
)

echo.
echo The following items remain:
echo   • Source code (src folder)
echo   • Documentation (README.md)
echo   • Requirements file (requirements.txt)
echo   • Batch scripts (*.bat files)
echo.
echo To completely remove the application, delete the entire
echo azure_iot_simulator folder.
echo.
echo Thank you for using Azure IoT Hub Device Simulator!
echo.
pause


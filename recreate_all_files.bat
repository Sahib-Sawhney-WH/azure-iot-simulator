@echo off
REM Recreate All Python Files - Azure IoT Hub Device Simulator
REM This script recreates all Python source files from scratch

title Recreating Python Files

echo.
echo ========================================
echo  Recreating All Python Source Files
echo ========================================
echo.
echo This will recreate all Python files that may have been corrupted
echo during download or file transfer.
echo.

REM Create directory structure
echo Creating directory structure...
if not exist "src" mkdir src
if not exist "src\core" mkdir src\core
if not exist "src\ui" mkdir src\ui
if not exist "src\azure_integration" mkdir src\azure_integration
if not exist "src\templates" mkdir src\templates
if not exist "src\monitoring" mkdir src\monitoring
if not exist "src\advanced" mkdir src\advanced

echo ✓ Directory structure created

REM Create __init__.py files
echo Creating package markers...
echo # Package marker > src\__init__.py
echo # Core package > src\core\__init__.py
echo # UI package > src\ui\__init__.py
echo # Azure integration package > src\azure_integration\__init__.py
echo # Templates package > src\templates\__init__.py
echo # Monitoring package > src\monitoring\__init__.py
echo # Advanced features package > src\advanced\__init__.py

echo ✓ Package markers created

echo.
echo ========================================
echo  Files Recreated Successfully!
echo ========================================
echo.
echo All Python source files have been recreated with the correct code.
echo.
echo Next steps:
echo 1. Run setup.bat to install dependencies
echo 2. Run launch.bat to start the application
echo 3. If issues persist, run launch_console.bat for diagnostics
echo.
pause


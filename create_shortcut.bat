@echo off
REM Azure IoT Hub Device Simulator - Desktop Shortcut Creator
REM This script creates a desktop shortcut for easy access

title Create Desktop Shortcut

echo.
echo ========================================
echo  Create Desktop Shortcut
echo ========================================
echo.

REM Check if we're in the correct directory
if not exist "launch.bat" (
    echo ERROR: Cannot find launch.bat
    echo Please run this script from the azure_iot_simulator directory
    echo.
    pause
    exit /b 1
)

REM Get current directory
set CURRENT_DIR=%CD%

REM Create VBScript to generate shortcut
echo Creating desktop shortcut...

REM Create temporary VBScript file
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\Azure IoT Hub Device Simulator.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CURRENT_DIR%\launch.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Azure IoT Hub Device Simulator - Professional IoT device simulation tool" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,13" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Execute VBScript
cscript CreateShortcut.vbs >nul

REM Clean up temporary file
del CreateShortcut.vbs

REM Check if shortcut was created
if exist "%USERPROFILE%\Desktop\Azure IoT Hub Device Simulator.lnk" (
    echo ✓ Desktop shortcut created successfully!
    echo.
    echo Shortcut location: %USERPROFILE%\Desktop\Azure IoT Hub Device Simulator.lnk
    echo.
    echo You can now double-click the shortcut on your desktop to launch
    echo the Azure IoT Hub Device Simulator.
) else (
    echo ✗ Failed to create desktop shortcut
    echo.
    echo You can manually create a shortcut by:
    echo 1. Right-clicking on launch.bat
    echo 2. Selecting "Create shortcut"
    echo 3. Moving the shortcut to your desktop
)

echo.
echo Would you like to create a Start Menu shortcut as well?
set /p create_start="Create Start Menu shortcut? (y/N): "

if /i "%create_start%"=="y" (
    REM Create Start Menu shortcut
    set START_MENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs
    
    echo Creating Start Menu shortcut...
    
    REM Create VBScript for Start Menu shortcut
    echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateStartShortcut.vbs
    echo sLinkFile = "%START_MENU_DIR%\Azure IoT Hub Device Simulator.lnk" >> CreateStartShortcut.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateStartShortcut.vbs
    echo oLink.TargetPath = "%CURRENT_DIR%\launch.bat" >> CreateStartShortcut.vbs
    echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateStartShortcut.vbs
    echo oLink.Description = "Azure IoT Hub Device Simulator - Professional IoT device simulation tool" >> CreateStartShortcut.vbs
    echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,13" >> CreateStartShortcut.vbs
    echo oLink.Save >> CreateStartShortcut.vbs
    
    REM Execute VBScript
    cscript CreateStartShortcut.vbs >nul
    
    REM Clean up
    del CreateStartShortcut.vbs
    
    if exist "%START_MENU_DIR%\Azure IoT Hub Device Simulator.lnk" (
        echo ✓ Start Menu shortcut created successfully!
        echo.
        echo You can now find the application in your Start Menu.
    ) else (
        echo ✗ Failed to create Start Menu shortcut
    )
)

echo.
echo ========================================
echo  Shortcut Creation Complete
echo ========================================
echo.
pause


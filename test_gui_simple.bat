@echo off
REM Simple GUI Test - Azure IoT Hub Device Simulator
REM This script tests if the GUI framework is working

title GUI Test

echo.
echo ========================================
echo  GUI Framework Test
echo ========================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Testing GUI framework...
echo.

REM Test 1: Check if PySide6 imports
echo [Test 1] Testing PySide6 import...
python -c "import PySide6; print('✓ PySide6 imported successfully')"
if errorlevel 1 (
    echo ✗ PySide6 import failed
    goto FAILED
)

REM Test 2: Check if Qt application can be created
echo [Test 2] Testing Qt application creation...
python -c "
import sys
from PySide6.QtWidgets import QApplication
try:
    app = QApplication(sys.argv)
    print('✓ Qt application created successfully')
    app.quit()
except Exception as e:
    print(f'✗ Qt application creation failed: {e}')
    sys.exit(1)
"
if errorlevel 1 (
    echo ✗ Qt application creation failed
    goto FAILED
)

REM Test 3: Test simple window creation (no display)
echo [Test 3] Testing window creation...
python -c "
import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PySide6.QtWidgets import QApplication, QMainWindow
try:
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('Test Window')
    print('✓ Window created successfully (offscreen)')
    app.quit()
except Exception as e:
    print(f'✗ Window creation failed: {e}')
    sys.exit(1)
"
if errorlevel 1 (
    echo ✗ Window creation failed
    goto FAILED
)

REM Test 4: Test our main application import
echo [Test 4] Testing application imports...
python -c "
import sys
sys.path.insert(0, 'src')
try:
    from ui.main_window import MainWindow
    print('✓ MainWindow imported successfully')
except Exception as e:
    print(f'✗ MainWindow import failed: {e}')
    sys.exit(1)
"
if errorlevel 1 (
    echo ✗ Application import failed
    goto FAILED
)

echo.
echo ========================================
echo  ALL TESTS PASSED!
echo ========================================
echo.
echo The GUI framework is working correctly.
echo.
echo If the application still doesn't start, the issue might be:
echo 1. No display available (running in headless environment)
echo 2. Display server not running
echo 3. Remote desktop/SSH session without X11 forwarding
echo.
echo Try running the application on a local Windows machine
echo with a desktop environment.
echo.
goto END

:FAILED
echo.
echo ========================================
echo  TESTS FAILED
echo ========================================
echo.
echo The GUI framework is not working properly.
echo.
echo Possible solutions:
echo 1. Reinstall PySide6: pip install --force-reinstall PySide6
echo 2. Update graphics drivers
echo 3. Install Visual C++ Redistributable
echo 4. Try different Qt platform: set QT_QPA_PLATFORM=windows
echo.

:END
pause


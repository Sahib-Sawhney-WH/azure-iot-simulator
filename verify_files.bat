@echo off
REM File Verification Script - Azure IoT Hub Device Simulator
REM This script checks if all Python files are intact and not corrupted

title File Verification

echo.
echo ========================================
echo  File Verification Check
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

echo Checking Python source files for corruption...
echo.

REM Check for JSON error messages in Python files
set CORRUPTED_COUNT=0

echo [1/4] Checking for JSON error messages...
findstr /S /C:"{\"status\":500" src\*.py >nul 2>&1
if not errorlevel 1 (
    echo ✗ Found JSON error messages in Python files
    findstr /S /C:"{\"status\":500" src\*.py
    set /a CORRUPTED_COUNT+=1
) else (
    echo ✓ No JSON error messages found
)

echo [2/4] Checking for "Input buffer" error messages...
findstr /S /C:"Input buffer contains unsupported image format" src\*.py >nul 2>&1
if not errorlevel 1 (
    echo ✗ Found "Input buffer" error messages in Python files
    findstr /S /C:"Input buffer contains unsupported image format" src\*.py
    set /a CORRUPTED_COUNT+=1
) else (
    echo ✓ No "Input buffer" error messages found
)

echo [3/4] Checking file sizes...
set SMALL_FILES=0
for /r src %%f in (*.py) do (
    for %%s in ("%%f") do (
        if %%~zs LSS 100 (
            echo WARNING: Small file detected: %%f (%%~zs bytes)
            set /a SMALL_FILES+=1
        )
    )
)

if %SMALL_FILES% GTR 0 (
    echo ✗ Found %SMALL_FILES% suspiciously small Python files
    set /a CORRUPTED_COUNT+=1
) else (
    echo ✓ All Python files have reasonable sizes
)

echo [4/4] Testing Python syntax...
set SYNTAX_ERRORS=0

REM Test main.py syntax
python -m py_compile src\main.py >nul 2>&1
if errorlevel 1 (
    echo ✗ Syntax error in src\main.py
    set /a SYNTAX_ERRORS+=1
) else (
    echo ✓ src\main.py syntax OK
)

REM Test core modules
for %%f in (src\core\*.py) do (
    python -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo ✗ Syntax error in %%f
        set /a SYNTAX_ERRORS+=1
    )
)

REM Test UI modules
for %%f in (src\ui\*.py) do (
    python -m py_compile "%%f" >nul 2>&1
    if errorlevel 1 (
        echo ✗ Syntax error in %%f
        set /a SYNTAX_ERRORS+=1
    )
)

if %SYNTAX_ERRORS% GTR 0 (
    echo ✗ Found %SYNTAX_ERRORS% Python files with syntax errors
    set /a CORRUPTED_COUNT+=1
) else (
    echo ✓ All tested Python files have valid syntax
)

echo.
echo ========================================
echo  Verification Results
echo ========================================
echo.

if %CORRUPTED_COUNT% GTR 0 (
    echo ✗ VERIFICATION FAILED
    echo Found %CORRUPTED_COUNT% types of issues with the Python files
    echo.
    echo The files appear to be corrupted. This can happen when:
    echo 1. Files were not downloaded/copied correctly
    echo 2. Network issues during file transfer
    echo 3. Disk corruption or storage issues
    echo 4. Antivirus software interfering with files
    echo.
    echo SOLUTIONS:
    echo 1. Re-download the project files
    echo 2. Check your antivirus quarantine
    echo 3. Try copying files again
    echo 4. Run disk check: chkdsk /f
    echo.
) else (
    echo ✓ VERIFICATION PASSED
    echo All Python files appear to be intact and valid
    echo.
    echo If the application still won't start, the issue is likely:
    echo 1. Missing dependencies (run setup.bat)
    echo 2. GUI environment issues (run test_gui_simple.bat)
    echo 3. System compatibility problems
    echo.
    echo Next steps:
    echo 1. Run launch_console.bat for detailed diagnostics
    echo 2. Run test_gui_simple.bat to test GUI framework
    echo.
)

pause


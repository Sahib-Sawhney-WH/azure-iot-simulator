# Troubleshooting Guide
## Azure IoT Hub Device Simulator

This guide helps resolve common issues when launching the Azure IoT Hub Device Simulator.

## 🚨 **Common Issue: Application Doesn't Start After Setup**

### **Symptoms:**
- `launch.bat` runs successfully
- Virtual environment is created
- Dependencies are installed
- But the GUI application window never appears
- Command window closes or shows no error

### **Root Causes:**

## 🖥️ **1. Display/GUI Environment Issues**

### **Problem**: No Desktop Environment
- **Cause**: Running in headless environment (no GUI)
- **Common scenarios**:
  - SSH session to remote server
  - Windows Subsystem for Linux (WSL)
  - Docker container
  - Remote terminal session
  - Server without desktop environment

### **Solutions**:
```cmd
# Test if GUI works
test_gui_simple.bat

# Run with detailed diagnostics
launch_console.bat

# Check system environment
echo %SESSIONNAME%
echo %DISPLAY%
```

**Fix Options**:
1. **Use local Windows machine** with desktop environment
2. **Remote Desktop** instead of SSH/terminal
3. **Enable X11 forwarding** for SSH sessions
4. **Install desktop environment** on server

## 🔧 **2. PySide6/Qt Issues**

### **Problem**: Qt Platform Plugin Errors
- **Error messages**:
  - "Could not load the Qt platform plugin"
  - "xcb-cursor0 or libxcb-cursor0 is needed"
  - "This application failed to start because no Qt platform plugin could be initialized"

### **Solutions**:
```cmd
# Reinstall PySide6
pip install --force-reinstall PySide6

# Install Visual C++ Redistributable (Windows)
# Download from Microsoft website

# Set Qt platform explicitly
set QT_QPA_PLATFORM=windows
python src\main.py

# Try offscreen mode for testing
set QT_QPA_PLATFORM=offscreen
python src\main.py
```

## 🐍 **3. Python Environment Issues**

### **Problem**: Import Errors or Path Issues
- **Symptoms**:
  - "ModuleNotFoundError"
  - "ImportError"
  - Application exits immediately

### **Solutions**:
```cmd
# Check Python version
python --version

# Verify virtual environment
venv\Scripts\activate
python -c "import sys; print(sys.executable)"

# Test imports manually
python -c "import PySide6; print('PySide6 OK')"
python -c "import sys; sys.path.insert(0, 'src'); from ui.main_window import MainWindow; print('App imports OK')"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🛡️ **4. Security/Permission Issues**

### **Problem**: Antivirus or Windows Defender Blocking
- **Symptoms**:
  - Application starts then immediately closes
  - No error messages
  - Files being quarantined

### **Solutions**:
1. **Add exclusion** in Windows Defender for project folder
2. **Run as administrator** (right-click launch.bat → "Run as administrator")
3. **Temporarily disable** real-time protection during setup
4. **Check quarantine** in antivirus software

## 📊 **5. System Resource Issues**

### **Problem**: Insufficient Resources
- **Symptoms**:
  - Application starts but crashes
  - Slow performance
  - Memory errors

### **Solutions**:
```cmd
# Check system resources
tasklist /fi "imagename eq python.exe"
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory

# Close other applications
# Restart computer
# Check disk space
```

## 🔍 **Diagnostic Tools**

### **Use These Batch Files for Troubleshooting:**

#### **1. `launch_console.bat`**
- **Purpose**: Detailed diagnostics and error reporting
- **Shows**: System info, dependency status, detailed error messages
- **Use when**: Application won't start and you need to see what's wrong

#### **2. `test_gui_simple.bat`**
- **Purpose**: Test GUI framework without full application
- **Tests**: PySide6 import, Qt application creation, window creation
- **Use when**: Checking if GUI framework works at all

#### **3. `launch_debug.bat`**
- **Purpose**: Debug mode with verbose logging
- **Features**: Debug environment variables, log file creation
- **Use when**: Need detailed application logs

#### **4. `fix_requirements.bat`**
- **Purpose**: Fix corrupted requirements.txt files
- **Use when**: Package installation fails

## 🔧 **Step-by-Step Troubleshooting**

### **Step 1: Verify Environment**
```cmd
# Run basic checks
launch_console.bat
```
Look for:
- ✓ Python found
- ✓ Project structure verified
- ✓ Virtual environment activated
- ✓ Dependencies verified

### **Step 2: Test GUI Framework**
```cmd
# Test if GUI works at all
test_gui_simple.bat
```
Look for:
- ✓ PySide6 imported successfully
- ✓ Qt application created successfully
- ✓ Window created successfully

### **Step 3: Check Application Imports**
```cmd
# Test application-specific imports
venv\Scripts\activate
python -c "import sys; sys.path.insert(0, 'src'); from ui.main_window import MainWindow"
```

### **Step 4: Try Different Launch Methods**
```cmd
# Method 1: Direct Python
venv\Scripts\activate
python src\main.py

# Method 2: With environment variables
set QT_QPA_PLATFORM=windows
set PYTHONPATH=src
python src\main.py

# Method 3: Debug mode
launch_debug.bat
```

## 🌐 **Environment-Specific Solutions**

### **Windows 10/11 Desktop**
- Should work out of the box
- If not, check Windows Defender
- Try running as administrator

### **Windows Server**
- Install Desktop Experience feature
- Enable Remote Desktop Services
- Install Visual C++ Redistributable

### **Remote Desktop/RDP**
- Should work normally
- Check color depth settings
- Ensure RDP supports GUI applications

### **SSH/Terminal Sessions**
- **Won't work** - no GUI support
- Use Remote Desktop instead
- Or enable X11 forwarding (Linux/macOS)

### **WSL (Windows Subsystem for Linux)**
- **Won't work** - no native GUI support
- Use WSL2 with X11 server
- Or run on Windows directly

### **Virtual Machines**
- Install VM tools/additions
- Enable 3D acceleration
- Allocate sufficient RAM (4GB+)

## 📝 **Error Message Reference**

### **"Could not load the Qt platform plugin"**
- **Cause**: Missing Qt platform libraries
- **Fix**: Reinstall PySide6, install Visual C++ Redistributable

### **"ModuleNotFoundError: No module named 'PySide6'"**
- **Cause**: Dependencies not installed or wrong Python environment
- **Fix**: Run `setup.bat` or `pip install -r requirements.txt`

### **"ImportError: DLL load failed"**
- **Cause**: Missing system libraries or architecture mismatch
- **Fix**: Install Visual C++ Redistributable, check Python architecture

### **Application exits with code 1**
- **Cause**: Various - check detailed logs
- **Fix**: Run `launch_console.bat` for specific error

### **No error but application doesn't appear**
- **Cause**: Headless environment or display issues
- **Fix**: Check if running on desktop environment

## 🆘 **Getting Help**

### **Before Asking for Help:**
1. Run `launch_console.bat` and save the output
2. Run `test_gui_simple.bat` and note results
3. Check Windows Event Viewer for application errors
4. Note your system configuration:
   - Windows version
   - Python version
   - How you're accessing the system (local/remote/SSH)

### **Include This Information:**
- Complete error messages
- Output from diagnostic batch files
- System environment (local Windows/remote/VM/etc.)
- Steps you've already tried

### **Support Channels:**
- GitHub Issues (for bugs)
- Documentation (README.md)
- System administrator (for enterprise environments)

---

**Remember**: The Azure IoT Hub Device Simulator is a **desktop GUI application** that requires a **Windows desktop environment** to run properly. It cannot run in headless environments, SSH sessions, or command-line-only systems.


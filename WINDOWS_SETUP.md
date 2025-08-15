# Windows Setup Guide
## Azure IoT Hub Device Simulator

This guide provides step-by-step instructions for setting up the Azure IoT Hub Device Simulator on Windows systems.

## 📋 Prerequisites

### Required Software
- **Windows 10 or later** (Windows 11 recommended)
- **Python 3.11 or higher** - [Download from python.org](https://python.org/downloads/)
- **Internet connection** for downloading dependencies

### Recommended Hardware
- **CPU**: 4+ cores (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **Network**: Broadband internet connection

## 🚀 Quick Setup (Recommended)

### Step 1: Download the Application

1. Download the project files to your computer
2. Extract to a folder like `C:\azure-iot-simulator\`
3. Open the folder in File Explorer

### Step 2: Install Python (if not already installed)

1. Go to [python.org/downloads/](https://python.org/downloads/)
2. Download Python 3.11 or higher
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

### Step 3: Run Setup

1. **Right-click** on `setup.bat` in the project folder
2. Select **"Run as administrator"** (recommended)
3. Follow the on-screen instructions
4. Wait for setup to complete (may take 5-10 minutes)

### Step 4: Launch the Application

**Option A: Using Batch File**
- Double-click `launch.bat`

**Option B: Create Desktop Shortcut**
1. Double-click `create_shortcut.bat`
2. Follow prompts to create desktop and Start Menu shortcuts
3. Use the shortcuts to launch the application

## 🛠️ Available Batch Files

The project includes several Windows batch files for different purposes:

### `setup.bat` - First-Time Setup
- **Purpose**: Complete installation and setup
- **What it does**:
  - Checks Python installation and version
  - Creates virtual environment
  - Installs all required dependencies
  - Tests the installation
- **When to use**: First time setup or after major updates
- **Run as**: Administrator (recommended)

### `launch.bat` - Normal Application Launch
- **Purpose**: Start the application for regular use
- **What it does**:
  - Activates virtual environment
  - Checks dependencies
  - Launches the GUI application
- **When to use**: Every time you want to use the simulator
- **Run as**: Normal user

### `launch_debug.bat` - Debug Mode Launch
- **Purpose**: Start with detailed logging for troubleshooting
- **What it does**:
  - Enables debug logging
  - Shows detailed system information
  - Saves logs to `logs\debug.log`
- **When to use**: When experiencing issues or for development
- **Run as**: Normal user

### `create_shortcut.bat` - Create Desktop Shortcuts
- **Purpose**: Create convenient shortcuts
- **What it does**:
  - Creates desktop shortcut
  - Optionally creates Start Menu shortcut
- **When to use**: After initial setup for convenience
- **Run as**: Normal user

### `uninstall.bat` - Clean Removal
- **Purpose**: Remove virtual environment and clean up
- **What it does**:
  - Removes virtual environment
  - Deletes log files and cache
  - Optionally removes user data
- **When to use**: When uninstalling the application
- **Run as**: Normal user

## 🔧 Manual Setup (Advanced Users)

If you prefer manual setup or the batch files don't work:

### Step 1: Open Command Prompt
1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to the project folder:
   ```cmd
   cd C:\path\to\azure-iot-simulator
   ```

### Step 2: Create Virtual Environment
```cmd
python -m venv venv
```

### Step 3: Activate Virtual Environment
```cmd
venv\Scripts\activate
```

### Step 4: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 5: Launch Application
```cmd
python src\main.py
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### "Python is not recognized"
**Problem**: Python not found in PATH
**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH:
   - Open System Properties → Advanced → Environment Variables
   - Add Python installation directory to PATH

#### "Failed to create virtual environment"
**Problem**: Insufficient permissions or disk space
**Solutions**:
- Run `setup.bat` as administrator
- Check available disk space (need ~1GB)
- Disable antivirus temporarily during setup

#### "Failed to install dependencies"
**Problem**: Network issues or package conflicts
**Solutions**:
- Check internet connection
- Try running: `pip install --upgrade pip`
- Clear pip cache: `pip cache purge`
- Use different package index: `pip install -r requirements.txt -i https://pypi.org/simple/`

#### "Application won't start"
**Problem**: Missing dependencies or configuration issues
**Solutions**:
- Run `launch_debug.bat` to see detailed error messages
- Check `logs\debug.log` for error details
- Try running `setup.bat` again
- Ensure all antivirus software allows the application

#### "Qt platform plugin error"
**Problem**: Missing system libraries
**Solutions**:
- Install Visual C++ Redistributable from Microsoft
- Update Windows to latest version
- Install Windows SDK components

### Getting Help

1. **Check the logs**: Look in `logs\debug.log` for detailed error messages
2. **Run debug mode**: Use `launch_debug.bat` for verbose output
3. **System information**: The debug launcher shows system details
4. **GitHub Issues**: Report bugs at the project repository
5. **Documentation**: Check README.md for additional information

## 📁 File Locations

### Application Files
- **Main folder**: Where you extracted the project
- **Virtual environment**: `venv\` subfolder
- **Source code**: `src\` subfolder
- **Logs**: `logs\` subfolder (created automatically)

### User Data
- **Configuration**: `%USERPROFILE%\.azure_iot_simulator\`
- **Templates**: Stored in configuration database
- **Device settings**: Stored in configuration database

### Windows Integration
- **Desktop shortcut**: `%USERPROFILE%\Desktop\Azure IoT Hub Device Simulator.lnk`
- **Start Menu**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Azure IoT Hub Device Simulator.lnk`

## 🔒 Security Considerations

### Antivirus Software
- Some antivirus programs may flag Python executables
- Add the project folder to antivirus exclusions if needed
- The application is safe and doesn't modify system files

### Firewall
- The application needs internet access for Azure IoT Hub
- Windows Firewall may prompt for network access - allow it
- Corporate firewalls may block IoT Hub endpoints

### Permissions
- Normal user permissions are sufficient for operation
- Administrator rights recommended only for initial setup
- The application doesn't require elevated privileges to run

## 🚀 Next Steps

After successful installation:

1. **Configure Azure IoT Hub**:
   - Get your connection string from Azure Portal
   - Go to Tools → Settings → Azure IoT tab
   - Enter and test your connection

2. **Create your first device**:
   - Click "Add Device" in the Device Explorer
   - Choose a template (e.g., Temperature Sensor)
   - Configure device settings

3. **Start simulation**:
   - Select your device
   - Click "Start Simulation" or press F5
   - Monitor in the Dashboard tab

4. **Explore features**:
   - Try different message templates
   - Use batch operations for multiple devices
   - Export data for analysis
   - Customize settings to your needs

## 📞 Support

For additional help:
- Check the main README.md file
- Visit the project documentation
- Report issues on GitHub
- Contact support for enterprise assistance

---

**Happy Simulating! 🎉**


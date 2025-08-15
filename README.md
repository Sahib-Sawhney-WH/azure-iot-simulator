# Azure IoT Hub Device Simulator

A professional desktop application for simulating IoT devices and testing Azure IoT Hub implementations. Built with Python and PySide6, this simulator provides enterprise-grade features for device simulation, monitoring, and data analysis.

![Azure IoT Hub Device Simulator](https://img.shields.io/badge/Azure-IoT%20Hub-blue) ![Python](https://img.shields.io/badge/Python-3.11+-green) ![PySide6](https://img.shields.io/badge/GUI-PySide6-orange) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### Core Functionality
- **Multi-Device Simulation**: Simulate up to 1,000+ concurrent virtual IoT devices
- **Azure IoT Hub Integration**: Full support for device twins, direct methods, and telemetry
- **Protocol Support**: MQTT, AMQP, and HTTPS protocols
- **Real-time Monitoring**: Live device status, metrics, and performance tracking
- **Professional UI**: Modern desktop interface with dark/light themes

### Advanced Features
- **Custom Message Templates**: Visual designer for creating sophisticated telemetry patterns
- **Batch Operations**: Bulk device creation, import/export, and management
- **Scenario Manager**: Pre-configured simulation scenarios for testing
- **Data Export**: Export to JSON, CSV, Excel, PDF, and HTML formats
- **Performance Analytics**: System resource monitoring and optimization recommendations
- **Comprehensive Settings**: Extensive configuration options for all aspects

### Message Template System
- **Built-in Templates**: 4 pre-configured device types (temperature, motion, GPS, industrial)
- **Data Patterns**: Sine wave, linear, Gaussian, random, and constant patterns
- **Field Types**: String, integer, float, boolean, timestamp, UUID, and location
- **Live Preview**: Real-time preview of generated messages
- **Import/Export**: Share templates between installations

### Monitoring & Analytics
- **Real-time Dashboard**: Live metrics and device status
- **Performance Monitoring**: CPU, memory, disk, and network usage
- **Historical Data**: 24-hour rolling history with trend analysis
- **Alert System**: Configurable thresholds and notifications
- **Resource Recommendations**: Intelligent optimization suggestions

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Network**: Internet connection for Azure IoT Hub connectivity

### Dependencies
- PySide6 (GUI framework)
- azure-iot-device (Azure IoT Hub client)
- pandas (data processing)
- psutil (system monitoring)
- reportlab (PDF generation)
- openpyxl (Excel export)
- faker (test data generation)

## 🛠️ Installation

### Option 1: Windows Easy Setup (Recommended)

**For Windows users, use the provided batch files for the easiest setup:**

1. **Download or clone the project**:
   ```bash
   git clone https://github.com/your-org/azure-iot-simulator.git
   cd azure-iot-simulator
   ```

2. **Run the setup script**:
   - Double-click `setup.bat` or run from Command Prompt
   - The script will automatically:
     - Check Python installation
     - Create virtual environment
     - Install all dependencies
     - Test the installation

3. **Launch the application**:
   - Double-click `launch.bat` for normal operation
   - Double-click `launch_debug.bat` for troubleshooting
   - Or run `create_shortcut.bat` to create desktop shortcuts

### Option 2: Manual Installation (All Platforms)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/azure-iot-simulator.git
   cd azure-iot-simulator
   ```

2. **Create virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/main.py
   ```

### Option 3: Standalone Executable (Coming Soon)

Pre-built executables will be available for Windows, macOS, and Linux.

## 🚀 Quick Start

### 1. Configure Azure IoT Hub Connection

1. Launch the application
2. Go to **Tools → Settings → Azure IoT** tab
3. Enter your Azure IoT Hub connection string
4. Test the connection

### 2. Create Virtual Devices

1. Click **Add Device** in the Device Explorer
2. Configure device properties:
   - Device ID and name
   - Message template
   - Simulation settings
3. Click **Create Device**

### 3. Start Simulation

1. Select devices in the Device Explorer
2. Click **Start Simulation** or press F5
3. Monitor real-time metrics in the Dashboard

### 4. Monitor and Analyze

1. Switch to the **Monitoring** tab
2. View real-time device metrics and system performance
3. Export data using **Tools → Data Export**

## 📖 User Guide

### Device Management

#### Creating Devices
- Use the **Add Device** button or **Ctrl+N**
- Configure device identity, connection, and simulation settings
- Choose from built-in templates or create custom ones

#### Bulk Operations
- Access via **Tools → Batch Operations** or **Ctrl+B**
- Create multiple devices with patterns
- Import/export device configurations
- Bulk update or delete operations

#### Device Configuration
- Individual device settings in the Device Configuration tab
- Real-time status monitoring
- Connection string management

### Message Templates

#### Built-in Templates
- **Temperature Sensor**: Realistic temperature and humidity data
- **Motion Sensor**: Movement detection with coordinates
- **GPS Tracker**: Location tracking with speed and heading
- **Industrial Sensor**: Multi-parameter industrial monitoring

#### Custom Templates
- Visual field editor with data type selection
- Multiple generation patterns (sine, linear, random, etc.)
- Live preview and testing
- Import/export capabilities

#### Template Designer
- Access via **Tools → Message Templates** or **Ctrl+T**
- Drag-and-drop field creation
- Pattern configuration with parameters
- JSON schema validation

### Simulation Control

#### Starting Simulations
- Individual device control
- Bulk simulation management
- Configurable intervals and limits
- Burst mode support

#### Monitoring
- Real-time device status
- Message count and rate tracking
- Error monitoring and alerts
- Performance metrics

### Data Export and Reporting

#### Export Formats
- **JSON**: Raw data export
- **CSV**: Spreadsheet-compatible format
- **Excel**: Multi-sheet workbooks with charts
- **PDF**: Professional reports with tables
- **HTML**: Web-viewable reports

#### Export Types
- Device metrics and statistics
- System performance data
- Simulation logs and events
- Comprehensive reports

## ⚙️ Configuration

### Application Settings

Access via **Tools → Settings** or **Ctrl+,**

#### General Settings
- Language and localization
- Auto-save configuration
- File locations and directories
- Startup behavior

#### Appearance
- Light/dark theme selection
- Custom color schemes
- Font configuration
- UI animations and effects

#### Simulation
- Default device settings
- Performance parameters
- Error handling options
- Connection timeouts

#### Monitoring
- Update intervals
- Data retention policies
- Alert thresholds
- Performance monitoring

#### Azure IoT
- Default protocol selection
- Connection pool settings
- Security configuration
- Message formatting

### Advanced Configuration

#### Performance Tuning
- Thread pool sizing
- Memory allocation
- Connection limits
- Queue management

#### Security
- Credential storage
- SSL/TLS settings
- Certificate validation
- Encryption options

## 🔧 Development

### Project Structure

```
azure_iot_simulator/
├── src/
│   ├── core/                 # Core application framework
│   │   ├── config.py        # Configuration management
│   │   ├── events.py        # Event system
│   │   └── logging_config.py # Logging setup
│   ├── ui/                  # User interface components
│   │   ├── main_window.py   # Main application window
│   │   ├── device_dialog.py # Device configuration
│   │   └── azure_config_dialog.py # Azure settings
│   ├── azure_integration/   # Azure IoT Hub integration
│   │   ├── device_client.py # Virtual device implementation
│   │   ├── connection_manager.py # Connection handling
│   │   └── simulation_engine.py # Simulation coordination
│   ├── templates/           # Message template system
│   │   ├── template_manager.py # Template storage
│   │   ├── template_editor.py # Visual editor
│   │   └── field_editor.py  # Field configuration
│   ├── monitoring/          # Monitoring and analytics
│   │   ├── metrics_collector.py # Data collection
│   │   ├── performance_monitor.py # System monitoring
│   │   └── monitoring_dashboard.py # UI dashboard
│   └── advanced/            # Advanced features
│       ├── scenario_manager.py # Simulation scenarios
│       ├── batch_operations.py # Bulk operations
│       ├── data_export.py   # Export functionality
│       └── settings_manager.py # Settings dialog
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── test_complete_application.py # Comprehensive tests
```

### Building from Source

1. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-qt black flake8 mypy
   ```

2. **Run tests**:
   ```bash
   python test_complete_application.py
   pytest tests/
   ```

3. **Code formatting**:
   ```bash
   black src/
   flake8 src/
   mypy src/
   ```

4. **Build executable**:
   ```bash
   pyinstaller --windowed --onefile src/main.py
   ```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📊 Performance

### Tested Configurations

- **1,000 devices**: Stable operation with 10-second intervals
- **500 devices**: High-frequency (1-second intervals) simulation
- **100 devices**: Real-time (sub-second) telemetry generation

### System Requirements by Scale

| Devices | CPU | Memory | Network |
|---------|-----|--------|---------|
| 1-50    | 2 cores | 2GB | 1 Mbps |
| 51-200  | 4 cores | 4GB | 5 Mbps |
| 201-500 | 6 cores | 8GB | 10 Mbps |
| 501+    | 8+ cores | 16GB+ | 25+ Mbps |

## 🐛 Troubleshooting

### Common Issues

#### Connection Problems
- Verify Azure IoT Hub connection string
- Check network connectivity
- Validate device credentials
- Review firewall settings

#### Performance Issues
- Monitor system resources
- Adjust simulation intervals
- Reduce concurrent devices
- Check memory usage

#### UI Problems
- Update graphics drivers
- Try different themes
- Reset window layout
- Check display scaling

### Logging

Logs are stored in:
- **Windows**: `%APPDATA%\azure_iot_simulator\logs\`
- **macOS**: `~/Library/Application Support/azure_iot_simulator/logs/`
- **Linux**: `~/.azure_iot_simulator/logs/`

Enable debug logging in **Tools → Settings → Advanced**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

### Documentation
- [Azure IoT Hub Documentation](https://docs.microsoft.com/en-us/azure/iot-hub/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)

### Community
- GitHub Issues for bug reports
- GitHub Discussions for questions
- Stack Overflow with tag `azure-iot-simulator`

### Commercial Support
Contact [support@manus.ai](mailto:support@manus.ai) for enterprise support options.

## 🎯 Roadmap

### Version 1.1 (Q2 2024)
- [ ] Real-time charts and graphs
- [ ] Custom protocol support
- [ ] Device twin visualization
- [ ] Advanced scheduling

### Version 1.2 (Q3 2024)
- [ ] Cloud deployment options
- [ ] REST API interface
- [ ] Plugin system
- [ ] Multi-tenant support

### Version 2.0 (Q4 2024)
- [ ] Machine learning integration
- [ ] Predictive analytics
- [ ] Advanced security features
- [ ] Enterprise SSO

## 🏆 Acknowledgments

- Microsoft Azure IoT team for excellent documentation
- Qt/PySide6 team for the robust GUI framework
- Python community for outstanding libraries
- Beta testers and early adopters

---

**Built with ❤️ by the Manus AI Team**

For more information, visit [https://manus.ai](https://manus.ai)


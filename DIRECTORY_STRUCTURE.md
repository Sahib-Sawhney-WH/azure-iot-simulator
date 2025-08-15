# Directory Structure
## Azure IoT Hub Device Simulator

This document provides a complete overview of the project directory structure and file organization.

## 📁 Complete Project Structure

```
azure_iot_simulator/
├── 📄 README.md                           # Main documentation and user guide
├── 📄 WINDOWS_SETUP.md                    # Windows-specific setup instructions
├── 📄 DIRECTORY_STRUCTURE.md              # This file - project structure guide
├── 📄 requirements.txt                    # Python dependencies specification
│
├── 🚀 Windows Batch Files
│   ├── setup.bat                          # Complete first-time setup script
│   ├── launch.bat                         # Main application launcher
│   ├── launch_debug.bat                   # Debug mode launcher with logging
│   ├── create_shortcut.bat                # Desktop shortcut creator
│   └── uninstall.bat                      # Clean removal and cleanup tool
│
├── 🧪 Test Files
│   ├── test_complete_application.py       # Comprehensive application test
│   ├── test_app.py                        # Basic application startup test
│   ├── test_azure_integration.py          # Azure IoT Hub integration tests
│   ├── test_gui_enhanced.py               # Enhanced GUI component tests
│   ├── test_monitoring_system.py          # Monitoring system tests
│   └── test_template_system.py            # Message template system tests
│
├── 📂 src/                                # Main source code directory
│   ├── 📄 __init__.py                     # Python package marker
│   ├── 🚀 main.py                         # Application entry point
│   │
│   ├── 📂 core/                           # Core application framework
│   │   ├── 📄 __init__.py                 # Package marker
│   │   ├── ⚙️ config.py                   # Configuration management system
│   │   ├── 📡 events.py                   # Event system for inter-module communication
│   │   └── 📝 logging_config.py           # Logging configuration and setup
│   │
│   ├── 📂 ui/                             # User interface components
│   │   ├── 📄 __init__.py                 # Package marker
│   │   ├── 🖥️ main_window.py              # Main application window
│   │   ├── 🔧 device_dialog.py            # Device creation and configuration dialog
│   │   ├── 🌐 azure_config_dialog.py      # Azure IoT Hub configuration dialog
│   │   └── 🌳 device_tree_widget.py       # Enhanced device tree widget
│   │
│   ├── 📂 azure_integration/              # Azure IoT Hub integration
│   │   ├── 📄 __init__.py                 # Package marker
│   │   ├── 🔌 connection_manager.py       # Azure IoT Hub connection management
│   │   ├── 📱 device_client.py            # Virtual device implementation
│   │   ├── 📨 message_generator.py        # Telemetry message generation
│   │   └── ⚡ simulation_engine.py        # Device simulation coordination
│   │
│   ├── 📂 templates/                      # Message template system
│   │   ├── 📄 __init__.py                 # Package marker
│   │   ├── 💾 template_manager.py         # Template storage and management
│   │   ├── ✏️ template_editor.py          # Visual template editor dialog
│   │   ├── 🔍 template_browser.py         # Template browser and manager
│   │   └── 📝 field_editor.py             # Field configuration editor
│   │
│   ├── 📂 monitoring/                     # Monitoring and analytics
│   │   ├── 📄 __init__.py                 # Package marker
│   │   ├── 📊 metrics_collector.py        # Real-time metrics collection
│   │   ├── 🔍 performance_monitor.py      # System performance monitoring
│   │   └── 📈 monitoring_dashboard.py     # Monitoring dashboard widget
│   │
│   └── 📂 advanced/                       # Advanced features
│       ├── 📄 __init__.py                 # Package marker
│       ├── 🎭 scenario_manager.py         # Simulation scenario management
│       ├── 📦 batch_operations.py         # Bulk device operations
│       ├── 💾 data_export.py              # Data export functionality
│       └── ⚙️ settings_manager.py         # Comprehensive settings dialog
│
├── 📂 venv/                               # Python virtual environment (created by setup)
│   ├── 📂 Scripts/                        # Windows executables and activation scripts
│   ├── 📂 Lib/                            # Python libraries and packages
│   └── 📄 pyvenv.cfg                      # Virtual environment configuration
│
├── 📂 logs/                               # Log files (created automatically)
│   ├── 📄 app.log                         # Application log file
│   ├── 📄 debug.log                       # Debug mode log file
│   └── 📄 error.log                       # Error log file
│
└── 📂 data/                               # User data directory (created automatically)
    ├── 📄 config.db                       # SQLite configuration database
    ├── 📂 templates/                      # Custom message templates
    └── 📂 exports/                        # Exported data files
```

## 📋 File Descriptions

### 🚀 Entry Points and Launchers

| File | Purpose | Usage |
|------|---------|-------|
| `src/main.py` | Main application entry point | `python src/main.py` |
| `setup.bat` | Windows first-time setup | Double-click or run as admin |
| `launch.bat` | Windows application launcher | Double-click for normal use |
| `launch_debug.bat` | Debug mode launcher | Double-click for troubleshooting |

### 📚 Documentation

| File | Content | Audience |
|------|---------|----------|
| `README.md` | Complete user guide and documentation | All users |
| `WINDOWS_SETUP.md` | Windows-specific setup instructions | Windows users |
| `DIRECTORY_STRUCTURE.md` | This file - project organization | Developers |

### ⚙️ Core System Files

| File | Responsibility | Key Features |
|------|----------------|--------------|
| `src/core/config.py` | Configuration management | SQLite storage, app/Azure settings |
| `src/core/events.py` | Event system | Inter-module communication |
| `src/core/logging_config.py` | Logging setup | File rotation, colored output |

### 🖥️ User Interface Components

| File | Component | Description |
|------|-----------|-------------|
| `src/ui/main_window.py` | Main window | Primary application interface |
| `src/ui/device_dialog.py` | Device dialog | Device creation and configuration |
| `src/ui/azure_config_dialog.py` | Azure dialog | IoT Hub connection setup |
| `src/ui/device_tree_widget.py` | Device tree | Hierarchical device management |

### 🌐 Azure Integration

| File | Function | Capabilities |
|------|----------|--------------|
| `src/azure_integration/connection_manager.py` | Connection handling | Connection validation, management |
| `src/azure_integration/device_client.py` | Virtual devices | Device simulation, twins, methods |
| `src/azure_integration/message_generator.py` | Message creation | Template-based telemetry |
| `src/azure_integration/simulation_engine.py` | Simulation control | Multi-device coordination |

### 📋 Template System

| File | Purpose | Features |
|------|---------|----------|
| `src/templates/template_manager.py` | Template storage | CRUD operations, validation |
| `src/templates/template_editor.py` | Visual editor | Template creation and editing |
| `src/templates/template_browser.py` | Template browser | Management and selection |
| `src/templates/field_editor.py` | Field editor | Data type and pattern configuration |

### 📊 Monitoring System

| File | Function | Capabilities |
|------|----------|--------------|
| `src/monitoring/metrics_collector.py` | Data collection | Device and system metrics |
| `src/monitoring/performance_monitor.py` | Performance tracking | Resource monitoring, alerts |
| `src/monitoring/monitoring_dashboard.py` | Dashboard UI | Real-time visualization |

### 🚀 Advanced Features

| File | Feature | Description |
|------|---------|-------------|
| `src/advanced/scenario_manager.py` | Scenarios | Pre-configured simulation setups |
| `src/advanced/batch_operations.py` | Bulk operations | Multi-device management |
| `src/advanced/data_export.py` | Data export | Multiple format support |
| `src/advanced/settings_manager.py` | Settings | Comprehensive configuration |

## 📂 Directory Purposes

### `/src/` - Source Code
- **Purpose**: All Python source code
- **Organization**: Modular packages by functionality
- **Entry Point**: `main.py`

### `/venv/` - Virtual Environment
- **Purpose**: Isolated Python environment
- **Created By**: `setup.bat` or manual setup
- **Contains**: All Python dependencies

### `/logs/` - Log Files
- **Purpose**: Application logging and debugging
- **Created**: Automatically when application runs
- **Files**: Rotated log files with timestamps

### `/data/` - User Data
- **Purpose**: User configurations and templates
- **Location**: May be in user profile directory
- **Contents**: SQLite database, custom templates

## 🔧 Development Structure

### Package Organization
- **Modular Design**: Each package has specific responsibilities
- **Clear Interfaces**: Well-defined APIs between modules
- **Event-Driven**: Loose coupling via event system
- **Testable**: Comprehensive test coverage

### Code Organization Principles
1. **Separation of Concerns**: UI, business logic, and data separate
2. **Single Responsibility**: Each module has one primary purpose
3. **Dependency Injection**: Configuration and dependencies injected
4. **Error Handling**: Comprehensive error management throughout

### File Naming Conventions
- **Snake Case**: All Python files use snake_case
- **Descriptive Names**: File names clearly indicate purpose
- **Package Markers**: `__init__.py` in every package directory
- **Test Prefixes**: Test files start with `test_`

## 🚀 Getting Started

### For Users
1. **Download**: Get the complete project directory
2. **Setup**: Run `setup.bat` (Windows) or manual setup
3. **Launch**: Use `launch.bat` or `python src/main.py`

### For Developers
1. **Clone**: Get the source code repository
2. **Environment**: Create virtual environment
3. **Dependencies**: Install from `requirements.txt`
4. **Test**: Run test files to verify setup

## 📞 Support

For questions about the project structure or development:
- Check the README.md for user documentation
- Review individual file docstrings for technical details
- Run test files to understand component interactions
- Contact the development team for architecture questions

---

**Project Structure Version**: 1.0  
**Last Updated**: January 2024  
**Total Files**: 40+ Python files, 5 batch files, 3 documentation files


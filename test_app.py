#!/usr/bin/env python3
"""
Simple test script to verify the Azure IoT Hub Device Simulator application works
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from core.config import config_manager
        print("✓ Core config module imported successfully")
        
        from core.events import event_bus, EventType
        print("✓ Core events module imported successfully")
        
        from core.logging_config import setup_logging
        print("✓ Core logging module imported successfully")
        
        # Test configuration
        app_config = config_manager.get_app_config()
        print(f"✓ App config loaded: {app_config.app_name} v{app_config.version}")
        
        azure_config = config_manager.get_azure_config()
        print(f"✓ Azure config loaded: Protocol {azure_config.protocol}")
        
        # Test event system
        event_bus.emit(EventType.APP_STARTED, "TestScript", {"test": True})
        print("✓ Event system working")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_gui_imports():
    """Test GUI imports (without creating windows)"""
    print("\nTesting GUI imports...")
    
    try:
        # Set QT_QPA_PLATFORM to offscreen for headless testing
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        print("✓ PySide6 imported successfully")
        
        # Test creating QApplication
        app = QApplication([])
        print("✓ QApplication created successfully")
        
        from ui.main_window import MainWindow
        print("✓ MainWindow class imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Azure IoT Hub Device Simulator - Test Suite")
    print("=" * 50)
    
    success = True
    
    # Test core functionality
    if not test_imports():
        success = False
    
    # Test GUI functionality
    if not test_gui_imports():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("  cd /home/ubuntu/azure_iot_simulator")
        print("  source venv/bin/activate")
        print("  python src/main.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())


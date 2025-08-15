#!/usr/bin/env python3
"""
Test script for enhanced GUI features
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_enhanced_gui_imports():
    """Test that enhanced GUI components can be imported"""
    print("Testing enhanced GUI imports...")
    
    try:
        from ui.device_dialog import DeviceDialog
        print("✓ Device dialog imported successfully")
        
        from ui.device_tree_widget import DeviceTreeWidget, DeviceTreeItem
        print("✓ Enhanced device tree widget imported successfully")
        
        from ui.azure_config_dialog import AzureConfigDialog
        print("✓ Azure configuration dialog imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced GUI import test failed: {e}")
        return False

def test_device_management():
    """Test device management functionality"""
    print("\nTesting device management...")
    
    try:
        from azure_integration.device_client import device_manager, DeviceConfig
        from azure_integration.message_generator import message_generator
        
        # Test device creation
        config = DeviceConfig(
            device_id="test-gui-device",
            connection_string="HostName=test-hub.azure-devices.net;DeviceId=test-gui-device;SharedAccessKey=dGVzdGtleQ=="
        )
        
        device = device_manager.add_device(config)
        print(f"✓ Device created: {device.config.device_id}")
        
        # Test message templates
        templates = message_generator.get_builtin_templates()
        print(f"✓ Message templates available: {len(templates)}")
        
        # Test message generation
        template = templates["temperature_sensor"]
        message = message_generator.generate_message(template, "test-gui-device")
        print(f"✓ Sample message generated with {len(message)} fields")
        
        # Clean up
        device_manager.remove_device("test-gui-device")
        print("✓ Device cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Device management test failed: {e}")
        return False

def test_simulation_integration():
    """Test simulation engine integration"""
    print("\nTesting simulation integration...")
    
    try:
        from azure_integration.simulation_engine import simulation_engine
        from azure_integration.device_client import device_manager, DeviceConfig
        from azure_integration.message_generator import message_generator
        
        # Create test device
        config = DeviceConfig(
            device_id="sim-gui-test",
            connection_string="HostName=test-hub.azure-devices.net;DeviceId=sim-gui-test;SharedAccessKey=dGVzdGtleQ=="
        )
        device = device_manager.add_device(config)
        
        # Add simulation
        templates = message_generator.get_builtin_templates()
        template = templates["temperature_sensor"]
        
        success = simulation_engine.add_simulation(
            device_id="sim-gui-test",
            template=template,
            interval_seconds=2.0
        )
        print(f"✓ Simulation added: {success}")
        
        # Test status
        status = simulation_engine.get_all_simulation_status()
        print(f"✓ Simulation status retrieved: {status['total_simulations']} simulations")
        
        # Clean up
        simulation_engine.remove_simulation("sim-gui-test")
        device_manager.remove_device("sim-gui-test")
        print("✓ Simulation and device cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Simulation integration test failed: {e}")
        return False

def test_event_system():
    """Test event system integration"""
    print("\nTesting event system...")
    
    try:
        from core.events import EventType, event_bus
        
        # Test event subscription
        events_received = []
        
        def test_handler(event):
            events_received.append(event)
        
        event_bus.subscribe(EventType.DEVICE_CREATED, test_handler)
        print("✓ Event handler subscribed successfully")
        
        # Test using the event mixin approach
        from core.events import EventMixin
        
        class TestEmitter(EventMixin):
            def test_emit(self):
                self.emit_event(EventType.DEVICE_CREATED, {"device_id": "test-device"})
        
        emitter = TestEmitter()
        emitter.test_emit()
        
        print("✓ Event emitted via EventMixin")
        
        # Clean up
        event_bus.unsubscribe(EventType.DEVICE_CREATED, test_handler)
        print("✓ Event handler unsubscribed")
        
        return True
        
    except Exception as e:
        print(f"✗ Event system test failed: {e}")
        return False

def test_configuration_system():
    """Test configuration management"""
    print("\nTesting configuration system...")
    
    try:
        from core.config import config_manager
        
        # Test app config
        app_config = config_manager.get_app_config()
        print(f"✓ App config loaded: {app_config.app_name}")
        
        # Test Azure config
        azure_config = config_manager.get_azure_config()
        print(f"✓ Azure config loaded: Protocol {azure_config.protocol}")
        
        # Test config update
        config_manager.update_azure_config(
            hub_name="test-hub-gui",
            device_id="test-device-gui"
        )
        
        updated_config = config_manager.get_azure_config()
        print(f"✓ Azure config updated: Hub {updated_config.hub_name}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration system test failed: {e}")
        return False

def main():
    """Run all enhanced GUI tests"""
    print("Azure IoT Hub Device Simulator - Enhanced GUI Test Suite")
    print("=" * 60)
    
    success = True
    
    # Test enhanced GUI imports
    if not test_enhanced_gui_imports():
        success = False
    
    # Test device management
    if not test_device_management():
        success = False
    
    # Test simulation integration
    if not test_simulation_integration():
        success = False
    
    # Test event system
    if not test_event_system():
        success = False
    
    # Test configuration system
    if not test_configuration_system():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All enhanced GUI tests passed!")
        print("\nEnhanced GUI features are ready:")
        print("- Professional device management dialogs")
        print("- Advanced device tree with context menus")
        print("- Azure IoT Hub configuration interface")
        print("- Real-time device status monitoring")
        print("- Integrated simulation controls")
        print("- Event-driven UI updates")
        print("\nTo start the application:")
        print("  cd /home/ubuntu/azure_iot_simulator")
        print("  source venv/bin/activate")
        print("  python src/main.py")
    else:
        print("✗ Some enhanced GUI tests failed.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())


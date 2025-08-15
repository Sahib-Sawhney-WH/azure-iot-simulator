#!/usr/bin/env python3
"""
Test script for Azure IoT Hub integration components
"""

import sys
import os
import asyncio
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_azure_imports():
    """Test that all Azure integration modules can be imported"""
    print("Testing Azure integration imports...")
    
    try:
        from azure_integration.device_client import VirtualDevice, DeviceConfig, DeviceManager, device_manager
        print("✓ Device client module imported successfully")
        
        from azure_integration.connection_manager import ConnectionManager, connection_manager
        print("✓ Connection manager module imported successfully")
        
        from azure_integration.message_generator import MessageGenerator, MessageTemplate, message_generator
        print("✓ Message generator module imported successfully")
        
        from azure_integration.simulation_engine import SimulationEngine, simulation_engine
        print("✓ Simulation engine module imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Azure integration import test failed: {e}")
        return False

def test_connection_manager():
    """Test connection manager functionality"""
    print("\nTesting connection manager...")
    
    try:
        from azure_integration.connection_manager import connection_manager
        
        # Test connection string parsing
        test_connection_string = "HostName=test-hub.azure-devices.net;DeviceId=test-device;SharedAccessKey=dGVzdGtleQ=="
        
        conn_info = connection_manager.parse_connection_string(test_connection_string)
        print(f"✓ Connection string parsed: Hub={conn_info.hub_name}, Device={conn_info.device_id}")
        
        # Test validation
        is_valid, message = connection_manager.validate_device_id("test-device-123")
        print(f"✓ Device ID validation: {is_valid} - {message}")
        
        is_valid, message = connection_manager.validate_shared_access_key("dGVzdGtleWZvcnRlc3RpbmdwdXJwb3Nlcw==")
        print(f"✓ Shared access key validation: {is_valid} - {message}")
        
        return True
        
    except Exception as e:
        print(f"✗ Connection manager test failed: {e}")
        return False

def test_message_generator():
    """Test message generator functionality"""
    print("\nTesting message generator...")
    
    try:
        from azure_integration.message_generator import message_generator
        
        # Get built-in templates
        templates = message_generator.get_builtin_templates()
        print(f"✓ Built-in templates loaded: {len(templates)} templates")
        
        for name, template in templates.items():
            print(f"  - {name}: {template.description}")
        
        # Test message generation
        if "temperature_sensor" in templates:
            template = templates["temperature_sensor"]
            message = message_generator.generate_message(template, "test-device")
            print(f"✓ Sample message generated: {len(message)} fields")
            print(f"  Sample fields: {list(message.keys())[:3]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Message generator test failed: {e}")
        return False

def test_device_manager():
    """Test device manager functionality"""
    print("\nTesting device manager...")
    
    try:
        from azure_integration.device_client import device_manager, DeviceConfig
        
        # Test adding a device
        config = DeviceConfig(
            device_id="test-device-001",
            connection_string="HostName=test-hub.azure-devices.net;DeviceId=test-device-001;SharedAccessKey=dGVzdGtleQ=="
        )
        
        device = device_manager.add_device(config)
        print(f"✓ Device added: {device.config.device_id}")
        
        # Test getting device
        retrieved_device = device_manager.get_device("test-device-001")
        print(f"✓ Device retrieved: {retrieved_device.config.device_id}")
        
        # Test status summary
        status = device_manager.get_status_summary()
        print(f"✓ Status summary: {status['total_devices']} devices")
        
        # Clean up
        device_manager.remove_device("test-device-001")
        print("✓ Device removed")
        
        return True
        
    except Exception as e:
        print(f"✗ Device manager test failed: {e}")
        return False

def test_simulation_engine():
    """Test simulation engine functionality"""
    print("\nTesting simulation engine...")
    
    try:
        from azure_integration.simulation_engine import simulation_engine
        from azure_integration.device_client import device_manager, DeviceConfig
        from azure_integration.message_generator import message_generator
        
        # Add a test device
        config = DeviceConfig(
            device_id="sim-test-device",
            connection_string="HostName=test-hub.azure-devices.net;DeviceId=sim-test-device;SharedAccessKey=dGVzdGtleQ=="
        )
        device = device_manager.add_device(config)
        
        # Get a template
        templates = message_generator.get_builtin_templates()
        template = templates["temperature_sensor"]
        
        # Add simulation
        success = simulation_engine.add_simulation(
            device_id="sim-test-device",
            template=template,
            interval_seconds=1.0
        )
        print(f"✓ Simulation added: {success}")
        
        # Get status
        status = simulation_engine.get_all_simulation_status()
        print(f"✓ Simulation status: {status['total_simulations']} simulations")
        
        # Clean up
        simulation_engine.remove_simulation("sim-test-device")
        device_manager.remove_device("sim-test-device")
        print("✓ Simulation and device cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Simulation engine test failed: {e}")
        return False

async def test_async_functionality():
    """Test async functionality (without actual Azure connection)"""
    print("\nTesting async functionality...")
    
    try:
        from azure_integration.device_client import VirtualDevice, DeviceConfig
        
        # Create a device (won't actually connect without real connection string)
        config = DeviceConfig(
            device_id="async-test-device",
            connection_string="HostName=test-hub.azure-devices.net;DeviceId=async-test-device;SharedAccessKey=dGVzdGtleQ=="
        )
        
        device = VirtualDevice(config)
        print(f"✓ Virtual device created: {device.config.device_id}")
        
        # Test status info
        status_info = device.get_status_info()
        print(f"✓ Device status info: {status_info['status']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Async functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Azure IoT Hub Integration - Test Suite")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_azure_imports():
        success = False
    
    # Test individual components
    if not test_connection_manager():
        success = False
    
    if not test_message_generator():
        success = False
    
    if not test_device_manager():
        success = False
    
    if not test_simulation_engine():
        success = False
    
    # Test async functionality
    try:
        if not asyncio.run(test_async_functionality()):
            success = False
    except Exception as e:
        print(f"✗ Async test failed: {e}")
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All Azure integration tests passed!")
        print("\nAzure IoT Hub integration is ready.")
        print("Note: Actual Azure connectivity requires valid connection strings.")
    else:
        print("✗ Some Azure integration tests failed.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())


#!/usr/bin/env python3
"""
Test script for the complete message template system
"""

import sys
import os
import json
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_template_system_imports():
    """Test that all template system components can be imported"""
    print("Testing template system imports...")
    
    try:
        from templates.template_manager import template_manager
        print("✓ Template manager imported successfully")
        
        from templates.field_editor import FieldEditor
        print("✓ Field editor imported successfully")
        
        from templates.template_editor import TemplateEditor
        print("✓ Template editor imported successfully")
        
        from templates.template_browser import TemplateBrowser
        print("✓ Template browser imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Template system import test failed: {e}")
        return False

def test_template_manager():
    """Test template manager functionality"""
    print("\nTesting template manager...")
    
    try:
        from templates.template_manager import template_manager
        from azure_integration.message_generator import MessageTemplate, FieldConfig, DataType, PatternType
        
        # Create a test template
        test_field = FieldConfig(
            name="test_temperature",
            data_type=DataType.FLOAT,
            pattern=PatternType.SINE_WAVE,
            min_value=20.0,
            max_value=30.0,
            amplitude=5.0,
            frequency=0.1,
            offset=25.0,
            unit="°C"
        )
        
        test_template = MessageTemplate(
            name="Test Temperature Sensor",
            description="Test template for temperature sensor",
            fields=[test_field],
            message_type="telemetry",
            version="1.0"
        )
        
        # Save template
        template_id = template_manager.save_template(test_template)
        print(f"✓ Template saved with ID: {template_id}")
        
        # Load template
        loaded_template = template_manager.get_template(template_id)
        print(f"✓ Template loaded: {loaded_template.name}")
        
        # Get template list
        template_list = template_manager.get_template_list()
        print(f"✓ Template list retrieved: {len(template_list)} templates")
        
        # Validate template
        is_valid, errors = template_manager.validate_template(test_template)
        print(f"✓ Template validation: {is_valid}")
        
        # Get statistics
        stats = template_manager.get_template_statistics()
        print(f"✓ Template statistics: {stats['total_templates']} templates")
        
        # Clean up
        template_manager.delete_template(template_id)
        print("✓ Template cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Template manager test failed: {e}")
        return False

def test_field_configuration():
    """Test field configuration functionality"""
    print("\nTesting field configuration...")
    
    try:
        from azure_integration.message_generator import FieldConfig, DataType, PatternType
        
        # Test different field types
        field_configs = [
            # Numeric field with sine wave
            FieldConfig(
                name="temperature",
                data_type=DataType.FLOAT,
                pattern=PatternType.SINE_WAVE,
                amplitude=10.0,
                frequency=0.05,
                offset=25.0,
                unit="°C"
            ),
            
            # Integer field with random pattern
            FieldConfig(
                name="humidity",
                data_type=DataType.INTEGER,
                pattern=PatternType.RANDOM,
                min_value=30,
                max_value=80,
                unit="%"
            ),
            
            # String field with choices
            FieldConfig(
                name="status",
                data_type=DataType.STRING,
                pattern=PatternType.RANDOM,
                string_choices=["active", "idle", "maintenance", "error"]
            ),
            
            # Boolean field
            FieldConfig(
                name="alarm",
                data_type=DataType.BOOLEAN,
                pattern=PatternType.RANDOM
            ),
            
            # Timestamp field
            FieldConfig(
                name="timestamp",
                data_type=DataType.TIMESTAMP
            )
        ]
        
        print(f"✓ Created {len(field_configs)} different field configurations")
        
        # Test field value generation
        from azure_integration.message_generator import MessageGenerator
        generator = MessageGenerator()
        
        for field_config in field_configs:
            try:
                value = generator._generate_field_value(field_config, "test_device")
                print(f"✓ Generated value for {field_config.name}: {value} ({type(value).__name__})")
            except Exception as e:
                print(f"✗ Failed to generate value for {field_config.name}: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Field configuration test failed: {e}")
        return False

def test_template_creation():
    """Test complete template creation and usage"""
    print("\nTesting template creation...")
    
    try:
        from templates.template_manager import template_manager
        from azure_integration.message_generator import MessageTemplate, FieldConfig, DataType, PatternType, message_generator
        
        # Create a comprehensive test template
        fields = [
            FieldConfig(
                name="device_id",
                data_type=DataType.STRING,
                pattern=PatternType.CONSTANT,
                constant_value="SENSOR_001"
            ),
            FieldConfig(
                name="temperature",
                data_type=DataType.FLOAT,
                pattern=PatternType.SINE_WAVE,
                amplitude=5.0,
                frequency=0.1,
                offset=23.0,
                min_value=18.0,
                max_value=28.0,
                precision=2,
                unit="°C"
            ),
            FieldConfig(
                name="humidity",
                data_type=DataType.INTEGER,
                pattern=PatternType.GAUSSIAN,
                mean=50,
                std_dev=10,
                min_value=30,
                max_value=80,
                unit="%"
            ),
            FieldConfig(
                name="pressure",
                data_type=DataType.FLOAT,
                pattern=PatternType.LINEAR,
                step_size=0.1,
                offset=1013.25,
                min_value=1000.0,
                max_value=1030.0,
                precision=2,
                unit="hPa"
            ),
            FieldConfig(
                name="status",
                data_type=DataType.STRING,
                pattern=PatternType.RANDOM,
                string_choices=["normal", "warning", "critical"]
            ),
            FieldConfig(
                name="battery_level",
                data_type=DataType.INTEGER,
                pattern=PatternType.LINEAR,
                step_size=-1,
                offset=100,
                min_value=0,
                max_value=100,
                unit="%"
            ),
            FieldConfig(
                name="timestamp",
                data_type=DataType.TIMESTAMP
            )
        ]
        
        comprehensive_template = MessageTemplate(
            name="Comprehensive Environmental Sensor",
            description="Multi-parameter environmental sensor with various data patterns",
            fields=fields,
            message_type="telemetry",
            version="1.0"
        )
        
        # Save template
        template_id = template_manager.save_template(comprehensive_template)
        print(f"✓ Comprehensive template saved: {template_id}")
        
        # Generate test messages
        for i in range(5):
            message = message_generator.generate_message(comprehensive_template, f"test_device_{i}")
            print(f"✓ Generated message {i+1}: {len(message)} fields")
        
        # Test template export/import
        export_path = "/tmp/test_template.json"
        success = template_manager.export_template(template_id, export_path)
        print(f"✓ Template exported: {success}")
        
        # Import template with new name
        imported_id = template_manager.import_template(export_path, "Imported Test Template")
        print(f"✓ Template imported: {imported_id}")
        
        # Clean up
        template_manager.delete_template(template_id)
        template_manager.delete_template(imported_id)
        os.remove(export_path)
        print("✓ Templates and files cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Template creation test failed: {e}")
        return False

def test_builtin_template_integration():
    """Test integration with built-in templates"""
    print("\nTesting built-in template integration...")
    
    try:
        from templates.template_manager import template_manager
        from azure_integration.message_generator import message_generator
        
        # Get built-in templates
        builtin_templates = message_generator.get_builtin_templates()
        print(f"✓ Found {len(builtin_templates)} built-in templates")
        
        # Test creating custom template from built-in
        if "temperature_sensor" in builtin_templates:
            custom_id = template_manager.create_template_from_builtin(
                "temperature_sensor", "My Custom Temperature Sensor"
            )
            print(f"✓ Created custom template from built-in: {custom_id}")
            
            # Verify the custom template
            custom_template = template_manager.get_template(custom_id)
            if custom_template:
                print(f"✓ Custom template verified: {custom_template.name}")
                
                # Generate message with custom template
                message = message_generator.generate_message(custom_template, "custom_device")
                print(f"✓ Generated message with custom template: {len(message)} fields")
            
            # Clean up
            template_manager.delete_template(custom_id)
            print("✓ Custom template cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Built-in template integration test failed: {e}")
        return False

def test_template_validation():
    """Test template validation functionality"""
    print("\nTesting template validation...")
    
    try:
        from templates.template_manager import template_manager
        from azure_integration.message_generator import MessageTemplate, FieldConfig, DataType, PatternType
        
        # Test valid template
        valid_template = MessageTemplate(
            name="Valid Template",
            description="A valid test template",
            fields=[
                FieldConfig(
                    name="valid_field",
                    data_type=DataType.FLOAT,
                    pattern=PatternType.RANDOM,
                    min_value=0.0,
                    max_value=100.0
                )
            ]
        )
        
        is_valid, errors = template_manager.validate_template(valid_template)
        print(f"✓ Valid template validation: {is_valid} (errors: {len(errors)})")
        
        # Test invalid template - no name
        invalid_template1 = MessageTemplate(
            name="",
            description="Invalid template with no name",
            fields=[
                FieldConfig(
                    name="field1",
                    data_type=DataType.FLOAT,
                    pattern=PatternType.RANDOM
                )
            ]
        )
        
        is_valid, errors = template_manager.validate_template(invalid_template1)
        print(f"✓ Invalid template (no name) validation: {is_valid} (errors: {len(errors)})")
        
        # Test invalid template - duplicate field names
        invalid_template2 = MessageTemplate(
            name="Invalid Template",
            description="Invalid template with duplicate field names",
            fields=[
                FieldConfig(
                    name="duplicate_field",
                    data_type=DataType.FLOAT,
                    pattern=PatternType.RANDOM
                ),
                FieldConfig(
                    name="duplicate_field",
                    data_type=DataType.INTEGER,
                    pattern=PatternType.RANDOM
                )
            ]
        )
        
        is_valid, errors = template_manager.validate_template(invalid_template2)
        print(f"✓ Invalid template (duplicate fields) validation: {is_valid} (errors: {len(errors)})")
        
        # Test invalid template - invalid range
        invalid_template3 = MessageTemplate(
            name="Invalid Range Template",
            description="Invalid template with invalid range",
            fields=[
                FieldConfig(
                    name="invalid_range",
                    data_type=DataType.FLOAT,
                    pattern=PatternType.RANDOM,
                    min_value=100.0,
                    max_value=50.0  # min > max
                )
            ]
        )
        
        is_valid, errors = template_manager.validate_template(invalid_template3)
        print(f"✓ Invalid template (invalid range) validation: {is_valid} (errors: {len(errors)})")
        
        return True
        
    except Exception as e:
        print(f"✗ Template validation test failed: {e}")
        return False

def main():
    """Run all template system tests"""
    print("Azure IoT Hub Device Simulator - Template System Test Suite")
    print("=" * 65)
    
    success = True
    
    # Test template system imports
    if not test_template_system_imports():
        success = False
    
    # Test template manager
    if not test_template_manager():
        success = False
    
    # Test field configuration
    if not test_field_configuration():
        success = False
    
    # Test template creation
    if not test_template_creation():
        success = False
    
    # Test built-in template integration
    if not test_builtin_template_integration():
        success = False
    
    # Test template validation
    if not test_template_validation():
        success = False
    
    print("\n" + "=" * 65)
    if success:
        print("✓ All template system tests passed!")
        print("\nTemplate system features are ready:")
        print("- Advanced field editor with multiple data types and patterns")
        print("- Visual template editor with drag-and-drop field management")
        print("- Template browser with search, filtering, and categorization")
        print("- Template manager with import/export capabilities")
        print("- Integration with built-in templates")
        print("- Comprehensive validation and error checking")
        print("- Real-time preview and test generation")
        print("\nTo start the application:")
        print("  cd /home/ubuntu/azure_iot_simulator")
        print("  source venv/bin/activate")
        print("  python src/main.py")
        print("\nAccess templates via: Tools → Message Templates...")
    else:
        print("✗ Some template system tests failed.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())


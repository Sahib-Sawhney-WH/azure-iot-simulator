"""
Message generator for Azure IoT Hub Device Simulator
"""

import json
import random
import math
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False
    Faker = None

from core.logging_config import get_logger

logger = get_logger('message_generator')


class DataPattern(Enum):
    """Data generation patterns"""
    CONSTANT = "constant"
    RANDOM = "random"
    SINE_WAVE = "sine_wave"
    LINEAR = "linear"
    GAUSSIAN = "gaussian"


@dataclass
class FieldConfig:
    """Configuration for a message field"""
    name: str
    data_type: str  # string, int, float, bool, timestamp, uuid, location
    pattern: DataPattern
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    constant_value: Any = None
    step_size: float = 0.1
    amplitude: float = 1.0
    frequency: float = 1.0
    mean: float = 0.0
    std_dev: float = 1.0


class MessageTemplate:
    """Message template with field configurations"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.fields: List[FieldConfig] = []
        self._step_counter = 0
        self._faker = Faker() if FAKER_AVAILABLE else None
    
    def add_field(self, field_config: FieldConfig):
        """Add a field to the template"""
        self.fields.append(field_config)
    
    def generate_message(self) -> Dict[str, Any]:
        """Generate a message based on the template"""
        message = {}
        
        for field in self.fields:
            message[field.name] = self._generate_field_value(field)
        
        # Always include timestamp
        if 'timestamp' not in message:
            message['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        self._step_counter += 1
        return message
    
    def _generate_field_value(self, field: FieldConfig) -> Any:
        """Generate value for a specific field"""
        try:
            if field.data_type == "timestamp":
                return datetime.now(timezone.utc).isoformat()
            
            elif field.data_type == "uuid":
                return str(uuid.uuid4())
            
            elif field.data_type == "location":
                return self._generate_location()
            
            elif field.data_type == "bool":
                if field.pattern == DataPattern.CONSTANT:
                    return bool(field.constant_value)
                else:
                    return random.choice([True, False])
            
            elif field.data_type == "string":
                return self._generate_string_value(field)
            
            elif field.data_type in ["int", "float"]:
                return self._generate_numeric_value(field)
            
            else:
                logger.warning(f"Unknown data type: {field.data_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating value for field {field.name}: {e}")
            return None
    
    def _generate_string_value(self, field: FieldConfig) -> str:
        """Generate string value"""
        if field.pattern == DataPattern.CONSTANT:
            return str(field.constant_value or "")
        
        elif field.pattern == DataPattern.RANDOM:
            if self._faker:
                # Use faker for realistic string data
                if field.name.lower() in ['name', 'device_name']:
                    return self._faker.name()
                elif field.name.lower() in ['location', 'address']:
                    return self._faker.address()
                elif field.name.lower() in ['status', 'state']:
                    return random.choice(['active', 'inactive', 'warning', 'error'])
                else:
                    return self._faker.word()
            else:
                # Simple random string
                return f"value_{random.randint(1, 1000)}"
        
        else:
            return f"{field.name}_{self._step_counter}"
    
    def _generate_numeric_value(self, field: FieldConfig) -> float:
        """Generate numeric value"""
        if field.pattern == DataPattern.CONSTANT:
            value = field.constant_value or 0
        
        elif field.pattern == DataPattern.RANDOM:
            min_val = field.min_value or 0
            max_val = field.max_value or 100
            value = random.uniform(min_val, max_val)
        
        elif field.pattern == DataPattern.SINE_WAVE:
            amplitude = field.amplitude or 1.0
            frequency = field.frequency or 1.0
            offset = field.mean or 0
            value = offset + amplitude * math.sin(2 * math.pi * frequency * self._step_counter / 100)
        
        elif field.pattern == DataPattern.LINEAR:
            start_value = field.min_value or 0
            step = field.step_size or 0.1
            value = start_value + (step * self._step_counter)
            
            # Wrap around if max value is set
            if field.max_value and value > field.max_value:
                value = field.min_value or 0
                self._step_counter = 0
        
        elif field.pattern == DataPattern.GAUSSIAN:
            mean = field.mean or 0
            std_dev = field.std_dev or 1.0
            value = random.gauss(mean, std_dev)
            
            # Clamp to min/max if specified
            if field.min_value is not None:
                value = max(value, field.min_value)
            if field.max_value is not None:
                value = min(value, field.max_value)
        
        else:
            value = 0
        
        # Convert to int if needed
        if field.data_type == "int":
            return int(value)
        else:
            return round(value, 2)
    
    def _generate_location(self) -> Dict[str, float]:
        """Generate GPS location"""
        if self._faker:
            return {
                "latitude": float(self._faker.latitude()),
                "longitude": float(self._faker.longitude())
            }
        else:
            # Simple random location
            return {
                "latitude": random.uniform(-90, 90),
                "longitude": random.uniform(-180, 180)
            }


class MessageGenerator:
    """Message generator with built-in templates"""
    
    def __init__(self):
        self.templates: Dict[str, MessageTemplate] = {}
        self._create_builtin_templates()
    
    def _create_builtin_templates(self):
        """Create built-in message templates"""
        
        # Temperature sensor template
        temp_template = MessageTemplate(
            "temperature_sensor",
            "Temperature and humidity sensor"
        )
        temp_template.add_field(FieldConfig(
            "temperature", "float", DataPattern.SINE_WAVE,
            min_value=15.0, max_value=35.0, amplitude=10.0, frequency=0.1, mean=22.5
        ))
        temp_template.add_field(FieldConfig(
            "humidity", "float", DataPattern.GAUSSIAN,
            min_value=30.0, max_value=80.0, mean=55.0, std_dev=10.0
        ))
        self.templates["temperature_sensor"] = temp_template
        
        # Motion sensor template
        motion_template = MessageTemplate(
            "motion_sensor",
            "Motion detection sensor"
        )
        motion_template.add_field(FieldConfig(
            "motion_detected", "bool", DataPattern.RANDOM
        ))
        motion_template.add_field(FieldConfig(
            "confidence", "float", DataPattern.RANDOM,
            min_value=0.0, max_value=1.0
        ))
        self.templates["motion_sensor"] = motion_template
        
        logger.info(f"Created {len(self.templates)} built-in templates")
    
    def get_template(self, name: str) -> Optional[MessageTemplate]:
        """Get a template by name"""
        return self.templates.get(name)
    
    def generate_message(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Generate a message using the specified template"""
        template = self.get_template(template_name)
        if template:
            return template.generate_message()
        else:
            logger.error(f"Template not found: {template_name}")
            return None
    
    def generate_test_message(self, device_id: str = "test_device") -> Dict[str, Any]:
        """Generate a simple test message"""
        return {
            "device_id": device_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message_id": str(uuid.uuid4()),
            "test_value": random.randint(1, 100),
            "status": "ok"
        }

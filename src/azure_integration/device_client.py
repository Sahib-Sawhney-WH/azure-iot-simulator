"""
Azure IoT Hub device client wrapper
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict

try:
    from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
    from azure.iot.device.exceptions import ConnectionFailedError
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    IoTHubDeviceClient = None
    Message = None
    MethodResponse = None
    ConnectionFailedError = Exception

from core.logging_config import get_logger
from core.events import EventMixin, EventType

logger = get_logger('device_client')


@dataclass
class DeviceConfig:
    """Device configuration"""
    device_id: str
    connection_string: str
    protocol: str = "MQTT"
    auto_reconnect: bool = True
    message_interval: int = 10  # seconds
    template_name: str = "temperature_sensor"


class VirtualDevice(EventMixin):
    """Virtual IoT device"""
    
    def __init__(self, config: DeviceConfig):
        super().__init__()
        self.config = config
        self.client: Optional[IoTHubDeviceClient] = None
        self.is_connected = False
        self.is_simulating = False
        self.message_count = 0
        self.error_count = 0
        self.last_message_time: Optional[datetime] = None
        
        # Device twin properties
        self.reported_properties = {}
        self.desired_properties = {}
        
        # Message handlers
        self.message_handler: Optional[Callable] = None
        self.method_handler: Optional[Callable] = None
        self.twin_handler: Optional[Callable] = None
        
        if not AZURE_AVAILABLE:
            logger.warning(f"Azure IoT SDK not available for device {config.device_id}")
    
    async def connect(self) -> bool:
        """Connect the device to Azure IoT Hub"""
        if not AZURE_AVAILABLE:
            logger.error(f"Cannot connect device {self.config.device_id} - Azure SDK not available")
            return False
        
        try:
            if self.is_connected:
                return True
            
            # Create client
            self.client = IoTHubDeviceClient.create_from_connection_string(
                self.config.connection_string
            )
            
            # Set up handlers
            self._setup_handlers()
            
            # Connect
            await self.client.connect()
            self.is_connected = True
            
            # Emit connection event
            self.emit_event(EventType.DEVICE_CONNECTED, {
                "device_id": self.config.device_id
            })
            
            logger.info(f"Device {self.config.device_id} connected")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect device {self.config.device_id}: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """Disconnect the device"""
        try:
            if self.client and self.is_connected:
                await self.client.disconnect()
                
                # Emit disconnection event
                self.emit_event(EventType.DEVICE_DISCONNECTED, {
                    "device_id": self.config.device_id
                })
                
                logger.info(f"Device {self.config.device_id} disconnected")
            
            self.client = None
            self.is_connected = False
            self.is_simulating = False
            
        except Exception as e:
            logger.error(f"Error disconnecting device {self.config.device_id}: {e}")
    
    def _setup_handlers(self):
        """Setup message and method handlers"""
        if not self.client:
            return
        
        # Cloud-to-device message handler
        self.client.on_message_received = self._handle_message
        
        # Direct method handler
        self.client.on_method_request_received = self._handle_method_request
        
        # Device twin handler
        self.client.on_twin_desired_properties_patch_received = self._handle_twin_patch
    
    async def _handle_message(self, message):
        """Handle cloud-to-device messages"""
        try:
            message_data = {
                "device_id": self.config.device_id,
                "message_id": getattr(message, 'message_id', str(uuid.uuid4())),
                "data": message.data.decode('utf-8') if hasattr(message, 'data') else str(message),
                "properties": dict(getattr(message, 'custom_properties', {})),
                "timestamp": datetime.now()
            }
            
            self.emit_event(EventType.MESSAGE_RECEIVED, message_data)
            
            if self.message_handler:
                await self.message_handler(message_data)
            
            logger.info(f"Device {self.config.device_id} received message")
            
        except Exception as e:
            logger.error(f"Error handling message for device {self.config.device_id}: {e}")
    
    async def _handle_method_request(self, method_request):
        """Handle direct method requests"""
        try:
            method_data = {
                "device_id": self.config.device_id,
                "method_name": getattr(method_request, 'name', 'unknown'),
                "payload": getattr(method_request, 'payload', {}),
                "request_id": getattr(method_request, 'request_id', str(uuid.uuid4())),
                "timestamp": datetime.now()
            }
            
            # Default response
            response_payload = {"result": "success", "message": "Method executed"}
            response_status = 200
            
            if self.method_handler:
                result = await self.method_handler(method_data)
                if isinstance(result, dict):
                    response_payload = result.get("payload", response_payload)
                    response_status = result.get("status", response_status)
            
            # Send method response
            if AZURE_AVAILABLE and MethodResponse:
                method_response = MethodResponse.create_from_method_request(
                    method_request, response_status, response_payload
                )
                await self.client.send_method_response(method_response)
            
            logger.info(f"Device {self.config.device_id} handled method: {method_data['method_name']}")
            
        except Exception as e:
            logger.error(f"Error handling method for device {self.config.device_id}: {e}")
    
    async def _handle_twin_patch(self, patch):
        """Handle device twin desired properties patch"""
        try:
            self.desired_properties.update(patch)
            
            twin_data = {
                "device_id": self.config.device_id,
                "desired_properties": patch,
                "timestamp": datetime.now()
            }
            
            if self.twin_handler:
                await self.twin_handler(twin_data)
            
            logger.info(f"Device {self.config.device_id} received twin patch")
            
        except Exception as e:
            logger.error(f"Error handling twin patch for device {self.config.device_id}: {e}")
    
    async def send_message(self, message_data: Dict[str, Any]) -> bool:
        """Send a telemetry message"""
        try:
            if not AZURE_AVAILABLE:
                logger.warning(f"Cannot send message from device {self.config.device_id} - Azure SDK not available")
                # Simulate successful send for testing
                self.message_count += 1
                self.last_message_time = datetime.now()
                self.emit_event(EventType.MESSAGE_SENT, {
                    "device_id": self.config.device_id,
                    "message_id": str(uuid.uuid4()),
                    "data": message_data,
                    "timestamp": self.last_message_time
                })
                return True
            
            if not self.client or not self.is_connected:
                logger.warning(f"Device {self.config.device_id} not connected")
                return False
            
            # Create message
            message_json = json.dumps(message_data)
            message = Message(message_json)
            
            # Add message properties
            message.message_id = str(uuid.uuid4())
            message.correlation_id = str(uuid.uuid4())
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            
            # Add custom properties
            message.custom_properties["deviceId"] = self.config.device_id
            message.custom_properties["timestamp"] = datetime.now().isoformat()
            
            # Send message
            await self.client.send_message(message)
            
            self.message_count += 1
            self.last_message_time = datetime.now()
            
            # Emit message sent event
            self.emit_event(EventType.MESSAGE_SENT, {
                "device_id": self.config.device_id,
                "message_id": message.message_id,
                "data": message_data,
                "timestamp": self.last_message_time
            })
            
            logger.debug(f"Device {self.config.device_id} sent message: {message.message_id}")
            return True
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Failed to send message from device {self.config.device_id}: {e}")
            
            # Emit message failed event
            self.emit_event(EventType.MESSAGE_FAILED, {
                "device_id": self.config.device_id,
                "error": str(e),
                "timestamp": datetime.now()
            })
            
            return False
    
    async def update_reported_properties(self, properties: Dict[str, Any]) -> bool:
        """Update device twin reported properties"""
        try:
            if not AZURE_AVAILABLE or not self.client or not self.is_connected:
                # Update local copy only
                self.reported_properties.update(properties)
                return True
            
            # Update local copy
            self.reported_properties.update(properties)
            
            # Send to IoT Hub
            await self.client.patch_twin_reported_properties(properties)
            
            logger.info(f"Device {self.config.device_id} updated reported properties")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update reported properties for device {self.config.device_id}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get device status"""
        return {
            "device_id": self.config.device_id,
            "connected": self.is_connected,
            "simulating": self.is_simulating,
            "message_count": self.message_count,
            "error_count": self.error_count,
            "last_message_time": self.last_message_time.isoformat() if self.last_message_time else None,
            "reported_properties": self.reported_properties,
            "desired_properties": self.desired_properties,
            "azure_available": AZURE_AVAILABLE
        }
    
    def set_message_handler(self, handler: Callable):
        """Set cloud-to-device message handler"""
        self.message_handler = handler
    
    def set_method_handler(self, handler: Callable):
        """Set direct method handler"""
        self.method_handler = handler
    
    def set_twin_handler(self, handler: Callable):
        """Set device twin handler"""
        self.twin_handler = handler


class DeviceManager(EventMixin):
    """Manages multiple virtual devices"""
    
    def __init__(self):
        super().__init__()
        self.devices: Dict[str, VirtualDevice] = {}
    
    def add_device(self, config: DeviceConfig) -> VirtualDevice:
        """Add a new virtual device"""
        device = VirtualDevice(config)
        self.devices[config.device_id] = device
        
        self.emit_event(EventType.DEVICE_ADDED, {
            "device_id": config.device_id
        })
        
        logger.info(f"Added device: {config.device_id}")
        return device
    
    def remove_device(self, device_id: str) -> bool:
        """Remove a virtual device"""
        if device_id in self.devices:
            device = self.devices[device_id]
            
            # Disconnect if connected
            if device.is_connected:
                asyncio.create_task(device.disconnect())
            
            del self.devices[device_id]
            
            self.emit_event(EventType.DEVICE_REMOVED, {
                "device_id": device_id
            })
            
            logger.info(f"Removed device: {device_id}")
            return True
        
        return False
    
    def get_device(self, device_id: str) -> Optional[VirtualDevice]:
        """Get a virtual device by ID"""
        return self.devices.get(device_id)
    
    def get_all_devices(self) -> Dict[str, VirtualDevice]:
        """Get all virtual devices"""
        return self.devices.copy()
    
    async def connect_all(self) -> Dict[str, bool]:
        """Connect all devices"""
        results = {}
        for device_id, device in self.devices.items():
            results[device_id] = await device.connect()
        return results
    
    async def disconnect_all(self):
        """Disconnect all devices"""
        for device in self.devices.values():
            await device.disconnect()
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get status summary for all devices"""
        total_devices = len(self.devices)
        connected_devices = sum(1 for d in self.devices.values() if d.is_connected)
        simulating_devices = sum(1 for d in self.devices.values() if d.is_simulating)
        total_messages = sum(d.message_count for d in self.devices.values())
        total_errors = sum(d.error_count for d in self.devices.values())
        
        return {
            "total_devices": total_devices,
            "connected_devices": connected_devices,
            "simulating_devices": simulating_devices,
            "total_messages": total_messages,
            "total_errors": total_errors,
            "azure_available": AZURE_AVAILABLE
        }


"""
Azure IoT Hub connection manager
"""

import asyncio
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass

try:
    from azure.iot.device import IoTHubDeviceClient
    from azure.iot.device.exceptions import ConnectionFailedError, CredentialError
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    IoTHubDeviceClient = None
    ConnectionFailedError = Exception
    CredentialError = Exception

from core.logging_config import get_logger
from core.events import EventMixin, EventType

logger = get_logger('connection_manager')


@dataclass
class ConnectionInfo:
    """Connection information"""
    hub_name: str
    device_id: str
    shared_access_key: str
    connection_string: str
    protocol: str = "MQTT"


class ConnectionManager(EventMixin):
    """Manages Azure IoT Hub connections"""
    
    def __init__(self):
        super().__init__()
        self.connection_info: Optional[ConnectionInfo] = None
        self.client: Optional[IoTHubDeviceClient] = None
        self.is_connected = False
        
        if not AZURE_AVAILABLE:
            logger.warning("Azure IoT SDK not available - connection features disabled")
    
    def parse_connection_string(self, connection_string: str) -> Optional[ConnectionInfo]:
        """Parse Azure IoT Hub connection string"""
        try:
            # Parse connection string components
            parts = {}
            for part in connection_string.split(';'):
                if '=' in part:
                    key, value = part.split('=', 1)
                    parts[key] = value
            
            # Extract required components
            hostname = parts.get('HostName', '')
            device_id = parts.get('DeviceId', '')
            shared_access_key = parts.get('SharedAccessKey', '')
            
            if not all([hostname, device_id, shared_access_key]):
                logger.error("Invalid connection string: missing required components")
                return None
            
            # Extract hub name from hostname
            hub_name = hostname.split('.')[0] if '.' in hostname else hostname
            
            connection_info = ConnectionInfo(
                hub_name=hub_name,
                device_id=device_id,
                shared_access_key=shared_access_key,
                connection_string=connection_string
            )
            
            logger.info(f"Parsed connection string for device: {device_id}")
            return connection_info
            
        except Exception as e:
            logger.error(f"Failed to parse connection string: {e}")
            return None
    
    def validate_device_id(self, device_id: str) -> bool:
        """Validate device ID format"""
        if not device_id:
            return False
        
        if len(device_id) > 128:
            return False
        
        # Must contain only alphanumeric characters, hyphens, and underscores
        pattern = r'^[a-zA-Z0-9\-_]+$'
        return bool(re.match(pattern, device_id))
    
    def validate_shared_access_key(self, key: str) -> bool:
        """Validate shared access key format"""
        if not key:
            return False
        
        # Basic validation - should be base64 encoded
        try:
            import base64
            base64.b64decode(key)
            return True
        except Exception:
            return False
    
    async def test_connection(self, connection_string: str) -> Dict[str, Any]:
        """Test Azure IoT Hub connection"""
        result = {
            "success": False,
            "error": None,
            "connection_info": None
        }
        
        if not AZURE_AVAILABLE:
            result["error"] = "Azure IoT SDK not installed"
            return result
        
        try:
            # Parse connection string
            connection_info = self.parse_connection_string(connection_string)
            if not connection_info:
                result["error"] = "Invalid connection string format"
                return result
            
            # Validate components
            if not self.validate_device_id(connection_info.device_id):
                result["error"] = "Invalid device ID format"
                return result
            
            if not self.validate_shared_access_key(connection_info.shared_access_key):
                result["error"] = "Invalid shared access key format"
                return result
            
            # Test connection
            test_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
            
            # Try to connect
            await test_client.connect()
            
            # If we get here, connection was successful
            result["success"] = True
            result["connection_info"] = connection_info
            
            # Disconnect test client
            await test_client.disconnect()
            
            logger.info(f"Connection test successful for device: {connection_info.device_id}")
            
        except ConnectionFailedError as e:
            result["error"] = f"Connection failed: {str(e)}"
            logger.error(f"Connection test failed: {e}")
            
        except CredentialError as e:
            result["error"] = f"Authentication failed: {str(e)}"
            logger.error(f"Authentication failed: {e}")
            
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected error during connection test: {e}")
        
        return result
    
    async def connect(self, connection_string: str) -> bool:
        """Connect to Azure IoT Hub"""
        if not AZURE_AVAILABLE:
            logger.error("Azure IoT SDK not available")
            return False
        
        try:
            # Parse and validate connection string
            connection_info = self.parse_connection_string(connection_string)
            if not connection_info:
                return False
            
            # Create client
            self.client = IoTHubDeviceClient.create_from_connection_string(connection_string)
            
            # Connect
            await self.client.connect()
            
            self.connection_info = connection_info
            self.is_connected = True
            
            # Emit connection event
            self.emit_event(EventType.DEVICE_CONNECTED, {
                "device_id": connection_info.device_id,
                "hub_name": connection_info.hub_name
            })
            
            logger.info(f"Connected to Azure IoT Hub: {connection_info.hub_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Azure IoT Hub: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from Azure IoT Hub"""
        try:
            if self.client and self.is_connected:
                await self.client.disconnect()
                
                # Emit disconnection event
                if self.connection_info:
                    self.emit_event(EventType.DEVICE_DISCONNECTED, {
                        "device_id": self.connection_info.device_id,
                        "hub_name": self.connection_info.hub_name
                    })
                
                logger.info("Disconnected from Azure IoT Hub")
            
            self.client = None
            self.is_connected = False
            
        except Exception as e:
            logger.error(f"Error during disconnection: {e}")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        return {
            "connected": self.is_connected,
            "connection_info": self.connection_info,
            "client_available": self.client is not None,
            "azure_sdk_available": AZURE_AVAILABLE
        }
    
    def get_client(self) -> Optional[IoTHubDeviceClient]:
        """Get the IoT Hub client"""
        return self.client if self.is_connected else None


"""
Event system for Azure IoT Hub Device Simulator
"""

from enum import Enum
from typing import Any, Callable, Dict, List
from dataclasses import dataclass
import threading
from datetime import datetime

from .logging_config import get_logger

logger = get_logger('events')


class EventType(Enum):
    """Event types for the application"""
    # Application events
    APP_STARTED = "app_started"
    APP_CLOSING = "app_closing"
    
    # Device events
    DEVICE_ADDED = "device_added"
    DEVICE_REMOVED = "device_removed"
    DEVICE_UPDATED = "device_updated"
    DEVICE_CONNECTED = "device_connected"
    DEVICE_DISCONNECTED = "device_disconnected"
    
    # Simulation events
    SIMULATION_STARTED = "simulation_started"
    SIMULATION_STOPPED = "simulation_stopped"
    SIMULATION_PAUSED = "simulation_paused"
    SIMULATION_RESUMED = "simulation_resumed"
    
    # Message events
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_FAILED = "message_failed"
    
    # Configuration events
    CONFIG_CHANGED = "config_changed"
    AZURE_CONFIG_CHANGED = "azure_config_changed"
    
    # Template events
    TEMPLATE_CREATED = "template_created"
    TEMPLATE_UPDATED = "template_updated"
    TEMPLATE_DELETED = "template_deleted"
    
    # Monitoring events
    METRICS_UPDATED = "metrics_updated"
    PERFORMANCE_ALERT = "performance_alert"


@dataclass
class Event:
    """Event data structure"""
    event_type: EventType
    source: str
    data: Any = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventBus:
    """Event bus for application-wide communication"""
    
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}
        self._lock = threading.RLock()
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Subscribe to an event type"""
        with self._lock:
            if event_type not in self._handlers:
                self._handlers[event_type] = []
            
            if handler not in self._handlers[event_type]:
                self._handlers[event_type].append(handler)
                logger.debug(f"Handler subscribed to {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Unsubscribe from an event type"""
        with self._lock:
            if event_type in self._handlers:
                if handler in self._handlers[event_type]:
                    self._handlers[event_type].remove(handler)
                    logger.debug(f"Handler unsubscribed from {event_type.value}")
    
    def emit(self, event_type: EventType, source: str, data: Any = None):
        """Emit an event"""
        event = Event(event_type, source, data)
        
        with self._lock:
            handlers = self._handlers.get(event_type, []).copy()
        
        logger.debug(f"Emitting event {event_type.value} from {source}")
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event_type.value}: {e}")


class EventMixin:
    """Mixin class for objects that need to emit events"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event_bus = event_bus
    
    def emit_event(self, event_type: EventType, data: Any = None):
        """Emit an event from this object"""
        source = self.__class__.__name__
        self._event_bus.emit(event_type, source, data)
    
    def subscribe_to_event(self, event_type: EventType, handler: Callable[[Event], None]):
        """Subscribe to an event type"""
        self._event_bus.subscribe(event_type, handler)
    
    def unsubscribe_from_event(self, event_type: EventType, handler: Callable[[Event], None]):
        """Unsubscribe from an event type"""
        self._event_bus.unsubscribe(event_type, handler)


# Global event bus instance
event_bus = EventBus()


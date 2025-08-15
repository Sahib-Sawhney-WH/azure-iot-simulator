"""Metrics collector for real-time monitoring"""
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, deque
from core.logging_config import get_logger
from core.events import EventMixin, EventType

logger = get_logger('metrics_collector')

class MetricsCollector(EventMixin):
    def __init__(self):
        super().__init__()
        self.device_metrics = defaultdict(lambda: {
            "message_count": 0,
            "error_count": 0,
            "last_message_time": None,
            "connection_status": "disconnected",
            "simulation_status": "stopped"
        })
        
        self.system_metrics = {
            "total_messages": 0,
            "total_errors": 0,
            "messages_per_second": 0.0,
            "active_devices": 0,
            "connected_devices": 0
        }
        
        # Historical data (last 24 hours, 1-minute intervals)
        self.history_size = 24 * 60  # 24 hours * 60 minutes
        self.message_history = deque(maxlen=self.history_size)
        self.error_history = deque(maxlen=self.history_size)
        
        self.start_time = datetime.now()
        self._last_update = time.time()
    
    def record_message_sent(self, device_id: str, message_data: Dict[str, Any]):
        """Record a message sent event"""
        self.device_metrics[device_id]["message_count"] += 1
        self.device_metrics[device_id]["last_message_time"] = datetime.now()
        
        self.system_metrics["total_messages"] += 1
        
        # Update historical data
        current_time = datetime.now()
        self.message_history.append((current_time, 1))
        
        self._update_rates()
        
        # Emit metrics update event
        self.emit_event(EventType.METRICS_UPDATED, {
            "device_id": device_id,
            "metric_type": "message_sent",
            "timestamp": current_time
        })
    
    def record_message_error(self, device_id: str, error_data: Dict[str, Any]):
        """Record a message error event"""
        self.device_metrics[device_id]["error_count"] += 1
        
        self.system_metrics["total_errors"] += 1
        
        # Update historical data
        current_time = datetime.now()
        self.error_history.append((current_time, 1))
        
        # Emit metrics update event
        self.emit_event(EventType.METRICS_UPDATED, {
            "device_id": device_id,
            "metric_type": "message_error",
            "timestamp": current_time
        })
    
    def update_device_status(self, device_id: str, status_data: Dict[str, Any]):
        """Update device connection and simulation status"""
        metrics = self.device_metrics[device_id]
        
        old_connected = metrics["connection_status"] == "connected"
        old_simulating = metrics["simulation_status"] == "running"
        
        metrics["connection_status"] = "connected" if status_data.get("connected", False) else "disconnected"
        metrics["simulation_status"] = "running" if status_data.get("simulating", False) else "stopped"
        
        # Update system counters
        new_connected = metrics["connection_status"] == "connected"
        new_simulating = metrics["simulation_status"] == "running"
        
        if new_connected != old_connected:
            if new_connected:
                self.system_metrics["connected_devices"] += 1
            else:
                self.system_metrics["connected_devices"] -= 1
        
        if new_simulating != old_simulating:
            if new_simulating:
                self.system_metrics["active_devices"] += 1
            else:
                self.system_metrics["active_devices"] -= 1
    
    def _update_rates(self):
        """Update calculated rates"""
        current_time = time.time()
        time_diff = current_time - self._last_update
        
        if time_diff >= 1.0:  # Update every second
            # Calculate messages per second over last minute
            one_minute_ago = datetime.now() - timedelta(minutes=1)
            recent_messages = [
                count for timestamp, count in self.message_history
                if timestamp >= one_minute_ago
            ]
            
            self.system_metrics["messages_per_second"] = sum(recent_messages) / 60.0
            self._last_update = current_time
    
    def get_device_metrics(self, device_id: str) -> Dict[str, Any]:
        """Get metrics for a specific device"""
        return dict(self.device_metrics[device_id])
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system-wide metrics"""
        uptime = datetime.now() - self.start_time
        
        return {
            **self.system_metrics,
            "uptime_seconds": uptime.total_seconds(),
            "total_devices": len(self.device_metrics)
        }
    
    def get_historical_data(self, hours: int = 1) -> Dict[str, List]:
        """Get historical metrics data"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter historical data
        message_data = [
            {"timestamp": ts.isoformat(), "count": count}
            for ts, count in self.message_history
            if ts >= cutoff_time
        ]
        
        error_data = [
            {"timestamp": ts.isoformat(), "count": count}
            for ts, count in self.error_history
            if ts >= cutoff_time
        ]
        
        return {
            "messages": message_data,
            "errors": error_data
        }
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for reporting"""
        return {
            "system_metrics": self.get_system_metrics(),
            "device_metrics": dict(self.device_metrics),
            "historical_data": self.get_historical_data(24),  # Last 24 hours
            "export_timestamp": datetime.now().isoformat()
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.device_metrics.clear()
        self.system_metrics = {
            "total_messages": 0,
            "total_errors": 0,
            "messages_per_second": 0.0,
            "active_devices": 0,
            "connected_devices": 0
        }
        self.message_history.clear()
        self.error_history.clear()
        self.start_time = datetime.now()
        
        logger.info("Metrics reset")

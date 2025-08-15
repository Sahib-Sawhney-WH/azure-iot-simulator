"""Performance monitor for system resources"""
import time
from datetime import datetime
from typing import Dict, Any, List
from collections import deque

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

from core.logging_config import get_logger
from core.events import EventMixin, EventType

logger = get_logger('performance_monitor')

class PerformanceMonitor(EventMixin):
    def __init__(self):
        super().__init__()
        self.history_size = 300  # 5 minutes of data (1 sample per second)
        
        # Performance history
        self.cpu_history = deque(maxlen=self.history_size)
        self.memory_history = deque(maxlen=self.history_size)
        self.disk_history = deque(maxlen=self.history_size)
        self.network_history = deque(maxlen=self.history_size)
        
        # Performance baselines
        self.baseline_cpu = 0.0
        self.baseline_memory = 0.0
        self.baseline_established = False
        
        # Alert thresholds
        self.cpu_threshold = 80.0  # %
        self.memory_threshold = 85.0  # %
        self.disk_threshold = 90.0  # %
        
        # Alert state
        self.alerts_enabled = True
        self.active_alerts = set()
        
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available - performance monitoring disabled")
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current performance metrics"""
        if not PSUTIL_AVAILABLE:
            return self._get_dummy_metrics()
        
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB
            
            # Network metrics (if available)
            try:
                network = psutil.net_io_counters()
                network_sent = network.bytes_sent / (1024**2)  # MB
                network_recv = network.bytes_recv / (1024**2)  # MB
            except:
                network_sent = network_recv = 0
            
            metrics = {
                "timestamp": datetime.now(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count
                },
                "memory": {
                    "percent": memory_percent,
                    "available_gb": round(memory_available, 2),
                    "total_gb": round(memory_total, 2),
                    "used_gb": round(memory_total - memory_available, 2)
                },
                "disk": {
                    "percent": disk_percent,
                    "free_gb": round(disk_free, 2),
                    "total_gb": round(disk_total, 2),
                    "used_gb": round(disk_total - disk_free, 2)
                },
                "network": {
                    "sent_mb": round(network_sent, 2),
                    "received_mb": round(network_recv, 2)
                }
            }
            
            # Store in history
            self._store_metrics(metrics)
            
            # Check for alerts
            self._check_alerts(metrics)
            
            # Establish baseline if needed
            if not self.baseline_established:
                self._establish_baseline(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")
            return self._get_dummy_metrics()
    
    def _get_dummy_metrics(self) -> Dict[str, Any]:
        """Get dummy metrics when psutil is not available"""
        return {
            "timestamp": datetime.now(),
            "cpu": {"percent": 0.0, "count": 1},
            "memory": {"percent": 0.0, "available_gb": 0.0, "total_gb": 0.0, "used_gb": 0.0},
            "disk": {"percent": 0.0, "free_gb": 0.0, "total_gb": 0.0, "used_gb": 0.0},
            "network": {"sent_mb": 0.0, "received_mb": 0.0}
        }
    
    def _store_metrics(self, metrics: Dict[str, Any]):
        """Store metrics in history"""
        self.cpu_history.append((metrics["timestamp"], metrics["cpu"]["percent"]))
        self.memory_history.append((metrics["timestamp"], metrics["memory"]["percent"]))
        self.disk_history.append((metrics["timestamp"], metrics["disk"]["percent"]))
        
        # Network rate (simplified)
        network_total = metrics["network"]["sent_mb"] + metrics["network"]["received_mb"]
        self.network_history.append((metrics["timestamp"], network_total))
    
    def _check_alerts(self, metrics: Dict[str, Any]):
        """Check for performance alerts"""
        if not self.alerts_enabled:
            return
        
        alerts_to_trigger = []
        alerts_to_clear = []
        
        # CPU alert
        if metrics["cpu"]["percent"] > self.cpu_threshold:
            if "cpu_high" not in self.active_alerts:
                alerts_to_trigger.append(("cpu_high", f"CPU usage high: {metrics['cpu']['percent']:.1f}%"))
        else:
            if "cpu_high" in self.active_alerts:
                alerts_to_clear.append("cpu_high")
        
        # Memory alert
        if metrics["memory"]["percent"] > self.memory_threshold:
            if "memory_high" not in self.active_alerts:
                alerts_to_trigger.append(("memory_high", f"Memory usage high: {metrics['memory']['percent']:.1f}%"))
        else:
            if "memory_high" in self.active_alerts:
                alerts_to_clear.append("memory_high")
        
        # Disk alert
        if metrics["disk"]["percent"] > self.disk_threshold:
            if "disk_high" not in self.active_alerts:
                alerts_to_trigger.append(("disk_high", f"Disk usage high: {metrics['disk']['percent']:.1f}%"))
        else:
            if "disk_high" in self.active_alerts:
                alerts_to_clear.append("disk_high")
        
        # Trigger new alerts
        for alert_type, message in alerts_to_trigger:
            self.active_alerts.add(alert_type)
            self.emit_event(EventType.PERFORMANCE_ALERT, {
                "alert_type": alert_type,
                "message": message,
                "timestamp": datetime.now()
            })
            logger.warning(f"Performance alert: {message}")
        
        # Clear resolved alerts
        for alert_type in alerts_to_clear:
            self.active_alerts.discard(alert_type)
            logger.info(f"Performance alert cleared: {alert_type}")
    
    def _establish_baseline(self, metrics: Dict[str, Any]):
        """Establish performance baseline"""
        if len(self.cpu_history) >= 30:  # 30 seconds of data
            cpu_values = [value for _, value in list(self.cpu_history)[-30:]]
            memory_values = [value for _, value in list(self.memory_history)[-30:]]
            
            self.baseline_cpu = sum(cpu_values) / len(cpu_values)
            self.baseline_memory = sum(memory_values) / len(memory_values)
            self.baseline_established = True
            
            logger.info(f"Performance baseline established - CPU: {self.baseline_cpu:.1f}%, Memory: {self.baseline_memory:.1f}%")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        current_metrics = self.collect_metrics()
        
        # Calculate averages over last minute
        one_minute_ago = datetime.now().timestamp() - 60
        
        recent_cpu = [value for ts, value in self.cpu_history if ts.timestamp() > one_minute_ago]
        recent_memory = [value for ts, value in self.memory_history if ts.timestamp() > one_minute_ago]
        
        avg_cpu = sum(recent_cpu) / len(recent_cpu) if recent_cpu else 0
        avg_memory = sum(recent_memory) / len(recent_memory) if recent_memory else 0
        
        return {
            "current": current_metrics,
            "averages": {
                "cpu_1min": round(avg_cpu, 1),
                "memory_1min": round(avg_memory, 1)
            },
            "baseline": {
                "cpu": round(self.baseline_cpu, 1) if self.baseline_established else None,
                "memory": round(self.baseline_memory, 1) if self.baseline_established else None
            },
            "active_alerts": list(self.active_alerts),
            "psutil_available": PSUTIL_AVAILABLE
        }
    
    def get_historical_data(self, minutes: int = 5) -> Dict[str, List]:
        """Get historical performance data"""
        cutoff_time = datetime.now().timestamp() - (minutes * 60)
        
        cpu_data = [
            {"timestamp": ts.isoformat(), "value": value}
            for ts, value in self.cpu_history
            if ts.timestamp() > cutoff_time
        ]
        
        memory_data = [
            {"timestamp": ts.isoformat(), "value": value}
            for ts, value in self.memory_history
            if ts.timestamp() > cutoff_time
        ]
        
        return {
            "cpu": cpu_data,
            "memory": memory_data,
            "timespan_minutes": minutes
        }
    
    def set_alert_thresholds(self, cpu: float = None, memory: float = None, disk: float = None):
        """Set alert thresholds"""
        if cpu is not None:
            self.cpu_threshold = cpu
        if memory is not None:
            self.memory_threshold = memory
        if disk is not None:
            self.disk_threshold = disk
        
        logger.info(f"Alert thresholds updated - CPU: {self.cpu_threshold}%, Memory: {self.memory_threshold}%, Disk: {self.disk_threshold}%")
    
    def enable_alerts(self, enabled: bool = True):
        """Enable or disable alerts"""
        self.alerts_enabled = enabled
        if not enabled:
            self.active_alerts.clear()
        logger.info(f"Performance alerts {'enabled' if enabled else 'disabled'}")
    
    def reset_baseline(self):
        """Reset performance baseline"""
        self.baseline_established = False
        self.baseline_cpu = 0.0
        self.baseline_memory = 0.0
        logger.info("Performance baseline reset")
